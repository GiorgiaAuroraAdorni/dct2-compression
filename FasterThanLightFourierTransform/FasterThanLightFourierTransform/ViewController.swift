//
//  ViewController.swift
//  FasterThanLightFourierTransform
//
//  Created by Giorgia Adorni on 01/06/2019.
//  Copyright © 2019 Giorgia e Elia. All rights reserved.
//

import Cocoa
import Quartz

class ViewController: NSViewController {

    @IBOutlet weak var originalImageWell: ImageView!
    @IBOutlet weak var compressedImageWell: ImageView!
    
    @IBOutlet weak var windowSlider: SliderView!
    @IBOutlet weak var cutOffSlider: SliderView!
    
    private let py = Python.import("main")
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
//        self.compressedImageWell.refusesFirstResponder = false
//        self.compressedImageWell.allowsCutCopyPaste = true
//        self.compressedImageWell.isEnabled = true
//        self.compressedImageWell.focusRingType = .exterior
        self.compressedImageWell.isEditable = true
        // FIXME: not really what I wanted
        
        self.windowSlider.minValue = 1
        self.windowSlider.value = 8
        self.windowSlider.maxValue = 64
        
        self.cutOffSlider.minValue = 0
        self.cutOffSlider.maxValue = 2 * self.windowSlider.value - 2
    }

    override func keyUp(with event: NSEvent) {
        // FIXME: shouldn't receive event when a text field is active
        guard event.characters == " " else {
            return super.keyUp(with: event)
        }
        
        self.toggleQuickLookPanel()
    }
    
    private func toggleQuickLookPanel() {
        let panel = QLPreviewPanel.shared()!
        
        if !panel.isVisible {
            panel.makeKeyAndOrderFront(self)
        } else {
            panel.close()
        }
    }
    
    @IBAction func userDidUpdateParameters(_ sender: Any) {
        self.cutOffSlider.maxValue = 2 * self.windowSlider.value - 2
        
        self.updateCompressedImage()
    }
    
    @IBAction func userDidDropImage(_ sender: NSImageView) {
        self.updateCompressedImage()
    }
    
    @IBAction func open(_ sender: NSButton) {
        let panel = NSOpenPanel()
        
        panel.allowedFileTypes = [kUTTypeImage as String]
        
        panel.directoryURL = URL(fileURLWithPath: NSHomeDirectory())
            .appendingPathComponent("FtlFT/images", isDirectory: true)
        
        panel.beginSheetModal(for: self.view.window!) { response in
            if response == .OK {
                let image = NSImage(contentsOf: panel.url!)

                self.originalImageWell.image = image
                self.updateCompressedImage()
            }
        }
    }
    
    @IBAction func runBenchmark(_ sender: Any) {
        let samples = benchmark(block: self.updateCompressedImage)
        
        summary(samples: samples)
    }
    
    // MARK: - Process updates
    
    func updateCompressedImage() {
        guard let image = self.originalImageWell.image else {
            return
        }
        
        let window = Int(self.windowSlider.value)
        let cutoff = Int(self.cutOffSlider.value)
        
        // TODO: do processing on background thread
        
        var compressedImage: NSImage?
        
        do {
            compressedImage = try self.generateCompressedImage(from: image, window: window, cutoff: cutoff)
        } catch {
            // TODO: show message to the user
            print(error)
        }
        
        self.compressedImageWell.image = compressedImage
    }
    
    private func generateCompressedImage(from image: NSImage, window: Int, cutoff: Int) throws -> NSImage {
        guard let imageArray = image.makeNumpyArray() else {
            throw NSError(domain: "FtlFT", code: 1, userInfo: [
                NSLocalizedDescriptionKey: "The format of the input image is not supported."
            ])
        }
        
        let compressed = try py.compress_image.throwing(imageArray, window: window, cutoff: cutoff)
        
        guard let compressedImage = NSImage(numpy: compressed) else {
            throw NSError(domain: "FtlFT", code: 2, userInfo: [
                NSLocalizedDescriptionKey: "Couldn't process output image"
            ])
        }
        
        return compressedImage
    }
}
