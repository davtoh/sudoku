"""Reusable UI components and widgets with smooth styling and event handling."""

import pygame
from typing import Optional, Tuple, Callable
from ..config import Theme, ColorType


class FontCache:
    """Caches SysFont instances by size to optimize rendering."""
    _cache = {}

    @classmethod
    def get_font(cls, size: int, bold: bool = False) -> pygame.font.Font:
        key = (size, bold)
        if key not in cls._cache:
            cls._cache[key] = pygame.font.SysFont(None, size, bold=bold)
        return cls._cache[key]


class Button:
    """Clickable and touchable button with hover, active, and toggle states."""

    def __init__(
        self,
        rect: pygame.Rect,
        label: str,
        id: str = "",
        subtext: str = "",
        is_action: bool = False,
        border_radius: int = 8,
        on_click: Optional[Callable[[], None]] = None
    ) -> None:
        self.rect: pygame.Rect = rect
        self.label: str = label
        self.id: str = id or label
        self.subtext: str = subtext
        self.is_action: bool = is_action
        self.border_radius: int = border_radius
        self.on_click: Optional[Callable[[], None]] = on_click
        
        self.is_hovered: bool = False
        self.is_pressed: bool = False
        self.is_active: bool = False   # For toggle buttons like Notes mode
        self.is_disabled: bool = False

    def update_geometry(self, rect: pygame.Rect) -> None:
        """Updates button bounding rectangle."""
        self.rect = rect

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Processes mouse/touch events. Returns True if button was triggered."""
        if self.is_disabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                if self.on_click:
                    self.on_click()
                return True
            self.is_pressed = False

        return False

    def render(self, surface: pygame.Surface, theme: Theme, font_size: int = 24) -> None:
        """Renders the button onto surface."""
        # Determine background color based on state
        if self.is_disabled:
            bg_color = theme.bg_secondary
            text_color = theme.text_secondary
            border_color = theme.btn_border
        elif self.is_active:
            bg_color = theme.btn_action_active if self.is_action else theme.btn_active
            text_color = theme.cell_user
            border_color = theme.cell_user
        elif self.is_pressed:
            bg_color = theme.btn_active
            text_color = theme.text_primary
            border_color = theme.text_secondary
        elif self.is_hovered:
            bg_color = theme.btn_hover
            text_color = theme.text_primary
            border_color = theme.text_secondary
        else:
            bg_color = theme.btn_action_bg if self.is_action else theme.btn_bg
            text_color = theme.text_accent if self.is_action else theme.btn_text
            border_color = theme.btn_border

        # Draw button surface
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=self.border_radius)
        border_width = 2 if (self.is_active or self.is_hovered) else 1
        pygame.draw.rect(surface, border_color, self.rect, width=border_width, border_radius=self.border_radius)

        # Draw label
        font = FontCache.get_font(font_size, bold=self.is_action or self.is_active)
        text_surf = font.render(self.label, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # If subtext exists (e.g. keyboard shortcut or icon), offset slightly
        if self.subtext:
            text_rect.centery = self.rect.centery - font_size // 6
            surface.blit(text_surf, text_rect)
            
            sub_font = FontCache.get_font(max(10, int(font_size * 0.55)))
            sub_surf = sub_font.render(self.subtext, True, theme.text_secondary)
            sub_rect = sub_surf.get_rect(center=(self.rect.centerx, self.rect.centery + font_size // 3))
            surface.blit(sub_surf, sub_rect)
        else:
            surface.blit(text_surf, text_rect)


class Card:
    """Card container widget for panels, menus, and popups."""

    @staticmethod
    def draw(
        surface: pygame.Surface,
        rect: pygame.Rect,
        bg_color: ColorType,
        border_color: ColorType,
        border_radius: int = 12,
        border_width: int = 1
    ) -> None:
        pygame.draw.rect(surface, bg_color, rect, border_radius=border_radius)
        if border_width > 0:
            pygame.draw.rect(surface, border_color, rect, width=border_width, border_radius=border_radius)

