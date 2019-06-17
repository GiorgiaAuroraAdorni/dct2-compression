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

func benchmark(n: Int = 50, block: () throws -> ()) rethrows -> [Double] {
    var samples = [Double]()
    
    samples.reserveCapacity(n)
    
    for _ in 0..<n {
        let time = try measure(block: block)
        
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
    
    let title = String(format: """
        Execution times over %d samples:
        mean %.3lf ms, stdev %.3lf ms
    """, samples.count, mean, stdev)
        
    plt.figure(1)
    plt.clf()
    
    plt.suptitle(title)
    
    plt.subplot(1, 2, 1)
    plt.plot(samples)
    plt.ylim(0)
    plt.title("Plot")
    plt.xlabel("Samples")
    plt.ylabel("Time (ms)")
    
    plt.subplot(1, 2, 2)
    plt.hist(samples)
    plt.title("Histogram")
    plt.xlabel("Time (ms)")
    plt.ylabel("Count")
    
    plt.tight_layout(rect: [0, 0.03, 1, 0.92])
}
