"""Unit tests for responsive LayoutManager, keypad placement, and free positioning."""

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

    def test_small_phone_portrait_bounds(self):
        # Test very small screen (320x480)
        w, h = 320, 480
        metrics = self.layout_mgr.calculate(w, h)

        self.assertEqual(metrics.placement, KeypadPlacement.BOTTOM)
        self.assertGreaterEqual(metrics.board_rect.left, 0)
        self.assertLessEqual(metrics.board_rect.right, w)
        self.assertLessEqual(metrics.keypad_rect.bottom, h)

        for b_geo in metrics.keypad_buttons:
            self.assertTrue(metrics.keypad_rect.contains(b_geo.rect), f"Button {b_geo.id} outside keypad rect on small screen")

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

    def test_element_repositioning_offsets(self):
        # Test applying custom offsets
        w, h = 400, 800
        initial_metrics = self.layout_mgr.calculate(w, h)

        self.layout_mgr.adjust_board_offset(15, -20)
        self.layout_mgr.adjust_keypad_offset(-10, 25)
        offset_metrics = self.layout_mgr.calculate(w, h)

        self.assertEqual(offset_metrics.board_rect.x, initial_metrics.board_rect.x + 15)
        self.assertEqual(offset_metrics.board_rect.y, initial_metrics.board_rect.y - 20)
        self.assertEqual(offset_metrics.keypad_rect.x, initial_metrics.keypad_rect.x - 10)
        self.assertEqual(offset_metrics.keypad_rect.y, initial_metrics.keypad_rect.y + 25)
        self.assertTrue(self.layout_mgr.has_custom_offsets)

        # Test reset
        self.layout_mgr.reset_offsets()
        reset_metrics = self.layout_mgr.calculate(w, h)
        self.assertEqual(reset_metrics.board_rect.x, initial_metrics.board_rect.x)
        self.assertEqual(reset_metrics.board_rect.y, initial_metrics.board_rect.y)
        self.assertFalse(self.layout_mgr.has_custom_offsets)


if __name__ == "__main__":
    unittest.main()
