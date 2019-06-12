//
//  AppDelegate.swift
//  FasterThanLightFourierTransform
//
//  Created by Giorgia Adorni on 01/06/2019.
//  Copyright © 2019 Giorgia e Elia. All rights reserved.
//

import Cocoa

@NSApplicationMain
class AppDelegate: NSObject, NSApplicationDelegate {

    override init() {
        // Force the bridging code to load Python 3
        PythonLibrary.useVersion(3)
        
        let sys = Python.import("sys")
        let pythonSources = Bundle.main.path(forResource: "src", ofType: nil)
        
        // Append the src/ folder to PYTHONPATH to be able to import it
        sys.path.insert(0, pythonSources)
    }
    
    func applicationDidFinishLaunching(_ aNotification: Notification) {
        // Insert code here to initialize your application
    }

    func applicationWillTerminate(_ aNotification: Notification) {
        // Insert code here to tear down your application
    }


}

