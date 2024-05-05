//: A UIKit based Playground for presenting user interface
  
import UIKit
import PlaygroundSupport

class ViewController: UIViewController {
    
    let heartLayer = CAShapeLayer()

    override func viewDidLoad() {
        super.viewDidLoad()
        createHeart()
    }
    
    func createHeart() {
        let heartPath = UIBezierPath()
        let heartWidth: CGFloat = 100
        let heartHeight: CGFloat = 90
        
        heartPath.move(to: CGPoint(x: heartWidth / 2, y: heartHeight / 4))
        
        // Create the heart shape with Bezier curves
        heartPath.addCurve(to: CGPoint(x: heartWidth / 2, y: heartHeight),
                           controlPoint1: CGPoint(x: heartWidth * 1.2, y: 0),
                           controlPoint2: CGPoint(x: heartWidth, y: heartHeight / 1.3))
        
        heartPath.addCurve(to: CGPoint(x: heartWidth / 2, y: heartHeight / 4),
                           controlPoint1: CGPoint(x: 0, y: heartHeight / 1.3),
                           controlPoint2: CGPoint(x: heartWidth * -0.2, y: 0))
        
        heartLayer.path = heartPath.cgPath
        heartLayer.fillColor = UIColor.red.cgColor
        heartLayer.position = CGPoint(x: view.bounds.midX - heartWidth / 2, y: view.bounds.midY - heartHeight / 2)
        view.layer.addSublayer(heartLayer)
    }
    
    func animateHeart(rate: Double) {
        let animation = CABasicAnimation(keyPath: "transform.scale")
        animation.toValue = 1.1
        animation.duration = 60 / rate / 2 // duration based on heart rate (beats per minute)
        animation.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)
        animation.autoreverses = true
        animation.repeatCount = .infinity
        
        heartLayer.add(animation, forKey: "pulse")
    }
}

// Present the view controller in the Live View window
PlaygroundPage.current.liveView = ViewController()
