# BC Design System for Flutter

Implementation guide for **Flutter 3.x** using Material 3 and Google Fonts.

---

## 1. Theme Configuration (`bc_theme.dart`)

```dart
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class BCDesignTheme {
  // Light Palette
  static const Color bgLight = Color(0xFFFAF9F5);
  static const Color surfaceLight = Color(0xFFFFFFFF);
  static const Color textLight = Color(0xFF1F1E1B);
  static const Color mutedLight = Color(0xFF6B6760);
  
  // Dark Palette
  static const Color bgDark = Color(0xFF181816);
  static const Color surfaceDark = Color(0xFF242421);
  static const Color textDark = Color(0xFFFAF9F5);
  static const Color mutedDark = Color(0xFFA39E93);

  // Terracotta Accent
  static const Color terracotta = Color(0xFFD97757);

  static ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    scaffoldBackgroundColor: bgLight,
    colorScheme: const ColorScheme.light(
      primary: terracotta,
      surface: surfaceLight,
      onSurface: textLight,
    ),
    textTheme: TextTheme(
      headlineLarge: GoogleFonts.newsreader(fontSize: 36, fontWeight: FontWeight.w500, color: textLight),
      headlineMedium: GoogleFonts.newsreader(fontSize: 26, fontWeight: FontWeight.w500, color: textLight),
      bodyLarge: GoogleFonts.inter(fontSize: 16, color: textLight),
      bodyMedium: GoogleFonts.inter(fontSize: 14, color: mutedLight),
    ),
  );

  static ThemeData darkTheme = ThemeData(
    useMaterial3: true,
    scaffoldBackgroundColor: bgDark,
    colorScheme: const ColorScheme.dark(
      primary: terracotta,
      surface: surfaceDark,
      onSurface: textDark,
    ),
    textTheme: TextTheme(
      headlineLarge: GoogleFonts.newsreader(fontSize: 36, fontWeight: FontWeight.w500, color: textDark),
      headlineMedium: GoogleFonts.newsreader(fontSize: 26, fontWeight: FontWeight.w500, color: textDark),
      bodyLarge: GoogleFonts.inter(fontSize: 16, color: textDark),
      bodyMedium: GoogleFonts.inter(fontSize: 14, color: mutedDark),
    ),
  );
}
```

---

## 2. Reusable BC Design Card Widget (`bc_card.dart`)

```dart
import 'package:flutter/material.dart';

class BCDesignCard extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;

  const BCDesignCard({Key? key, required this.child, this.onTap}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surface,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: isDark ? Colors.white.withOpacity(0.08) : Colors.black.withOpacity(0.08),
            width: 1,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(isDark ? 0.35 : 0.04),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: child,
      ),
    );
  }
}
```
