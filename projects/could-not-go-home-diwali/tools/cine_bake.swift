// cine_bake.swift — bake Apple Cinematic Video depth-of-field into a plain ProRes file.
//
// Reel-local tool (could-not-go-home-diwali). The director shot in Blackmagic Cam's Cinematic mode
// (com.apple.quicktime.cinematic-video-intent=1). The file holds a sharp image plus a disparity track
// ("dish") and focus metadata ("mebx"); Apple apps draw the blur at playback, Premiere/ffmpeg don't.
// This renders the blur with Apple's Cinematic framework (CNRenderingSession) using the recorded focus
// decisions, optionally overriding the f-number, and writes ProRes 422 HQ with the source's rotation tag,
// so the output is a drop-in replacement for the camera file (same size, fps, timing, orientation tag).
//
// Build:  swiftc -O -o tools/cine_bake tools/cine_bake.swift
// Usage:  tools/cine_bake <in.mov> <out.mov> [--fnumber 2.8] [--start 0] [--dur 0 (=all)] [--audio]
//
// Audio: passed through (AAC → PCM) only with --audio.

import AVFoundation
import Cinematic
import CoreMedia
import CoreVideo
import Foundation
import Metal

func die(_ msg: String) -> Never {
    FileHandle.standardError.write((msg + "\n").data(using: .utf8)!)
    exit(1)
}

var args = Array(CommandLine.arguments.dropFirst())
guard args.count >= 2 else { die("usage: cine_bake <in.mov> <out.mov> [--fnumber F] [--start S] [--dur D] [--audio]") }
let inURL = URL(fileURLWithPath: args.removeFirst())
let outURL = URL(fileURLWithPath: args.removeFirst())
var fOverride: Float? = nil
var startS = 0.0
var durS = 0.0
var withAudio = false
var passthrough = false
// Rack focus (v1b): --rack "t0,t1,ax,ay,aw,ah,bx,by,bw,bh": focus on rect A until t0, ease to rect B by t1 (seconds from the
// output's start; rects normalised 0–1, top-left origin, in the stored picture = the upright landscape frame). Each rect's
// disparity is its median, measured on every frame, so the focus follows the subject's depth. A rect of width 0 means
// "the camera's recorded focus" (Apple's face/subject tracking), for a subject that moves across the frame.
var rack: [Double]? = nil
var focusDump = false
while !args.isEmpty {
    let a = args.removeFirst()
    switch a {
    case "--fnumber": fOverride = Float(args.removeFirst())
    case "--start": startS = Double(args.removeFirst())!
    case "--dur": durS = Double(args.removeFirst())!
    case "--audio": withAudio = true
    case "--passthrough": passthrough = true
    case "--rack": rack = args.removeFirst().split(separator: ",").map { Double($0)! }; if rack!.count != 10 { die("--rack needs 10 numbers") }
    case "--focus-dump": focusDump = true
    default: die("unknown arg \(a)")
    }
}

let sem = DispatchSemaphore(value: 0)
var exitCode: Int32 = 0

Task {
    do {
        let asset = AVURLAsset(url: inURL)
        guard await CNAssetInfo.isCinematic(asset: asset) else { die("not a Cinematic asset: \(inURL.path)") }
        let info = try await CNAssetInfo(asset: asset)
        let sessionAttrs = try await CNRenderingSession.Attributes(asset: asset)
        let vTrack = info.cinematicVideoTrack
        let dTrack = info.cinematicDisparityTrack
        let mTrack = info.cinematicMetadataTrack
        let natural = info.naturalSize
        let xform = try await vTrack.load(.preferredTransform)
        let fps = try await vTrack.load(.nominalFrameRate)
        print("in: \(inURL.lastPathComponent) natural \(Int(natural.width))x\(Int(natural.height)) fps \(fps) renderingVersion \(sessionAttrs.renderingVersion)")
        print("source formats: \(CNRenderingSession.sourcePixelFormatTypes.map { fourcc($0) })  dest formats: \(CNRenderingSession.destinationPixelFormatTypes.map { fourcc($0) })")

        let srcFmt = CNRenderingSession.sourcePixelFormatTypes.first!
        let dstFmt = CNRenderingSession.destinationPixelFormatTypes.first!

        let reader = try AVAssetReader(asset: asset)
        let full = info.timeRange
        if startS > 0 || durS > 0 {
            let st = CMTime(seconds: startS, preferredTimescale: 600)
            let du = durS > 0 ? CMTime(seconds: durS, preferredTimescale: 600) : CMTimeSubtract(full.duration, st)
            reader.timeRange = CMTimeRange(start: CMTimeAdd(full.start, st), duration: du)
        }
        let vOut = AVAssetReaderTrackOutput(track: vTrack, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: srcFmt])
        let dOut = AVAssetReaderTrackOutput(track: dTrack, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_DisparityFloat16])
        let mOut = AVAssetReaderTrackOutput(track: mTrack, outputSettings: nil)
        for o in [vOut, dOut, mOut] { o.alwaysCopiesSampleData = false; reader.add(o) }
        var aOut: AVAssetReaderTrackOutput? = nil
        if withAudio, let aTrack = try await asset.loadTracks(withMediaType: .audio).first {
            let ao = AVAssetReaderTrackOutput(track: aTrack, outputSettings: [AVFormatIDKey: kAudioFormatLinearPCM, AVLinearPCMBitDepthKey: 24, AVLinearPCMIsFloatKey: false, AVLinearPCMIsBigEndianKey: false, AVLinearPCMIsNonInterleaved: false])
            reader.add(ao); aOut = ao
        }
        guard reader.startReading() else { die("reader: \(String(describing: reader.error))") }

        try? FileManager.default.removeItem(at: outURL)
        let writer = try AVAssetWriter(outputURL: outURL, fileType: .mov)
        let vIn = AVAssetWriterInput(mediaType: .video, outputSettings: [
            AVVideoCodecKey: AVVideoCodecType.proRes422HQ,
            AVVideoWidthKey: Int(natural.width), AVVideoHeightKey: Int(natural.height),
            AVVideoColorPropertiesKey: [AVVideoColorPrimariesKey: AVVideoColorPrimaries_ITU_R_709_2,
                                        AVVideoTransferFunctionKey: AVVideoTransferFunction_ITU_R_709_2,
                                        AVVideoYCbCrMatrixKey: AVVideoYCbCrMatrix_ITU_R_709_2]])
        vIn.transform = xform
        vIn.expectsMediaDataInRealTime = false
        let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: vIn, sourcePixelBufferAttributes: [
            kCVPixelBufferPixelFormatTypeKey as String: dstFmt,
            kCVPixelBufferWidthKey as String: Int(natural.width), kCVPixelBufferHeightKey as String: Int(natural.height),
            kCVPixelBufferMetalCompatibilityKey as String: true, kCVPixelBufferIOSurfacePropertiesKey as String: [:]])
        writer.add(vIn)
        var aIn: AVAssetWriterInput? = nil
        if aOut != nil {
            let ai = AVAssetWriterInput(mediaType: .audio, outputSettings: nil)
            ai.expectsMediaDataInRealTime = false
            writer.add(ai); aIn = ai
        }
        guard writer.startWriting() else { die("writer: \(String(describing: writer.error))") }

        guard let device = MTLCreateSystemDefaultDevice(), let queue = device.makeCommandQueue() else { die("no Metal") }
        let session = CNRenderingSession(commandQueue: queue, sessionAttributes: sessionAttrs, preferredTransform: .identity, quality: .export)

        var started = false
        var t0src = CMTime.zero
        var n = 0
        var pendingD: CMSampleBuffer? = nil
        var pendingM: CMSampleBuffer? = nil
        func nextMatching(_ out: AVAssetReaderTrackOutput, _ pending: inout CMSampleBuffer?, _ t: CMTime) -> CMSampleBuffer? {
            // advance until the sample whose PTS is the latest ≤ t (tracks share timing; tolerate tiny offsets)
            var best = pending
            while true {
                if let b = best, CMTimeCompare(CMSampleBufferGetPresentationTimeStamp(b), t) >= 0 { break }
                guard let s = out.copyNextSampleBuffer() else { break }
                if CMSampleBufferGetNumSamples(s) == 0 { continue }
                best = s
            }
            pending = best
            return best
        }
        while let vs = vOut.copyNextSampleBuffer() {
            guard let src = CMSampleBufferGetImageBuffer(vs) else { continue }
            let t = CMSampleBufferGetPresentationTimeStamp(vs)
            guard let ds = nextMatching(dOut, &pendingD, t), let disp = CMSampleBufferGetImageBuffer(ds) else { die("no disparity at \(t.seconds)") }
            guard let ms = nextMatching(mOut, &pendingM, t) else { die("no metadata at \(t.seconds)") }
            guard var fa = CNRenderingSession.FrameAttributes(sampleBuffer: ms, sessionAttributes: sessionAttrs) else { die("frame attrs failed at \(t.seconds)") }
            if let f = fOverride { fa.fNumber = f }
            if !started { writer.startSession(atSourceTime: t); started = true; t0src = t }
            let tl = CMTimeSubtract(t, t0src).seconds
            if let r = rack {
                let recorded = fa.focusDisparity
                let dA = r[4] > 0 ? rectDisparity(disp, r[2], r[3], r[4], r[5]) : recorded
                let dB = r[8] > 0 ? rectDisparity(disp, r[6], r[7], r[8], r[9]) : recorded  // a zero-width rect = the camera's recorded focus (its own subject tracking)
                var u = r[1] > r[0] ? (tl - r[0]) / (r[1] - r[0]) : (tl >= r[0] ? 1 : 0)
                u = min(max(u, 0), 1); u = u * u * (3 - 2 * u)
                fa.focusDisparity = Float(Double(dA) + (Double(dB) - Double(dA)) * u)
                if focusDump { print(String(format: "  t=%.2f dA=%.3f dB=%.3f focus=%.3f recorded→%.3f", tl, dA, dB, fa.focusDisparity, fa.focusDisparity)) }
            } else if focusDump {
                print(String(format: "  t=%.2f recorded focus=%.3f  centre=%.3f", tl, fa.focusDisparity, rectDisparity(disp, 0.4, 0.4, 0.2, 0.2)))
            }
            var dst: CVPixelBuffer? = nil
            CVPixelBufferPoolCreatePixelBuffer(nil, adaptor.pixelBufferPool!, &dst)
            guard let dstBuf = dst else { die("no dst buffer") }
            guard let cb = queue.makeCommandBuffer() else { die("no command buffer") }
            guard session.encodeRender(to: cb, frameAttributes: fa, sourceImage: src, sourceDisparity: disp, destinationImage: dstBuf) else { die("encodeRender failed at \(t.seconds)") }
            cb.commit(); cb.waitUntilCompleted()
            while !vIn.isReadyForMoreMediaData { usleep(2000) }
            adaptor.append(passthrough ? src : dstBuf, withPresentationTime: t)
            if n == 0 || n % 50 == 0 { print(String(format: "  frame %d t=%.2f fNumber=%.2f focusDisparity=%.3f", n, t.seconds, fa.fNumber, fa.focusDisparity)) }
            n += 1
        }
        vIn.markAsFinished()
        if let ao = aOut, let ai = aIn {
            while let s = ao.copyNextSampleBuffer() {
                while !ai.isReadyForMoreMediaData { usleep(2000) }
                ai.append(s)
            }
            ai.markAsFinished()
        }
        await writer.finishWriting()
        if writer.status != .completed { die("writer failed: \(String(describing: writer.error))") }
        print("✓ \(outURL.path): \(n) frames")
    } catch {
        FileHandle.standardError.write("error: \(error)\n".data(using: .utf8)!)
        exitCode = 1
    }
    sem.signal()
}

/// Median disparity inside a normalised rect (top-left origin) of a DisparityFloat16 buffer.
func rectDisparity(_ buf: CVPixelBuffer, _ x: Double, _ y: Double, _ w: Double, _ h: Double) -> Float {
    CVPixelBufferLockBaseAddress(buf, .readOnly); defer { CVPixelBufferUnlockBaseAddress(buf, .readOnly) }
    let W = CVPixelBufferGetWidth(buf), H = CVPixelBufferGetHeight(buf), row = CVPixelBufferGetBytesPerRow(buf)
    guard let base = CVPixelBufferGetBaseAddress(buf) else { return 0 }
    let x0 = max(0, Int(x * Double(W))), x1 = min(W, Int((x + w) * Double(W)))
    let y0 = max(0, Int(y * Double(H))), y1 = min(H, Int((y + h) * Double(H)))
    var vals: [Float] = []
    for yy in y0..<max(y1, y0 + 1) {
        let p = base.advanced(by: yy * row).assumingMemoryBound(to: Float16.self)
        for xx in x0..<max(x1, x0 + 1) { let v = Float(p[xx]); if v.isFinite { vals.append(v) } }
    }
    if vals.isEmpty { return 0 }
    vals.sort(); return vals[vals.count / 2]
}

func fourcc(_ n: OSType) -> String {
    let v = n
    let c = [24, 16, 8, 0].map { Character(UnicodeScalar(UInt8((v >> UInt32($0)) & 0xff))) }
    return String(c)
}

sem.wait()
exit(exitCode)
