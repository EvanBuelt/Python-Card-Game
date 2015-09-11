import pygame

pygame.font.init()
UI_FONT = gentiumBookBasic = pygame.font.Font(pygame.font.match_font('gentiumbookbasic'), 14)

BLACK = (0, 0, 0, 255)
DARKGRAY = (64, 64, 64, 255)
GRAY = (128, 128, 128, 255)
LIGHTGRAY = (140, 140, 140, 255)
LIGHTGRAY2 = (212, 208, 200, 255)
WHITE = (255, 255, 255, 255)
TRANSPARENT = (255, 255, 255, 0)
GREEN = (24, 119, 24, 255)


class EventHandler:
    def __init__(self):
        self._functions = []

    def __iadd__(self, function):
        if function not in self._functions:
            self._functions.append(function)
        return self

    def __isub__(self, function):
        if function in self._functions:
            self._functions.remove(function)
        return self

    def append(self, function):
        if function not in self._functions:
            self._functions.append(function)

    def pop(self, index=None):
        if index is None and len(self._functions) > 0:
            self._functions.pop()
        elif 0 <= index < len(self._functions):
            self._functions.pop(index)

    def remove(self, function):
        if function in self._functions:
            self._functions.remove(function)

    def fire(self, *args, **kwargs):
        for function in self._functions:
            function(*args, **kwargs)


class InheritanceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UIElement(object):

    def render(self, surface):
        raise InheritanceError('Function not defined')

    def _update(self):
        raise InheritanceError('Function not defined')

    def set_location(self, x, y):
        raise InheritanceError('Function not defined')

    def handle_event(self, event):
        raise InheritanceError('Function not defined')


class Card(UIElement):
    def __init__(self):
        pass

    def render(self, surface):
        pass

    def _update(self):
        pass

    def set_location(self, x, y):
        pass

    def set_callback(self, function):
        pass

    def handle_event(self, event):
        pass

    def mouse_click(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass


class Text(UIElement):
    def __init__(self, rect=None, text='',
                 bg_color=TRANSPARENT, fg_color=BLACK, font=None):
        if rect is None:
            self._rect = pygame.Rect(0, 0, 60, 30)
        else:
            self._rect = pygame.Rect(rect)

        self._bgColor = bg_color
        self._fgColor = fg_color

        if text is '':
            self._text = 'Text'
        else:
            self._text = text

        if font is None:
            self._font = UI_FONT
        else:
            self._font = font

        self._visible = True

        # Create standard surface for text
        self._surfaceNormal = pygame.Surface(self._rect.size).convert_alpha()
        self._update()

    def render(self, surface):
        if self._visible:
            surface.blit(self._surfaceNormal, self._rect)

    def _update(self):
        # Make syntax pretty
        w = self._rect.width
        h = self._rect.height

        # Update surface to fit size of rect
        self._surfaceNormal = pygame.Surface(self._rect.size).convert_alpha()
        self._surfaceNormal.fill(self._bgColor)

        # Draw text on surface
        text_surf = self.font.render(self._text, True, self._fgColor)
        text_rect = text_surf.get_rect()
        text_rect.center = int(w / 2), int(h / 2)
        self._surfaceNormal.blit(text_surf, text_rect)

    def handle_event(self, event):
        # As text is display-only, no need to handle events.
        # Still need to overwrite to avoid raising an exception.
        return

    def _prop_get_text(self):
        return self._text

    def _prop_set_text(self, new_text):
        self._text = new_text
        self._update()
        return

    def _prop_get_rect(self):
        return self._rect

    def _prop_set_rect(self, new_rect):
        self._rect = pygame.Rect(new_rect)
        self._update()
        return

    def _prop_get_font(self):
        return self._font

    def _prop_set_font(self, new_font):
        self._font = new_font
        self._update()
        return

    def _prop_get_bg_color(self):
        return self._bgColor

    def _prop_set_bg_color(self, new_background_color):
        self._bgColor = new_background_color
        self._update()
        return

    def _prop_get_fg_color(self):
        return self._fgColor

    def _prop_set_fg_color(self, new_foreground_color):
        self._fgColor = new_foreground_color
        self._update()
        return

    def _prop_get_visible(self):
        return self._visible

    def _prop_set_visible(self, visible):
        self._visible = visible
        self._update()
        return

    text = property(_prop_get_text, _prop_set_text)
    rect = property(_prop_get_rect, _prop_set_rect)
    font = property(_prop_get_font, _prop_set_font)
    bgColor = property(_prop_get_bg_color, _prop_set_bg_color)
    fgColor = property(_prop_get_fg_color, _prop_set_fg_color)
    visible = property(_prop_get_visible, _prop_set_visible)


class TextBox(UIElement):
    def __init__(self, rect=None, background_text=None, background_color=WHITE,
                 input_text_color=BLACK, background_text_color=LIGHTGRAY,
                 font=None, callback_function=None):
        if rect is None:
            self._rect = pygame.Rect(0, 0, 60, 30)
        else:
            self._rect = pygame.Rect(rect)

        # Set values for surface display
        self._bgColor = background_color
        self._inputTextColor = input_text_color
        self._bgTextColor = background_text_color
        self._visible = True

        # Input text uses a list that is converted to a string (which is immutable)
        self._inputText = ''
        self._listInputText = []

        # Background text 
        if background_text is None:
            self._bgText = 'Input'
        else:
            self._bgText = background_text

        # If no font is given, use gentium book, font size 12
        if font is None:
            self._font = UI_FONT
        else:
            self._font = font

        # Set callback function for when enter is pressed.  Defaults to None
        self._callbackFunction = callback_function

        # Track mouse click events and keyboard inputs
        self._isSelected = False
        self._lastMouseDownOverTextBox = False
        self._keydown = False

        # Create Surface
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceInput = pygame.Surface(self._rect.size)

        self._update()

    def render(self, surface):
        if self._visible:
            if self._inputText is not '':
                surface.blit(self._surfaceInput, self._rect)
            else:
                surface.blit(self._surfaceNormal, self._rect)

    def _update(self):
        # Syntactic sugar for height and width for text
        w = self._rect.width
        h = self._rect.height

        # Start with a clean slate for the surfaces with background color
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceInput = pygame.Surface(self._rect.size)

        self._surfaceNormal.fill(self._bgColor)
        self._surfaceInput.fill(self._bgColor)

        # Create background text
        bg_text_surf = self._font.render(self._bgText, True, self._bgTextColor, self._bgColor)
        bg_text_rect = bg_text_surf.get_rect()
        bg_text_rect.left = 5
        bg_text_rect.centery = int(h / 2)
        self._surfaceNormal.blit(bg_text_surf, bg_text_rect)

        # Create input text
        self._listInputText = [y for y in self._listInputText if y != '']
        self._inputText = str(''.join(self._listInputText))
        input_text_surf = self._font.render(self._inputText, True, self._inputTextColor, self._bgColor)
        input_text_rect = input_text_surf.get_rect()
        input_text_rect.left = 5
        input_text_rect.centery = int(h / 2)
        self._surfaceInput.blit(input_text_surf, input_text_rect)

        # Update normal surface used not selected and no input
        pygame.draw.rect(self._surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.line(self._surfaceNormal, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceNormal, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self._surfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, GRAY, (1, h - 2), (w - 2, h - 2))
        pygame.draw.line(self._surfaceNormal, GRAY, (w - 2, 1), (w - 2, h - 2))

        # Update input surface used for when selected or there is input
        pygame.draw.rect(self._surfaceInput, BLACK, pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.line(self._surfaceInput, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceInput, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self._surfaceInput, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceInput, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, GRAY, (1, h - 2), (w - 2, h - 2))
        pygame.draw.line(self._surfaceNormal, GRAY, (w - 2, 1), (w - 2, h - 2))

    def set_callback(self, new_callback_function):
        # Set the callback function to be called upon user hitting the enter key
        self._callbackFunction = new_callback_function

    def handle_event(self, event):
        # Track only mouse presses and key presses
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
                              pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
            return

        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            if self._rect.collidepoint(event.pos):
                # clicking and releasing inside textbox selects it
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._lastMouseDownOverTextBox = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._lastMouseDownOverTextBox:
                        self._isSelected = True
                    self._lastMouseDownOverTextBox = False
            else:
                # releasing mouseclick outside textbox deselects it
                self._lastMouseDownOverTextBox = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self._isSelected = False

        if event.type is pygame.KEYDOWN and self._isSelected:
            if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                if len(self._listInputText) > 0:
                    self._listInputText.pop()

            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                pass  # Future update.  Allow user to move cursor location

            elif event.key in (pygame.K_TAB, pygame.K_ESCAPE):
                pass  # Events to ignore

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self._callbackFunction is not None:
                    self._callbackFunction(self)

            else:
                self._listInputText.append(event.unicode)

            self._update()

    def mouse_click(self, event):
        pass

    def mouse_enter(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_exit(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def keyboard_down(self, event):
        pass

    def keyboard_up(self, event):
        pass

    def _prop_set_rect(self, new_rect):
        self._rect = pygame.Rect(new_rect)
        self._update()

    def _prop_get_rect(self):
        return self._rect

    def _prop_set_background_text(self, new_background_text):
        self._bgText = new_background_text
        self._update()

    def _prop_get_background_text(self):
        return self._bgText

    def _prop_set_background_color(self, new_background_color):
        self._bgColor = new_background_color
        self._update()

    def _prop_get_background_color(self):
        return self._bgColor

    def _prop_set_input_text(self, new_input_text):
        self._listInputText = []
        for char in new_input_text:
            self._listInputText.append(char)

    def _prop_get_input_text(self):
        return self._inputText

    def _prop_set_input_text_color(self, new_input_text_color):
        self._inputTextColor = new_input_text_color
        self._update()

    def _prop_get_input_text_color(self):
        return self._inputTextColor

    def _prop_set_background_text_color(self, new_background_text_color):
        self._bgTextColor = new_background_text_color
        self._update()

    def _prop_get_background_text_color(self):
        return self._bgTextColor

    def _prop_set_font(self, new_font):
        self._font = new_font
        self._update()

    def _prop_get_font(self):
        return self._font

    def _prop_set_callback_function(self, new_callback_function):
        self._callbackFunction = new_callback_function
        self._update()

    def _prop_get_callback_function(self):
        return self._callbackFunction

    def _prop_set_visible(self, visible):
        self._visible = visible
        self._update()

    def _prop_get_visible(self):
        return self._visible

    rect = property(_prop_get_rect, _prop_set_rect)
    bgText = property(_prop_get_background_text, _prop_set_background_text)
    bgColor = property(_prop_get_background_color, _prop_set_background_color)
    inputText = property(_prop_get_input_text, _prop_set_input_text)
    inputTextColor = property(_prop_get_input_text_color, _prop_set_input_text_color)
    bgTextColor = property(_prop_get_background_text_color, _prop_set_background_text_color)
    font = property(_prop_get_font, _prop_set_font)
    callbackFunction = property(_prop_get_callback_function, _prop_set_callback_function)
    visible = property(_prop_get_visible, _prop_set_visible)


class CheckBox(UIElement):
    def __init__(self, rect=None, background_color=WHITE, callback_function=None):
        if rect is None:
            self._rect = pygame.Rect(0, 0, 14, 14)
        else:
            self._rect = pygame.Rect(rect)

        self._bgColor = background_color

        self._isChecked = False
        self._lastMouseDownOverCheckBox = False
        self._visible = True

        self._callbackFunction = callback_function
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceChecked = pygame.Surface(self._rect.size)

        self._update()

    def render(self, surface):
        if self._isChecked:
            surface.blit(self._surfaceChecked, self._rect)
        else:
            surface.blit(self._surfaceNormal, self._rect)

    def _update(self):
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceChecked = pygame.Surface(self._rect.size)

        w = self._rect.width
        h = self._rect.height

        self._surfaceNormal.fill(self._bgColor)
        pygame.draw.rect(self._surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.rect(self._surfaceNormal, BLACK, pygame.Rect((1, 1, w - 2, h - 2)),
                         1)  # black border around everything

        self._surfaceChecked.fill(self._bgColor)
        pygame.draw.rect(self._surfaceChecked, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.rect(self._surfaceChecked, BLACK, pygame.Rect((1, 1, w - 2, h - 2)),
                         1)  # black border around everything
        pygame.draw.line(self._surfaceChecked, GREEN, (3, int(h / 2)), (int(w / 2), h - 5), 3)
        pygame.draw.line(self._surfaceChecked, GREEN, (int(w / 2), h - 5), (w - 5, 4), 3)

    def set_callback(self, new_callback_function):
        # Set the callback function to be called upon checkbox changing checked state
        self._callbackFunction = new_callback_function

    def handle_event(self, event):
        # Track only mouse presses and key presses
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN) or not self._visible:
            return

        if self._rect.collidepoint(event.pos):
            # clicking and releasing inside checkbox toggles check
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._lastMouseDownOverCheckBox = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self._lastMouseDownOverCheckBox and self._isChecked:
                    self._isChecked = False
                    if self._callbackFunction is not None:
                        self._callbackFunction(self)
                elif self._lastMouseDownOverCheckBox and not self._isChecked:
                    self._isChecked = True
                    if self._callbackFunction is not None:
                        self._callbackFunction(self)
                self._lastMouseDownOverCheckBox = False
        else:
            self._lastMouseDownOverCheckBox = False

        self._update()

    def mouse_click(self, event):
        pass

    def mouse_enter(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_exit(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def _prop_set_rect(self, new_rect):
        self._rect = pygame.Rect(new_rect)
        self._update()

    def _prop_get_rect(self):
        return self._rect

    def _prop_set_background_color(self, new_background_color):
        self._bgColor = new_background_color
        self._update()

    def _prop_get_background_color(self):
        return self._bgColor

    def _prop_set_visible(self, new_visible):
        self._visible = new_visible
        self._update()

    def _prop_get_visible(self):
        return self._visible

    def _prop_set_callback_function(self, new_callback_function):
        self._callbackFunction = new_callback_function
        self._update()

    def _prop_get_callback_function(self):
        return self._callbackFunction

    def _prop_set_is_checked(self, is_checked):
        self._isChecked = is_checked
        self._update()

    def _prop_get_is_checked(self):
        return self._isChecked

    rect = property(_prop_get_rect, _prop_set_rect)
    bgColor = property(_prop_get_background_color, _prop_set_background_color)
    visible = property(_prop_get_visible, _prop_set_visible)
    callbackFunction = property(_prop_get_callback_function, _prop_set_callback_function)
    checked = property(_prop_get_is_checked, _prop_set_is_checked)


class Button(UIElement):
    def __init__(self, rect=None, text='',
                 background_color=LIGHTGRAY, foreground_color=BLACK, font=None):

        if rect is None:
            self.rect = pygame.Rect(0, 0, 30, 60)
        else:
            self.rect = pygame.Rect(rect)

        self.text = text
        self.bgColor = background_color
        self.fgColor = foreground_color

        if font is None:
            self.font = UI_FONT
        else:
            self.font = font

        self.surfaceNormal = pygame.Surface(self.rect.size)
        self.surfaceDown = pygame.Surface(self.rect.size)
        self.surfaceHighlight = pygame.Surface(self.rect.size)

        # tracks the state of the button
        self.buttonDown = False  # is the button currently pushed down?
        self.mouseOverButton = False  # is the mouse currently hovering over the button?
        self.lastMouseDownOverButton = False  # was the last mouse down event over the mouse button? (Tracks clicks.)
        self.visible = True  # is the button visible

        self._update()

    def render(self, surface):
        if self.visible:
            if self.buttonDown:
                surface.blit(self.surfaceDown, self.rect)
            elif self.mouseOverButton:
                surface.blit(self.surfaceHighlight, self.rect)
            else:
                surface.blit(self.surfaceNormal, self.rect)

    def _update(self):
        self.surfaceNormal = pygame.Surface(self.rect.size)
        self.surfaceDown = pygame.Surface(self.rect.size)
        self.surfaceHighlight = pygame.Surface(self.rect.size)

        w = self.rect.width  # syntactic sugar
        h = self.rect.height  # syntactic sugar

        # fill background color for all buttons
        self.surfaceNormal.fill(self.bgColor)
        self.surfaceDown.fill(self.bgColor)
        self.surfaceHighlight.fill(self.bgColor)

        # draw caption text for all buttons
        caption_surf = self.font.render(self.text, True, self.fgColor, self.bgColor)
        caption_rect = caption_surf.get_rect()
        caption_rect.center = int(w / 2), int(h / 2)
        self.surfaceNormal.blit(caption_surf, caption_rect)
        self.surfaceDown.blit(caption_surf, caption_rect)

        # draw border for normal button
        pygame.draw.rect(self.surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.surfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceNormal, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.surfaceNormal, GRAY, (w - 2, 2), (w - 2, h - 2))

        # draw border for down button
        pygame.draw.rect(self.surfaceDown, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.surfaceDown, DARKGRAY, (1, h - 2), (1, 1))
        pygame.draw.line(self.surfaceDown, DARKGRAY, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceDown, GRAY, (2, h - 3), (2, 2))
        pygame.draw.line(self.surfaceDown, GRAY, (2, 2), (w - 3, 2))

        # draw border for highlight button
        self.surfaceHighlight = self.surfaceNormal

    def get_text(self):
        return self.text

    def set_text(self, new_text):
        self.text = new_text

    def handle_event(self, event):
        if event.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN) or not self.visible:
            # The button only cares bout mouse-related events (or no events, if it is invisible)
            return

        has_exited = False
        if not self.mouseOverButton and self.rect.collidepoint(event.pos):
            # if mouse has entered the button:
            self.mouseOverButton = True
            self.mouse_enter(event)
        elif self.mouseOverButton and not self.rect.collidepoint(event.pos):
            # if mouse has exited the button:
            self.mouseOverButton = False
            has_exited = True  # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

        if self.rect.collidepoint(event.pos):
            # if mouse event happened over the button:
            if event.type == pygame.MOUSEMOTION:
                self.mouse_move(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.buttonDown = True
                self.lastMouseDownOverButton = True
                self.mouse_down(event)
        else:
            if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                # if an up/down happens off the button, then the next up won't cause mouseClick()
                self.lastMouseDownOverButton = False

        # mouse up is handled whether or not it was over the button
        do_mouse_click = False
        if event.type == pygame.MOUSEBUTTONUP:
            if self.lastMouseDownOverButton:
                do_mouse_click = True
            self.lastMouseDownOverButton = False

            if self.buttonDown:
                self.buttonDown = False
                self.mouse_up(event)

            if do_mouse_click:
                self.buttonDown = False
                self.mouse_click(event)

        if has_exited:
            self.mouse_exit(event)

    def mouse_click(self, event):
        pass

    def mouse_enter(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_exit(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass
