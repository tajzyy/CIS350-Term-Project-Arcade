import pygame
from sprite import Sprite, AnimatedSprite
from settings import Settings


class Button(Sprite):
    """Button class that works with keyboard and mouse"""

    def __init__(self, x: int, y: int, text, font, action,
                 color=None, hover_color=None, center=True) -> None:
        """Initializes Button"""
        # set defaults
        default_color = '#DDA059'
        default_hover_color = '#FFD921'

        # set instance variables
        self.color = default_color if color is None else color
        self.hover_color = default_hover_color if hover_color is None else hover_color
        self.currently_hovered = False
        self.currently_keyboard_hovered = False
        self.currently_mouse_hovered = False
        self.text = text
        self.font = font
        self.action = action

        # render font
        self.font_render = self.font.render(self.text, True, self.color)

        # call super with rendered font
        super().__init__(x, y, self.font_render)

        # center button
        if center:
            self.rect.center = (x, y)

    def check_mouse_hover(self, mouse: tuple) -> bool:
        """Checks if the mouse is hovering
        return True if colliding, False if not
        """
        collision = self.rect.collidepoint(mouse[0], mouse[1])
        self.currently_mouse_hovered = collision
        return self.currently_mouse_hovered

    def set_keyboard_hover(self, val: bool) -> None:
        """Sets keyboard hover to val"""
        self.currently_keyboard_hovered = val

    def update(self) -> None:
        """Updates button"""
        self.currently_hovered = (self.currently_keyboard_hovered
                                  or self.currently_mouse_hovered)

        changed = False
        if self.currently_hovered:
            # re-render font to hover
            self.font_render = self.font.render(
                self.text, True, self.hover_color)
            changed = True
        elif not self.currently_hovered:
            # re-render font to not hovered
            self.font_render = self.font.render(
                self.text, True, self.color)
            changed = True

        if changed:
            self.image = self.font_render
            self.rotate(self.rotation_degrees)

    def do_action(self) -> None:
        """Another way to call b.action()"""
        self.action()

    def do_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.do_action()
            return True
        return False

class AnimatedButton(AnimatedSprite):
    def __init__(self, x: int, y: int, path, animation_speed, action,
                center=True) -> None:
        """Initializes Button"""

        # set instance variables
        self.currently_hovered = False
        self.currently_keyboard_hovered = False
        self.currently_mouse_hovered = False
        self.action = action

        # render font

        # call super with rendered font
        super().__init__(x, y, path, animation_speed)

        # don't do animation
        self.pause_animation = True

        # center button
        if center:
            self.rect.center = (x, y)

    def check_mouse_hover(self, mouse: tuple) -> bool:
        """Checks if the mouse is hovering
        return True if colliding, False if not
        """
        collision = self.rect.collidepoint(mouse[0], mouse[1])
        self.currently_mouse_hovered = collision
        return self.currently_mouse_hovered

    def set_keyboard_hover(self, val: bool) -> None:
        """Sets keyboard hover to val"""
        self.currently_keyboard_hovered = val

    def update(self) -> None:
        """Updates button"""
        self.currently_hovered = (self.currently_keyboard_hovered
                                  or self.currently_mouse_hovered)

        if self.currently_hovered:
            self.pause_animation = False
        else:
            self.current_sprite = 0
            self.image = self.images[0]
            self.pause_animation = True
        super().update()

    def do_action(self) -> None:
        """Another way to call b.action()"""
        self.action()

    def do_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.do_action()
            return True
        return False


class ButtonGroup:
    def __init__(self):
        self.button_list: list[Button | AnimatedButton] = []
        self.num_buttons = 0
        self.current_button_index = 0
        self.enable_keyboard = True

    def add(self, button: Button):
        self.num_buttons += 1
        self.button_list.append(button)
        # if self.num_buttons == 1:
        #     self.button_list[0].set_keyboard_hover(True)

    def draw(self, screen):
        for button in self.button_list:
            button.draw(screen)

    def update(self):
        if not self.enable_keyboard:
            for button in self.button_list:
                button.currently_keyboard_hovered = False
        for button in self.button_list:
            button.update()

    def change_button(self, direction: str, sound=None):
        # play sound
        if sound:
            sound.play()

        # sets current button to not hovered
        self.button_list[self.current_button_index].set_keyboard_hover(False)

        # changes button
        if direction == 'up':
            self.current_button_index = (
                self.current_button_index - 1) % self.num_buttons
        elif direction == 'down':
            self.current_button_index = (
                self.current_button_index + 1) % self.num_buttons

        # sets new button to hovered
        self.button_list[self.current_button_index].set_keyboard_hover(True)

    def do_action(self):
        self.button_list[self.current_button_index].do_action()

    @staticmethod
    def get_direction() -> str:
        direction = None
        keys = pygame.key.get_pressed()
        if keys[Settings.main_keybinding.up] or keys[Settings.alternate_keybinding.up]:
            direction = 'up'
        elif keys[Settings.main_keybinding.down] or keys[Settings.alternate_keybinding.down]:
            direction = 'down'
        return direction

    def do_movement(self):
        if (direction := self.get_direction()) is not None:
            self.change_button(direction)

    def do_event(self, event, sound=None):
        mouse = pygame.mouse.get_pos()
        mouse_hovered = False
        button_clicked = False
        for button in self.button_list:
            mouse_hovered = button.check_mouse_hover(mouse) or mouse_hovered
            if mouse_hovered:
                self.enable_keyboard = False
                if not button_clicked:
                    button_clicked = button.do_event(event)

        # if the mouse is not hovering over a button, enable the keyboard
        if not mouse_hovered:
            self.enable_keyboard = True

        # if any button in the group is being hovered
        # by the mouse don't do any actions
        if not self.enable_keyboard:
            return

        # handle changing buttons and doing actions
        if event.type == pygame.KEYDOWN:
            if Settings.default_bindings:
                if event.key == Settings.main_keybinding.up:
                    self.change_button('up', sound)
                elif event.key == Settings.main_keybinding.down:
                    self.change_button('down', sound)
                elif event.key == Settings.main_keybinding.enter:
                    self.do_action()
            else:
                if event.key == Settings.alternate_keybinding.up:
                    self.change_button('up', sound)
                elif event.key == Settings.alternate_keybinding.down:
                    self.change_button('down', sound)
                elif event.key == Settings.alternate_keybinding.enter:
                    self.do_action()

        # if event.type == pygame.KEYDOWN:
        #     if event.key in (Settings.main_keybinding.up, Settings.alternate_keybinding.up):
        #         self.change_button('up', sound)
        #     elif event.key in (Settings.main_keybinding.down, Settings.alternate_keybinding.down):
        #         self.change_button('down', sound)
        #     elif event.key == Settings.main_keybinding.enter:
        #         self.do_action()
