//
//  PreciseSliderView.swift
//  FasterThanLightFourierTransform
//
//  Created by Giorgia Adorni on 01/06/2019.
//  Copyright © 2019 Giorgia e Elia. All rights reserved.
//

import Cocoa

class PreciseSliderView: NSView {

    @IBOutlet weak var slider: NSSlider!
    @IBOutlet weak var minimumLabel: NSTextField!
    @IBOutlet weak var maximumLabel: NSTextField!
    
    @IBOutlet weak var textField: NSTextField!
    @IBOutlet weak var stepper: NSStepper!
    
    var value: Double = 50 {
        didSet {
            slider.doubleValue = value
            textField.doubleValue = value
            stepper.doubleValue = value
        }
    }
    
    
    /*
    override func awakeFromNib() {
        super.awakeFromNib()
        
        let a = self.value
        self.value = a
    }
    */
    
    @IBAction func userDidUpdate(_ sender: NSControl) {
        self.value = sender.doubleValue
    }
    
    
}
