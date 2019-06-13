//
//  SliderView.swift
//  FasterThanLightFourierTransform
//
//  Created by Giorgia Adorni on 01/06/2019.
//  Copyright © 2019 Giorgia e Elia. All rights reserved.
//

import Cocoa

class SliderView: NSControl {

    @IBOutlet weak var slider: NSSlider!
    @IBOutlet weak var minLabel: NSTextField!
    @IBOutlet weak var maxLabel: NSTextField!
    
    @IBOutlet weak var textField: NSTextField!
    @IBOutlet weak var stepper: NSStepper!
    
    var value: Int = 0 {
        didSet {
            value = max(minValue, min(value, maxValue))
            
            slider.integerValue = value
            textField.integerValue = value
            stepper.integerValue = value
        }
    }
    
    var minValue: Int = 0 {
        didSet {
            slider.minValue = Double(minValue)
            stepper.minValue = Double(minValue)
            minLabel.integerValue = minValue
            
            // Ensure that value is correctly clipped
            value = (value) as Int
        }
    }
    
    var maxValue: Int = 50 {
        didSet {
            slider.maxValue = Double(maxValue)
            stepper.maxValue = Double(maxValue)
            maxLabel.integerValue = maxValue
            
            // Ensure that value is correctly clipped
            value = (value) as Int
        }
    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        
        value = (value) as Int
        minValue = (minValue) as Int
        maxValue = (maxValue) as Int
    }
    
    @IBAction func userDidUpdate(_ sender: NSControl) {
        value = sender.integerValue
        
        self.sendAction(self.action, to: self.target)
    }
    
    
}
