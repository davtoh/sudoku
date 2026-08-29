"""Unit tests for responsive LayoutManager and keypad placement."""

import unittest
from src.config import KeypadPlacement
from src.ui.layout import LayoutManager


class TestLayoutManager(unittest.TestCase):
    def setUp(self):
        self.layout_mgr = LayoutManager()

    def test_auto_resolution(self):
        # Portrait resolution should resolve to BOTTOM
        self.assertEqual(
            self.layout_mgr.resolve_placement(360, 640), KeypadPlacement.BOTTOM
        )
        self.assertEqual(
            self.layout_mgr.resolve_placement(720, 1280), KeypadPlacement.BOTTOM
        )

        # Landscape resolution should resolve to RIGHT
        self.assertEqual(
            self.layout_mgr.resolve_placement(1280, 720), KeypadPlacement.RIGHT
        )
        self.assertEqual(
            self.layout_mgr.resolve_placement(1920, 1080), KeypadPlacement.RIGHT
        )

    def test_portrait_layout_bounds(self):
        # Test mobile vertical screen
        w, h = 360, 640
        metrics = self.layout_mgr.calculate(w, h)

        self.assertEqual(metrics.placement, KeypadPlacement.BOTTOM)
        # Board fits within screen width and height
        self.assertGreaterEqual(metrics.board_rect.left, 0)
        self.assertLessEqual(metrics.board_rect.right, w)
        self.assertGreater(metrics.board_rect.top, metrics.header_rect.top)
        self.assertLess(metrics.board_rect.bottom, metrics.keypad_rect.top)

        # Keypad fits within screen
        self.assertGreaterEqual(metrics.keypad_rect.left, 0)
        self.assertLessEqual(metrics.keypad_rect.right, w)
        self.assertLessEqual(metrics.keypad_rect.bottom, h)

        # Check all keypad buttons fit inside keypad_rect
        for b_geo in metrics.keypad_buttons:
            self.assertTrue(metrics.keypad_rect.contains(b_geo.rect), f"Button {b_geo.id} outside keypad rect")

    def test_landscape_layout_bounds(self):
        # Test desktop / landscape tablet screen
        w, h = 1280, 720
        self.layout_mgr.set_placement(KeypadPlacement.RIGHT)
        metrics = self.layout_mgr.calculate(w, h)

        self.assertEqual(metrics.placement, KeypadPlacement.RIGHT)
        # Board fits on left
        self.assertGreaterEqual(metrics.board_rect.left, 0)
        self.assertLess(metrics.board_rect.right, metrics.keypad_rect.left)

        # Keypad is on the right and fits within screen
        self.assertGreater(metrics.keypad_rect.left, metrics.board_rect.right)
        self.assertLessEqual(metrics.keypad_rect.right, w)
        self.assertLessEqual(metrics.keypad_rect.bottom, h)

        # Check buttons fit inside keypad_rect
        for b_geo in metrics.keypad_buttons:
            self.assertTrue(metrics.keypad_rect.contains(b_geo.rect), f"Button {b_geo.id} outside keypad rect")

    def test_custom_forced_placement(self):
        # Force bottom placement on landscape resolution
        self.layout_mgr.set_placement(KeypadPlacement.BOTTOM)
        metrics = self.layout_mgr.calculate(1024, 768)
        self.assertEqual(metrics.placement, KeypadPlacement.BOTTOM)
        self.assertLess(metrics.board_rect.bottom, metrics.keypad_rect.top)

        # Force right placement on portrait resolution
        self.layout_mgr.set_placement(KeypadPlacement.RIGHT)
        metrics = self.layout_mgr.calculate(400, 800)
        self.assertEqual(metrics.placement, KeypadPlacement.RIGHT)
        self.assertLess(metrics.board_rect.right, metrics.keypad_rect.left)


if __name__ == "__main__":
    unittest.main()

