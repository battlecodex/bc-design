# BC Design System for SwiftUI

Native implementation for **iOS 17+ and macOS Sonoma+** using SwiftUI.

---

## 1. Design Tokens Extension (`BCDesignTokens.swift`)

```swift
import SwiftUI

public extension Color {
    // Canvas & Surfaces
    static let bcBgLight = Color(hex: "FAF9F5")
    static let bcBgDark = Color(hex: "181816")
    static let bcSurfaceLight = Color(hex: "FFFFFF")
    static let bcSurfaceDark = Color(hex: "242421")
    
    // Terracotta Brand Accent
    static let bcTerracotta = Color(hex: "D97757")
    static let bcTerracottaDark = Color(hex: "C15F3E")
    
    // Ink & Text
    static let bcInk = Color(hex: "1F1E1B")
    static let bcMuted = Color(hex: "6B6760")
    
    // Dynamic Adaptive Colors
    static let bcBg = Color(uiColor: UIColor { traits in
        traits.userInterfaceStyle == .dark ? UIColor(Color.bcBgDark) : UIColor(Color.bcBgLight)
    })
    
    static let bcSurface = Color(uiColor: UIColor { traits in
        traits.userInterfaceStyle == .dark ? UIColor(Color.bcSurfaceDark) : UIColor(Color.bcSurfaceLight)
    })
}

// Hex Color Initializer
extension Color {
    init(hex: String) {
        let scanner = Scanner(string: hex)
        var rgbValue: UInt64 = 0
        scanner.scanHexInt64(&rgbValue)
        let r = Double((rgbValue & 0xFF0000) >> 16) / 255.0
        let g = Double((rgbValue & 0x00FF00) >> 8) / 255.0
        let b = Double(rgbValue & 0x0000FF) / 255.0
        self.init(red: r, green: g, blue: b)
    }
}
```

---

## 2. Typography & ViewModifiers (`BCDesignCard.swift`)

```swift
import SwiftUI

public struct BCDesignCardModifier: ViewModifier {
    @Environment(\.colorScheme) var colorScheme
    
    public func body(content: Content) -> some View {
        content
            .padding(20)
            .background(Color.bcSurface)
            .cornerRadius(16)
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(colorScheme == .dark ? Color.white.opacity(0.08) : Color.black.opacity(0.08), lineWidth: 1)
            )
            .shadow(color: Color.black.opacity(colorScheme == .dark ? 0.4 : 0.04), radius: 8, x: 0, y: 3)
    }
}

public extension View {
    func bcCard() -> some View {
        self.modifier(BCDesignCardModifier())
    }
}
```

---

## 3. Signature BC Design Thinking Pulse (SwiftUI)

```swift
import SwiftUI

public struct BCDesignThinkingView: View {
    @State private var isPulsing = false
    
    public var body: some View {
        HStack(spacing: 8) {
            Circle()
                .fill(Color.bcTerracotta)
                .frame(width: 8, height: 8)
                .scaleEffect(isPulsing ? 1.2 : 0.8)
                .opacity(isPulsing ? 1.0 : 0.4)
            
            Text("BC Design is thinking...")
                .font(.system(size: 13, weight: .medium))
                .foregroundColor(Color.bcTerracotta)
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 6)
        .background(Color.bcTerracotta.opacity(0.12))
        .clipShape(Capsule())
        .onAppear {
            withAnimation(
                .easeInOut(duration: 1.2)
                .repeatForever(autoreverses: true)
            ) {
                isPulsing = true
            }
        }
    }
}
```
