//
//  NSImage+Python.swift
//  FasterThanLightFourierTransform
//
//  Created by Elia Cereda on 03/06/2019.
//  Copyright © 2019 Giorgia e Elia. All rights reserved.
//

import AppKit

/// The `numpy` Python module.
/// Note: Global variables are lazy, so the following declaration won't produce
/// a Python import error until it is first used.
private let np = Python.import("numpy")
private let ctypes = Python.import("ctypes")

extension NSImage {
    
    /// Creates a `numpy.ndarray` instance with the bitmap of this `NSImage`.
    ///
    /// - Precondition: The `numpy` Python package must be installed.
    func makeNumpyArray() -> PythonObject {
        var bitmapRep: NSBitmapImageRep! = nil
        
        for rep in representations {
            if let castedRep = rep as? NSBitmapImageRep {
                bitmapRep = castedRep
                break
            }
        }
        
        guard bitmapRep != nil else {
            preconditionFailure("This NSImage is not supported")
        }
        
        let height = bitmapRep.pixelsHigh
        let width = bitmapRep.pixelsWide
        let channels = bitmapRep.bitsPerPixel / bitmapRep.bitsPerSample
        
        let bytes = bitmapRep.bitmapData!
        let shape = [height, width, channels]
        let ctype = ctypes.c_uint8
        
        let data = ctypes.cast(Int(bitPattern: bytes), ctypes.POINTER(ctype))
        let ndarray = np.ctypeslib.as_array(data, shape: PythonObject(tupleContentsOf: shape))
        
        return np.copy(ndarray)
    }
}
