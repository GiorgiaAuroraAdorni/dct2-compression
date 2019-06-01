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
    @IBOutlet weak var minLabel: NSTextField!
    @IBOutlet weak var maxLabel: NSTextField!
    
    @IBOutlet weak var textField: NSTextField!
    @IBOutlet weak var stepper: NSStepper!
    
    var value: Double = 0 {
        didSet {
            slider.doubleValue = value
            textField.doubleValue = value
            stepper.doubleValue = value
        }
    }
    
    var minValue: Double = 0 {
        didSet {
            slider.minValue = minValue
            stepper.minValue = minValue
            minLabel.doubleValue = minValue
        }
    }
    
    var maxValue: Double = 50 {
        didSet {
            slider.maxValue = maxValue
            maxLabel.doubleValue = maxValue
            stepper.maxValue = maxValue
        }
    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        
        self.value = (self.value) as Double
        self.minValue = (self.minValue) as Double
        self.maxValue = (self.maxValue) as Double
    }
    
    @IBAction func userDidUpdate(_ sender: NSControl) {
        self.value = round(sender.doubleValue)
    }
    
    
}
