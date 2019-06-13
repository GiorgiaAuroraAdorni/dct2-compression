//
//  Performance.swift
//  FasterThanLightFourierTransform
//
//  Created by Elia Cereda on 13/06/2019.
//  Copyright © 2019 Giorgia e Elia. All rights reserved.
//

import Foundation

func measure(block: () throws -> ()) rethrows -> Double {
    let start = DispatchTime.now()
    try block()
    let end = DispatchTime.now()
    
    return Double(end.uptimeNanoseconds - start.uptimeNanoseconds) / 1000_000
}

func benchmark(n: Int = 50, block: () -> ()) -> [Double] {
    var samples = [Double]()
    
    samples.reserveCapacity(n)
    
    for _ in 0..<n {
        let time = measure(block: block)
        
        samples.append(time)
    }
    
    return samples
}

func summary(samples: [Double]) {
    var sum: Double = 0.0
    var sumSquared: Double = 0.0
    
    for sample in samples {
        sum += sample
        sumSquared += sample * sample
    }
    
    let n = Double(samples.count)
    let mean = sum / n
    let variance = sumSquared / n - mean * mean
    let stdev = sqrt(variance)
    
    let plt = Python.import("matplotlib.pyplot")
    
    let title = "Execution times over \(n) samples: mean \(mean) ms, stdev \(stdev) ms"
    
    // Enable interactive mode
    plt.ion()
    
    plt.figure(1)
    plt.clf()
    
    plt.suptitle(title)
    
    plt.subplot(1, 2, 1)
    plt.plot(samples)
    
    plt.subplot(1, 2, 2)
    plt.hist(samples)
}
