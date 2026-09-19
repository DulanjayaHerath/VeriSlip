import Vision
import Foundation
import AppKit

guard CommandLine.arguments.count > 1 else {
    print("[]")
    exit(0)
}

let imagePath = CommandLine.arguments[1]
let url = URL(fileURLWithPath: imagePath)

guard let image = NSImage(contentsOf: url),
      let tiffData = image.tiffRepresentation,
      let bitmap = NSBitmapImageRep(data: tiffData),
      let cgImage = bitmap.cgImage else {
    print("[]")
    exit(0)
}

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false
request.recognitionLanguages = ["en-US", "si", "ta"]

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try? handler.perform([request])

struct OCRResult: Codable {
    let text: String
    let confidence: Float
    let x: Double
    let y: Double
    let w: Double
    let h: Double
}

var output: [OCRResult] = []

let imgW = Double(cgImage.width)
let imgH = Double(cgImage.height)

if let results = request.results {
    for obs in results {
        guard let candidate = obs.topCandidates(1).first else { continue }
        // Vision coordinates are normalized (0..1) with bottom-left origin
        let box = obs.boundingBox
        let x = box.origin.x * imgW
        let y = (1.0 - box.origin.y - box.size.height) * imgH
        let w = box.size.width * imgW
        let h = box.size.height * imgH
        
        output.append(OCRResult(
            text: candidate.string,
            confidence: candidate.confidence,
            x: round(x * 10) / 10,
            y: round(y * 10) / 10,
            w: round(w * 10) / 10,
            h: round(h * 10) / 10
        ))
    }
}

let jsonData = (try? JSONEncoder().encode(output)) ?? Data()
if let jsonStr = String(data: jsonData, encoding: .utf8) {
    print(jsonStr)
} else {
    print("[]")
}
