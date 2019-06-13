//
//  ImageView.swift
//  FasterThanLightFourierTransform
//
//  Created by Elia Cereda on 13/06/2019.
//  Copyright © 2019 Giorgia e Elia. All rights reserved.
//

import Cocoa
import Quartz
import AVFoundation

class ImageView: NSImageView, QLPreviewPanelDataSource, QLPreviewPanelDelegate {
    
    override func becomeFirstResponder() -> Bool {
        let result = super.becomeFirstResponder()
        
        self.previewPanel?.updateController()
        
        return result
    }
    
    override func resignFirstResponder() -> Bool {
        let result = super.resignFirstResponder()
        
        self.previewPanel?.updateController()
        
        return result
    }
    
    override var image: NSImage? {
        didSet {
            self.previewPanel?.reloadData()
        }
    }
    
    // MARK: - QLPreviewPanelController
    
    private var previewPanel: QLPreviewPanel? {
        if QLPreviewPanel.sharedPreviewPanelExists() {
            return QLPreviewPanel.shared()
        } else {
            return nil
        }
    }
    
    override func acceptsPreviewPanelControl(_ panel: QLPreviewPanel!) -> Bool {
        return true
    }
    
    override func beginPreviewPanelControl(_ panel: QLPreviewPanel!) {
        panel.dataSource = self
        panel.delegate = self
    }
    
    override func endPreviewPanelControl(_ panel: QLPreviewPanel!) {
        panel.dataSource = nil
        panel.delegate = nil
    }
    
    // MARK: - QLPreviewPanelDataSource
    
    func numberOfPreviewItems(in panel: QLPreviewPanel!) -> Int {
        return (self.image != nil) ? 1 : 0
    }
    
    func previewPanel(_ panel: QLPreviewPanel!, previewItemAt index: Int) -> QLPreviewItem! {
        return ImagePreviewItem.for(self.image!, title: self.toolTip)
    }
    
    // MARK: - QLPreviewPanelDelegate
    
    func previewPanel(_ panel: QLPreviewPanel!, sourceFrameOnScreenFor item: QLPreviewItem!) -> NSRect {
        let imageFrame = AVMakeRect(aspectRatio: self.image!.size, insideRect: self.bounds)
        
        return self.window!.convertToScreen(self.convert(imageFrame, to: nil))
    }
}

class ImagePreviewItem: NSObject, QLPreviewItem {
    let previewItemURL: URL
    let previewItemTitle: String?
    
    private init?(image: NSImage, title: String?) {
        let fileURL = URL(fileURLWithPath: NSTemporaryDirectory(), isDirectory: true)
            .appendingPathComponent(UUID.init().uuidString)
            .appendingPathExtension("tiff")
        
        guard let data = image.tiffRepresentation(using: .none, factor: 0.0) else {
            return nil
        }
        
        do {
            try data.write(to: fileURL)
        } catch {
            return nil
        }
        
        self.previewItemURL = fileURL
        self.previewItemTitle = title
    }
    
    deinit {
        try? FileManager.default.removeItem(at: self.previewItemURL)
    }
    
    // MARK: - Item Cache
    
    // FIXME: does not make any sense to use an in-memory cache
    static let cache = NSCache<NSImage, ImagePreviewItem>()
    
    class func `for`(_ image: NSImage, title: String?) -> ImagePreviewItem {
        var item: ImagePreviewItem! = cache.object(forKey: image)
        
        if item == nil {
            item = ImagePreviewItem(image: image, title: title)
            
            cache.setObject(item, forKey: image)
        }
        
        return item
    }
}
