"""Base abstract Scene class for state management."""

from abc import ABC, abstractmethod
import pygame
from typing import Optional, TYPE_CHECKING
from ..config import Theme

if TYPE_CHECKING:
    from ..app import SudokuApp


class BaseScene(ABC):
    """Abstract interface for all game scenes (Menu, Gameplay, Settings, etc.)."""

    def __init__(self, app: "SudokuApp") -> None:
        self.app: "SudokuApp" = app

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Processes input events from the user."""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """Updates scene logic given elapsed delta time in seconds."""
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Draws the scene onto the display surface."""
        pass

    @abstractmethod
    def on_resize(self, width: int, height: int) -> None:
        """Handles screen resize and re-calculates UI geometries."""
        pass

