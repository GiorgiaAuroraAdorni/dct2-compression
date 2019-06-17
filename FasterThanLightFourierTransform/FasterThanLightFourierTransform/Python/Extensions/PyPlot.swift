//
//  PyPlot.swift
//  FasterThanLightFourierTransform
//
//  Created by Elia Cereda on 17/06/2019.
//  Copyright © 2019 Giorgia e Elia. All rights reserved.
//

private var dummyFigure: PythonObject?

let plt: PythonObject = {
    let plt = Python.import("matplotlib.pyplot")
    
    // Create and hold a reference to a figure without ever showing it on screen.
    // It prevents Matplotlib from closing the whole app when closing the last figure
    // https://github.com/matplotlib/matplotlib/blob/569204bfec35ef1532feed1752d77329f952ca76/src/_macosx.m#L1543
    dummyFigure = plt.figure(999)
    
    // Enable interactive mode
    plt.ion()
    
    return plt
}()
