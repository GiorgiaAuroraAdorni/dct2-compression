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
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        // Python:
        //    import numpy as np
        //    a = np.arange(15).reshape(3, 5)
        //    b = np.array([6, 7, 8])
        let np = Python.import("numpy")
        let a = np.arange(15).reshape(3, 5)
        let b = np.array([6, 7, 8])
        
        //    // Python:
        //    //    import gzip as gzip
        //    //    import pickle as pickle
        //    let gzip = Python.import("gzip")
        //    let pickle = Python.import("pickle")
        //
        //    // Python:
        //    //    file = gzip.open("mnist.pkl.gz", "rb")
        //    //    (images, labels) = pickle.load(file)
        //    //    print(images.shape) // (50000, 784)
        //    let file = gzip.open("mnist.pkl.gz", "rb")
        //    let (images, labels) = pickle.load(file).tuple2
        //    print(images.shape) // (50000, 784)
        //
    }

    @IBAction func userDidDropImage(_ sender: NSImageView) {
        DispatchQueue.main.async {
            let a = sender.image!.makeNumpyArray()
            
            let plt = Python.import("matplotlib.pyplot")
            
            plt.imshow(a)
            plt.show()
        }
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

