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
        let bitsPerSample: Int
        let byteOrder: CGImageByteOrderInfo
        
        switch numpyArray.dtype {
        case ctypes.c_uint8:
            bitsPerSample = 8
            byteOrder = .orderDefault
        case ctypes.c_uint16:
            bitsPerSample = 16
            byteOrder = .order16Little
            
        default:
            print("Unsupported dtype: \(numpyArray.dtype)")
            return nil
        }
        
        // Extract the shape of the `ndarray`.
        guard let shape = [Int](numpyArray.shape) else {
            return nil
        }
        
        let height: Int
        let width: Int
        let channels: Int
        
        switch shape.count {
        case 2:
            height   = shape[0]
            width    = shape[1]
            channels = 1
            
        case 3:
            height   = shape[0]
            width    = shape[1]
            channels = shape[2]
            
        default:
            return nil
        }
        
        // Compute properties
        let bitsPerPixel = bitsPerSample * channels
        let bytesPerRow = (bitsPerPixel / 8) * width
        
        let colorSpace = (channels == 1) ? CGColorSpace(name: CGColorSpace.genericGrayGamma2_2)! : CGColorSpace(name: CGColorSpace.sRGB)!
        let alphaInfo: CGImageAlphaInfo = (channels == 4) ? .last : .none
        let intent = CGColorRenderingIntent.defaultIntent
        
        let bitmapInfo: CGBitmapInfo = [
            CGBitmapInfo(rawValue: byteOrder.rawValue),
            CGBitmapInfo(rawValue: alphaInfo.rawValue)
        ]
        
        // Copy the image data
        let contiguous = np.ascontiguousarray(numpyArray)
        
        guard let dataValue = UInt(contiguous.__array_interface__["data"][0]) else {
            return nil
        }
        
        guard let dataPtr = UnsafeRawPointer(bitPattern: dataValue) else {
            return nil
        }
        
        let data = Data(bytes: dataPtr, count: width * height * (bitsPerPixel / 8))
        
        // Create image
        guard let dataProvider = CGDataProvider(data: data as CFData) else {
            return nil
        }
        
        guard let cgImage = CGImage(width: width, height: height,
                              bitsPerComponent: bitsPerSample, bitsPerPixel: bitsPerPixel, bytesPerRow: bytesPerRow,
                              space: colorSpace, bitmapInfo: bitmapInfo,
                              provider: dataProvider, decode: nil, shouldInterpolate: true, intent: intent) else {
            return nil
        }
        
        self.init(cgImage: cgImage, size: NSSize(width: width, height: height))
    }
    
    /// Creates a `numpy.ndarray` instance with the bitmap of this `NSImage`.
    ///
    /// - Precondition: The `numpy` Python package must be installed.
    func makeNumpyArray() -> PythonObject? {
        var bitmapRep: NSBitmapImageRep! = nil
        
        for rep in representations {
            if let castedRep = rep as? NSBitmapImageRep {
                bitmapRep = castedRep
                break
            }
        }
        
        guard bitmapRep != nil else {
            return nil
        }
        
        guard !bitmapRep.isPlanar else {
            // Not implemented
            return nil
        }
        
        let height = bitmapRep.pixelsHigh
        let width = bitmapRep.pixelsWide
        let channels = bitmapRep.bitsPerPixel / bitmapRep.bitsPerSample
        
        let bytes = bitmapRep.bitmapData!
        let shape = [height, width, channels]
        let ctype: PythonObject
        
        switch bitmapRep.bitsPerSample {
        case 8:
            ctype = ctypes.c_uint8
        case 16:
            ctype = ctypes.c_uint16
            
        default:
            return nil
        }
        
        let data = ctypes.cast(Int(bitPattern: bytes), ctypes.POINTER(ctype))
        let ndarray = np.ctypeslib.as_array(data, shape: PythonObject(tupleContentsOf: shape))
        
        return np.copy(ndarray)
    }
}
