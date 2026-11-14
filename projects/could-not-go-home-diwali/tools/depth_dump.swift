// depth_dump.swift — dump an Apple Cinematic Video's disparity (depth) frames and the recorded focus, reel-local
// (could-not-go-home-diwali v3c: director's note "the background should have more of that effect and the subject a
// little more highlighted ... the character playing in depth").
//
// Writes <out>.f32 (float32 disparity frames, natural/sensor orientation, row-major, concatenated) and <out>.json
// ({w, h, fps, frames, xform:[a,b,c,d,tx,ty], focus:[recorded focus disparity per frame], t:[source seconds]}).
// The picture's display rotation is `xform` (same as the camera file's preferredTransform).
//
// Build:  swiftc -O -o tools/depth_dump tools/depth_dump.swift
// Usage:  tools/depth_dump <camera.mov> <out_prefix> [--start S] [--dur D (0 = to end)] [--every N]

import AVFoundation
import Cinematic
import CoreMedia
import CoreVideo
import Foundation

func die(_ msg: String) -> Never { FileHandle.standardError.write((msg + "\n").data(using: .utf8)!); exit(1) }

var args = Array(CommandLine.arguments.dropFirst())
guard args.count >= 2 else { die("usage: depth_dump <camera.mov> <out_prefix> [--start S] [--dur D] [--every N]") }
let inURL = URL(fileURLWithPath: args.removeFirst())
let outPrefix = args.removeFirst()
var startS = 0.0, durS = 0.0, every = 1
while !args.isEmpty {
    switch args.removeFirst() {
    case "--start": startS = Double(args.removeFirst())!
    case "--dur": durS = Double(args.removeFirst())!
    case "--every": every = max(1, Int(args.removeFirst())!)
    default: die("unknown arg")
    }
}

let sem = DispatchSemaphore(value: 0)
Task {
    do {
        let asset = AVURLAsset(url: inURL)
        guard await CNAssetInfo.isCinematic(asset: asset) else { die("not a Cinematic asset: \(inURL.path)") }
        let info = try await CNAssetInfo(asset: asset)
        let sessionAttrs = try await CNRenderingSession.Attributes(asset: asset)
        let vTrack = info.cinematicVideoTrack
        let xf = try await vTrack.load(.preferredTransform)
        let fps = try await vTrack.load(.nominalFrameRate)
        let reader = try AVAssetReader(asset: asset)
        let full = info.timeRange
        let st = CMTime(seconds: startS, preferredTimescale: 600)
        let du = durS > 0 ? CMTime(seconds: durS, preferredTimescale: 600) : CMTimeSubtract(full.duration, st)
        reader.timeRange = CMTimeRange(start: CMTimeAdd(full.start, st), duration: du)
        let dOut = AVAssetReaderTrackOutput(track: info.cinematicDisparityTrack,
                                            outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_DisparityFloat16])
        let mOut = AVAssetReaderTrackOutput(track: info.cinematicMetadataTrack, outputSettings: nil)
        for o in [dOut, mOut] { o.alwaysCopiesSampleData = false; reader.add(o) }
        guard reader.startReading() else { die("reader: \(String(describing: reader.error))") }

        FileManager.default.createFile(atPath: outPrefix + ".f32", contents: nil)
        let fh = try FileHandle(forWritingTo: URL(fileURLWithPath: outPrefix + ".f32"))
        var W = 0, H = 0, n = 0, k = 0
        var focus: [Float] = [], times: [Double] = []
        var pendingM: CMSampleBuffer? = nil
        while let ds = dOut.copyNextSampleBuffer() {
            guard let buf = CMSampleBufferGetImageBuffer(ds) else { continue }
            let t = CMSampleBufferGetPresentationTimeStamp(ds)
            // metadata sample at or before t
            var best = pendingM
            while true {
                if let b = best, CMTimeCompare(CMSampleBufferGetPresentationTimeStamp(b), t) >= 0 { break }
                guard let s = mOut.copyNextSampleBuffer() else { break }
                if CMSampleBufferGetNumSamples(s) == 0 { continue }
                best = s
            }
            pendingM = best
            defer { k += 1 }
            if k % every != 0 { continue }
            var f: Float = .nan
            if let m = best, let fa = CNRenderingSession.FrameAttributes(sampleBuffer: m, sessionAttributes: sessionAttrs) { f = fa.focusDisparity }
            CVPixelBufferLockBaseAddress(buf, .readOnly)
            W = CVPixelBufferGetWidth(buf); H = CVPixelBufferGetHeight(buf)
            let row = CVPixelBufferGetBytesPerRow(buf)
            let base = CVPixelBufferGetBaseAddress(buf)!
            var out = [Float](repeating: 0, count: W * H)
            for y in 0..<H {
                let p = base.advanced(by: y * row).assumingMemoryBound(to: Float16.self)
                for x in 0..<W { out[y * W + x] = Float(p[x]) }
            }
            CVPixelBufferUnlockBaseAddress(buf, .readOnly)
            out.withUnsafeBufferPointer { fh.write(Data(buffer: $0)) }
            focus.append(f); times.append(CMTimeSubtract(t, full.start).seconds); n += 1
        }
        try fh.close()
        let meta: [String: Any] = ["w": W, "h": H, "fps": fps, "frames": n,
                                   "xform": [xf.a, xf.b, xf.c, xf.d, xf.tx, xf.ty], "focus": focus.map { $0.isFinite ? Double($0) : -1 }, "t": times]
        let data = try JSONSerialization.data(withJSONObject: meta, options: [.prettyPrinted])
        try data.write(to: URL(fileURLWithPath: outPrefix + ".json"))
        print("✓ \(outPrefix).f32: \(n) frames \(W)x\(H), xform \(xf)")
    } catch { FileHandle.standardError.write("error: \(error)\n".data(using: .utf8)!); exit(1) }
    sem.signal()
}
sem.wait()
