import 'package:flutter/services.dart';

/// Safe cross-platform haptic feedback utility.
class HapticUtil {
  static bool enabled = true;

  static void light() {
    if (!enabled) return;
    try {
      HapticFeedback.lightImpact();
    } catch (_) {}
  }

  static void selection() {
    if (!enabled) return;
    try {
      HapticFeedback.selectionClick();
    } catch (_) {}
  }

  static void medium() {
    if (!enabled) return;
    try {
      HapticFeedback.mediumImpact();
    } catch (_) {}
  }

  static void heavy() {
    if (!enabled) return;
    try {
      HapticFeedback.heavyImpact();
    } catch (_) {}
  }

  static void error() {
    if (!enabled) return;
    try {
      HapticFeedback.vibrate();
    } catch (_) {}
  }
}
