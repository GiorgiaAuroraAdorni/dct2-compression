//
//  ViewController.swift
//  FasterThanLightFourierTransform
//
//  Created by Giorgia Adorni on 01/06/2019.
//  Copyright © 2019 Giorgia e Elia. All rights reserved.
//

import Cocoa

class ViewController: NSViewController {

    @IBOutlet weak var originalImageWell: NSImageView!
    @IBOutlet weak var compressedImageWell: NSImageView!
    
    @IBOutlet weak var windowSlider: PreciseSliderView!
    @IBOutlet weak var cutOffSlider: PreciseSliderView!
    
    private let py = Python.import("main")
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    @IBAction func userDidDropImage(_ sender: NSImageView) {
        py.main()
        
//        DispatchQueue.main.async {
//            let a = sender.image!.makeNumpyArray()
//            
//            let plt = Python.import("matplotlib.pyplot")
//            
//            plt.imshow(a)
//            plt.show()
//        }
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
            }
        }
    }
    
}

