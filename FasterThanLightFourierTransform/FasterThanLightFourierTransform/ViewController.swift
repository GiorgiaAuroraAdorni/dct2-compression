//
//  ViewController.swift
//  FasterThanLightFourierTransform
//
//  Created by Giorgia Adorni on 01/06/2019.
//  Copyright © 2019 Giorgia e Elia. All rights reserved.
//

import Cocoa
import Quartz

private let py = Python.import("main")

class ViewController: NSViewController, NSMenuItemValidation {

    @IBOutlet weak var originalImageWell: ImageView!
    @IBOutlet weak var compressedImageWell: ImageView!
    
    @IBOutlet weak var windowSlider: SliderView!
    @IBOutlet weak var cutOffSlider: SliderView!
    @IBOutlet weak var outputControl: NSSegmentedControl!
    
    @IBOutlet weak var saveButton: NSButton!
    @IBOutlet weak var statusLabel: NSTextField!
    
    private var originalImage: NSImage? {
        get { return self.originalImageWell.image }
        set { self.originalImageWell.image = newValue; self.updateInterfaceState() }
    }
    
    private var compressedImage: NSImage? {
        get { return self.compressedImageWell.image }
        set { self.compressedImageWell.image = newValue; self.updateInterfaceState() }
    }
    
    enum OutputState: Int, PythonConvertible {
        case dct = 0
        case mask = 1
        case compressedDct = 2
        case compressedImage = 3
        
        var pythonObject: PythonObject {
            switch self {
            case .dct: return py.OUTPUT_DCT
            case .mask: return py.OUTPUT_MASK
            case .compressedDct: return py.OUTPUT_COMPRESSED_DCT
            case .compressedImage: return py.OUTPUT_COMPRESSED_IMAGE
            }
        }
    }
    
    private var outputState: OutputState {
        get { return OutputState(rawValue: self.outputControl.selectedSegment)! }
        set { self.outputControl.selectedSegment = newValue.rawValue }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
//        self.compressedImageWell.refusesFirstResponder = false
//        self.compressedImageWell.allowsCutCopyPaste = true
//        self.compressedImageWell.isEnabled = true
//        self.compressedImageWell.focusRingType = .exterior
        self.compressedImageWell.isEditable = true
        // FIXME: not really what I wanted
        
        self.windowSlider.minValue = 2
        self.windowSlider.value = 8
        
        self.cutOffSlider.minValue = 0
        
        self.updateInterfaceState()
    }

    private func updateInterfaceState() {
        if let size = self.originalImage?.size {
            self.windowSlider.maxValue = Int(min(size.height, size.width))
        } else {
            self.windowSlider.maxValue = 128
        }
        
        self.cutOffSlider.maxValue = 2 * self.windowSlider.value - 2
        
        self.saveButton.isEnabled = (self.compressedImage != nil)
        
        // FIXME: this is an ugly hack. how the hell should magnification filters be configured on an NSImageView?
        self.originalImageWell.subviews.first?.layer?.magnificationFilter = .nearest
        self.compressedImageWell.subviews.first?.layer?.magnificationFilter = .nearest
        
        self.compressedImageWell.toolTip = self.outputControl.label(forSegment: self.outputControl.selectedSegment)
    }
    
    override func keyDown(with event: NSEvent) {
        guard event.characters == " " else {
            return super.keyDown(with: event)
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
        self.updateInterfaceState()
        self.updateCompressedImage()
    }
    
    @IBAction func userDidDropImage(_ sender: NSImageView) {
        self.updateInterfaceState()
        self.updateCompressedImage()
    }
    
    @IBAction func open(_ sender: NSButton) {
        let panel = NSOpenPanel()
        
        panel.allowedFileTypes = [kUTTypeImage as String]
        
        panel.beginSheetModal(for: self.view.window!) { response in
            if response == .OK {
                let image = NSImage(contentsOf: panel.url!)

                self.originalImage = image
                self.updateCompressedImage()
            }
        }
    }
    
    @IBAction func runBenchmark(_ sender: NSButton) {
        self.statusLabel.stringValue = "Ready…"
        
        guard let image = self.originalImage else {
            return
        }
        
        let window = self.windowSlider.value
        let cutoff = self.cutOffSlider.value
        let output = self.outputState
        
        self.statusLabel.stringValue = "Running benchmark…"
        
        DispatchQueue.main.async {
            do {
                let samples = try benchmark {
                    _ = try self.generateCompressedImage(from: image, window: window, cutoff: cutoff, output: output)
                }
                
                summary(samples: samples)
                
                self.statusLabel.stringValue = "Benchmark completed."
            } catch {
                self.statusLabel.stringValue = "ERROR: \(error.localizedDescription)"
            }
        }
    }
    
    @IBAction func save(_ sender: NSButton) {
        guard let image = self.compressedImage else {
            return
        }
        
        let panel = NSSavePanel()
        
        panel.allowedFileTypes = [kUTTypeTIFF as String]
        
        panel.beginSheetModal(for: self.view.window!) { response in
            if response == .OK {
                guard let data = image.tiffRepresentation(using: .lzw, factor: 0.0) else {
                    self.statusLabel.stringValue = "ERROR: Unable to create image file."
                    return
                }
                
                do {
                    try data.write(to: panel.url!)
                } catch {
                    self.statusLabel.stringValue = "ERROR: \(error.localizedDescription)"
                    return
                }
            }
        }
    }
    
    func validateMenuItem(_ item: NSMenuItem) -> Bool {
        switch item.action {
        case #selector(save):
            return self.saveButton.isEnabled
            
        default:
            return true
        }
    }
    
    // MARK: - Process updates
    
    func updateCompressedImage() {
        self.statusLabel.stringValue = "Ready…"
        
        guard let image = self.originalImage else {
            return
        }
        
        let window = self.windowSlider.value
        let cutoff = self.cutOffSlider.value
        let output = self.outputState
        
        self.statusLabel.stringValue = "Processing…"
        
        // Defer to next runloop cycle to update the status label.
        DispatchQueue.main.async {
            var compressedImage: NSImage?
            var status: String?
            
            do {
                let time = try measure {
                    compressedImage = try self.generateCompressedImage(from: image, window: window, cutoff: cutoff, output: output)
                }
                
                status = String(format: "Image has been processed in %.3lf ms.", time)
            } catch {
                status = "ERROR: \(error.localizedDescription)"
                print(error)
            }
            
            self.compressedImage = compressedImage
            self.statusLabel.stringValue = status!
        }
    }
    
    private func generateCompressedImage(from image: NSImage, window: Int, cutoff: Int, output: OutputState) throws -> NSImage {
        guard let imageArray = image.makeNumpyArray() else {
            throw NSError(domain: "FtlFT", code: 1, userInfo: [
                NSLocalizedDescriptionKey: "The format of the input image is not supported."
            ])
        }
        
        let compressed = try py.compress_image.throwing(imageArray, window: window, cutoff: cutoff, output: output)
        
        guard let compressedImage = NSImage(numpy: compressed) else {
            throw NSError(domain: "FtlFT", code: 2, userInfo: [
                NSLocalizedDescriptionKey: "Couldn't process output image."
            ])
        }
        
        return compressedImage
    }
}
