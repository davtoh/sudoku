"""Game configuration, constants, themes, and difficulty definitions."""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Dict

ColorType = Tuple[int, int, int]
ColorAlphaType = Tuple[int, int, int, int]

class KeypadPlacement(Enum):
    AUTO = "auto"
    BOTTOM = "bottom"
    RIGHT = "right"

class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    EXPERT = "Expert"

# Number of cells to remove per difficulty
DIFFICULTY_EMPTIES: Dict[Difficulty, int] = {
    Difficulty.EASY: 32,      # 49 given clues
    Difficulty.MEDIUM: 42,    # 39 given clues
    Difficulty.HARD: 50,      # 31 given clues
    Difficulty.EXPERT: 56,    # 25 given clues
}

@dataclass(frozen=True)
class Theme:
    name: str
    bg_primary: ColorType
    bg_secondary: ColorType
    bg_board: ColorType
    bg_card: ColorType
    
    # Grid lines
    grid_thin: ColorType
    grid_thick: ColorType
    
    # Cells
    cell_given: ColorType
    cell_user: ColorType
    cell_error: ColorType
    cell_note: ColorType
    
    # Highlights
    highlight_selected: ColorAlphaType
    highlight_related: ColorAlphaType
    highlight_same_number: ColorAlphaType
    highlight_error: ColorAlphaType
    
    # UI & Keypad
    btn_bg: ColorType
    btn_hover: ColorType
    btn_active: ColorType
    btn_text: ColorType
    btn_border: ColorType
    btn_action_bg: ColorType
    btn_action_active: ColorType
    
    # Text
    text_primary: ColorType
    text_secondary: ColorType
    text_accent: ColorType

LIGHT_THEME = Theme(
    name="light",
    bg_primary=(245, 247, 250),
    bg_secondary=(232, 236, 241),
    bg_board=(255, 255, 255),
    bg_card=(255, 255, 255),
    
    grid_thin=(209, 213, 219),
    grid_thick=(55, 65, 81),
    
    cell_given=(17, 24, 39),
    cell_user=(37, 99, 235),        # Vibrant blue for correct/active user entry
    cell_error=(220, 38, 38),       # Red for conflicting numbers
    cell_note=(107, 114, 128),      # Muted gray for pencil marks
    
    highlight_selected=(59, 130, 246, 90),     # Semi-transparent blue
    highlight_related=(219, 234, 254, 120),    # Soft blue for row/col/block
    highlight_same_number=(191, 219, 254, 160), # Medium blue for matching digits
    highlight_error=(254, 202, 202, 140),      # Soft red
    
    btn_bg=(243, 244, 246),
    btn_hover=(229, 231, 235),
    btn_active=(209, 213, 219),
    btn_text=(31, 41, 55),
    btn_border=(209, 213, 219),
    btn_action_bg=(224, 231, 255),
    btn_action_active=(199, 210, 254),
    
    text_primary=(17, 24, 39),
    text_secondary=(107, 114, 128),
    text_accent=(37, 99, 235),
)

DARK_THEME = Theme(
    name="dark",
    bg_primary=(17, 24, 39),
    bg_secondary=(31, 41, 55),
    bg_board=(24, 32, 47),
    bg_card=(31, 41, 55),
    
    grid_thin=(55, 65, 81),
    grid_thick=(156, 163, 175),
    
    cell_given=(243, 244, 246),
    cell_user=(96, 165, 250),
    cell_error=(248, 113, 113),
    cell_note=(156, 163, 175),
    
    highlight_selected=(59, 130, 246, 110),
    highlight_related=(30, 58, 138, 70),
    highlight_same_number=(30, 64, 175, 100),
    highlight_error=(127, 29, 29, 90),
    
    btn_bg=(31, 41, 55),
    btn_hover=(55, 65, 81),
    btn_active=(75, 85, 99),
    btn_text=(243, 244, 246),
    btn_border=(75, 85, 99),
    btn_action_bg=(49, 46, 129),
    btn_action_active=(67, 56, 202),
    
    text_primary=(243, 244, 246),
    text_secondary=(156, 163, 175),
    text_accent=(96, 165, 250),
)

DEFAULT_THEME = LIGHT_THEME

# Grid constants
GRID_SIZE = 9
BOX_SIZE = 3

# Target FPS
FPS = 60

