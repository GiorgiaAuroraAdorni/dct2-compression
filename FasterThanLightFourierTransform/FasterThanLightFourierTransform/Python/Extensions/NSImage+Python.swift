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
    /// Creates an `NSImage` with the same shape and scalars as the specified
    /// `numpy.ndarray` instance.
    ///
    /// - Parameter numpyArray: The `numpy.ndarray` instance to convert.
    /// - Precondition: The `numpy` Python package must be installed.
    /// - Returns: `numpyArray` converted to an `NSImage`. Returns `nil` if
    ///   `numpyArray` does not have a compatible scalar `dtype`.
    convenience init?(numpy numpyArray: PythonObject) {
        // Check if input is a `numpy.ndarray` instance.
        guard Python.isinstance(numpyArray, np.ndarray) == true else {
            return nil
        }
        
        // Check if the dtype of the `ndarray` is compatible with the type.
        guard numpyArray.dtype == ctypes.c_uint8 else {
            return nil
        }
        
        // TODO
        return nil
    }
    
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
