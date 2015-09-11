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
    def __init__(self):
        raise InheritanceError('Function not defined')

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
                 bgColor=TRANSPARENT, fgColor=BLACK, font=None):
        if rect is None:
            self._rect = pygame.Rect(0, 0, 60, 30)
        else:
            self._rect = pygame.Rect(rect)

        self._bgColor = bgColor
        self._fgColor = fgColor

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
        textSurf = self.font.render(self._text, True, self._fgColor)
        textRect = textSurf.get_rect()
        textRect.center = int(w / 2), int(h / 2)
        self._surfaceNormal.blit(textSurf, textRect)

    def handle_event(self, event):
        # As text is display-only, no need to handle events.
        # Still need to overwrite to avoid raising an exception.
        return

    def _propGetText(self):
        return self._text

    def _propSetText(self, newText):
        self._text = newText
        self._update()
        return

    def _propGetRect(self):
        return self._rect

    def _propSetRect(self, newRect):
        self._rect = pygame.Rect(newRect)
        self._update()
        return

    def _propGetFont(self):
        return self._font

    def _propSetFont(self, newFont):
        self._font = newFont
        self._update()
        return

    def _propGetBgColor(self):
        return self._bgColor

    def _propSetBgColor(self, newBgColor):
        self._bgColor = newBgColor
        self._update()
        return

    def _propGetFgColor(self):
        return self._fgColor

    def _propSetFgColor(self, newFgColor):
        self._fgColor = newFgColor
        self._update()
        return

    def _propGetVisible(self):
        return self._visible

    def _propSetVisible(self, visible):
        self._visible = visible
        self._update()
        return

    text = property(_propGetText, _propSetText)
    rect = property(_propGetRect, _propSetRect)
    font = property(_propGetFont, _propSetFont)
    bgColor = property(_propGetBgColor, _propSetBgColor)
    fgColor = property(_propGetFgColor, _propSetFgColor)
    visible = property(_propGetVisible, _propSetVisible)


class TextBox(UIElement):
    def __init__(self, rect=None, bgText=None,
                 bgColor=WHITE, inputTextColor=BLACK, bgTextColor=LIGHTGRAY,
                 font=None, callbackFunction=None):
        if rect is None:
            self._rect = pygame.Rect(0, 0, 60, 30)
        else:
            self._rect = pygame.Rect(rect)

        # Set values for surface display
        self._bgColor = bgColor
        self._inputTextColor = inputTextColor
        self._bgTextColor = bgTextColor
        self._visible = True

        # Input text uses a list that is converted to a string (which is immutable)
        self._inputText = ''
        self._listInputText = []

        # Background text 
        if bgText is None:
            self._bgText = 'Input'
        else:
            self._bgText = bgText

        # If no font is given, use gentium book, font size 12
        if font is None:
            self._font = UI_FONT
        else:
            self._font = font

        # Set callback function for when enter is pressed.  Defaults to None
        self._callbackFunction = callbackFunction

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
        bgTextSurf = self._font.render(self._bgText, True, self._bgTextColor, self._bgColor)
        bgTextRect = bgTextSurf.get_rect()
        bgTextRect.left = 5
        bgTextRect.centery = int(h / 2)
        self._surfaceNormal.blit(bgTextSurf, bgTextRect)

        # Create input text
        self._listInputText = [y for y in self._listInputText if y != '']
        self._inputText = str(''.join(self._listInputText))
        inputTextSurf = self._font.render(self._inputText, True, self._inputTextColor, self._bgColor)
        inputTextRect = inputTextSurf.get_rect()
        inputTextRect.left = 5
        inputTextRect.centery = int(h / 2)
        self._surfaceInput.blit(inputTextSurf, inputTextRect)

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

    def set_callback(self, newCallbackFunction):
        # Set the callback function to be called upon user hitting the enter key
        self._callbackFunction = newCallbackFunction

    def handle_event(self, event):
        # Track only mouse presses and key presses
        if event.type not in (
        pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
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

    def _propSetRect(self, newRect):
        self._rect = pygame.Rect(newRect)
        self._update()

    def _propGetRect(self):
        return self._rect

    def _propSetBgText(self, newBgText):
        self._bgText = newBgText
        self._update()

    def _propGetBgText(self):
        return self._bgText

    def _propSetBgColor(self, newBgColor):
        self._bgColor = newBgColor
        self._update()

    def _propGetBgColor(self):
        return self._bgColor

    def _propSetInputText(self, newInputText):
        self._listInputText = []
        for char in newInputText:
            self._listInputText.append(char)

    def _propGetInputText(self):
        return self._inputText

    def _propSetInputTextColor(self, newInputTextColor):
        self._inputTextColor = newInputTextColor
        self._update()

    def _propGetInputTextColor(self):
        return self._inputTextColor

    def _propSetBgTextColor(self, newBgTextColor):
        self._bgTextColor = newBgTextColor
        self._update()

    def _propGetBgTextColor(self):
        return self._bgTextColor

    def _propSetFont(self, newFont):
        self._font = newFont
        self._update()

    def _propGetFont(self):
        return self._font

    def _propSetCallbackFunction(self, newCallbackFunction):
        self._callbackFunction = newCallbackFunction
        self._update()

    def _propGetCallbackFunction(self):
        return self._callbackFunction

    def _propSetVisible(self, visible):
        self._visible = visible
        self._update()

    def _propGetVisible(self):
        return self._visible

    rect = property(_propGetRect, _propSetRect)
    bgText = property(_propGetBgText, _propSetBgText)
    bgColor = property(_propGetBgColor, _propSetBgColor)
    inputText = property(_propGetInputText, _propSetInputText)
    inputTextColor = property(_propGetInputTextColor, _propSetInputTextColor)
    bgTextColor = property(_propGetBgTextColor, _propSetBgTextColor)
    font = property(_propGetFont, _propSetFont)
    callbackFunction = property(_propGetCallbackFunction, _propSetCallbackFunction)
    visible = property(_propGetVisible, _propSetVisible)


class CheckBox(UIElement):
    def __init__(self, rect=None, bgColor=WHITE, callbackFunction=None):
        if rect is None:
            self._rect = pygame.Rect(0, 0, 14, 14)
        else:
            self._rect = pygame.Rect(rect)

        self._bgColor = bgColor

        self._isChecked = False
        self._lastMouseOverCheckbox = False
        self._visible = True

        self._callbackFunction = callbackFunction
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

    def set_callback(self, newCallbackFunction):
        # Set the callback function to be called upon checkbox changing checked state
        self._callbackFunction = newCallbackFunction

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
                self._lastMouseDownOverTextBox = False
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

    def _propSetRect(self, newRect):
        self._rect = pygame.Rect(newRect)
        self._update()

    def _propGetRect(self):
        return self._rect

    def _propSetBgColor(self, newBgColor):
        self._bgColor = newBgColor
        self._update()

    def _propGetBgColor(self):
        return self._bgColor

    def _propSetVisible(self, newVisible):
        self._visible = newVisible
        self._update()

    def _propGetVisible(self):
        return self._visible

    def _propSetCallbackFunction(self, newCallbackFunction):
        self._callbackFunction = newCallbackFunction
        self._update()

    def _propGetCallbackFunction(self):
        return self._callbackFunction

    def _propSetIsChecked(self, isChecked):
        self._isChecked = isChecked
        self._update()

    def _propGetIsChecked(self):
        return self._isChecked

    rect = property(_propGetRect, _propSetRect)
    bgColor = property(_propGetBgColor, _propSetBgColor)
    visible = property(_propGetVisible, _propSetVisible)
    callbackFunction = property(_propGetCallbackFunction, _propSetCallbackFunction)
    checked = property(_propGetIsChecked, _propSetIsChecked)


class Button(UIElement):
    def __init__(self, rect=None, text='',
                 bgColor=LIGHTGRAY, fgColor=BLACK, font=None):

        if rect is None:
            self.rect = pygame.Rect(0, 0, 30, 60)
        else:
            self.rect = pygame.Rect(rect)

        self.text = text
        self.bgColor = bgColor
        self.fgColor = fgColor

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
        self.lastMouseDownOverButton = False  # was the last mouse down event over the mouse button? (Used to track clicks.)
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
        captionSurf = self.font.render(self.text, True, self.fgColor, self.bgColor)
        captionRect = captionSurf.get_rect()
        captionRect.center = int(w / 2), int(h / 2)
        self.surfaceNormal.blit(captionSurf, captionRect)
        self.surfaceDown.blit(captionSurf, captionRect)

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

    def set_text(self, newText):
        self.text = newText

    def handle_event(self, event):
        if event.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN) or not self.visible:
            # The button only cares bout mouse-related events (or no events, if it is invisible)
            return

        hasExited = False
        if not self.mouseOverButton and self.rect.collidepoint(event.pos):
            # if mouse has entered the button:
            self.mouseOverButton = True
            self.mouse_enter(event)
        elif self.mouseOverButton and not self.rect.collidepoint(event.pos):
            # if mouse has exited the button:
            self.mouseOverButton = False
            hasExited = True  # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

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
        doMouseClick = False
        if event.type == pygame.MOUSEBUTTONUP:
            if self.lastMouseDownOverButton:
                doMouseClick = True
            self.lastMouseDownOverButton = False

            if self.buttonDown:
                self.buttonDown = False
                self.mouse_up(event)

            if doMouseClick:
                self.buttonDown = False
                self.mouse_click(event)

        if hasExited:
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


class PygButton:
    def __init__(self, rect=None, caption='',
                 bgcolor=LIGHTGRAY, fgcolor=BLACK, font=None,
                 normal=None, down=None, highlight=None):
        """Create a new button object. Parameters:
            rect - The size and position of the button as a pygame.Rect object
                or 4-tuple of integers.
            caption - The text on the button (default is blank)
            bgcolor - The background color of the button (default is a light
                gray color)
            fgcolor - The foreground color (i.e. the color of the text).
                Default is black.
            font - The pygame.font.Font object for the font of the text.
                Default is freesansbold in point 14.
            normal - A pygame.Surface object for the button's normal
                appearance.
            down - A pygame.Surface object for the button's pushed down
                appearance.
            highlight - A pygame.Surface object for the button's appearance
                when the mouse is over it.

            If the Surface objects are used, then the caption, bgcolor,
            fgcolor, and font parameters are ignored (and vice versa).
            Specifying the Surface objects lets the user use a custom image
            for the button.
            The normal, down, and highlight Surface objects must all be the
            same size as each other. Only the normal Surface object needs to
            be specified. The others, if left out, will default to the normal
            surface.
            """
        if rect is None:
            self._rect = pygame.Rect(0, 0, 30, 60)
        else:
            self._rect = pygame.Rect(rect)

        self._caption = caption
        self._bgcolor = bgcolor
        self._fgcolor = fgcolor

        if font is None:
            self._font = PYGBUTTON_FONT
        else:
            self._font = font

        # tracks the state of the button
        self.buttonDown = False  # is the button currently pushed down?
        self.mouseOverButton = False  # is the mouse currently hovering over the button?
        self.lastMouseDownOverButton = False  # was the last mouse down event over the mouse button? (Used to track clicks.)
        self._visible = True  # is the button visible
        self.customSurfaces = False  # button starts as a text button instead of having custom images for each surface

        if normal is None:
            # create the surfaces for a text button
            self.surfaceNormal = pygame.Surface(self._rect.size)
            self.surfaceDown = pygame.Surface(self._rect.size)
            self.surfaceHighlight = pygame.Surface(self._rect.size)
            self._update()  # draw the initial button images
        else:
            # create the surfaces for a custom image button
            self.setSurfaces(normal, down, highlight)

    def handleEvent(self, eventObj):
        """All MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN event objects
        created by Pygame should be passed to this method. handleEvent() will
        detect if the event is relevant to this button and change its state.

        There are two ways that your code can respond to button-events. One is
        to inherit the PygButton class and override the mouse*() methods. The
        other is to have the caller of handleEvent() check the return value
        for the strings 'enter', 'move', 'down', 'up', 'click', or 'exit'.

        Note that mouseEnter() is always called before mouseMove(), and
        mouseMove() is always called before mouseExit(). Also, mouseUp() is
        always called before mouseClick().

        buttonDown is always True when mouseDown() is called, and always False
        when mouseUp() or mouseClick() is called. lastMouseDownOverButton is
        always False when mouseUp() or mouseClick() is called."""

        if eventObj.type not in (pygame.MOUSEMOTION,
                                 pygame.MOUSEBUTTONUP,
                                 pygame.MOUSEBUTTONDOWN) or not self._visible:
            # The button only cares bout mouse-related events (or no events, if it is invisible)
            return []

        retVal = []

        hasExited = False
        if not self.mouseOverButton and self._rect.collidepoint(eventObj.pos):
            # if mouse has entered the button:
            self.mouseOverButton = True
            self.mouseEnter(eventObj)
            retVal.append('enter')
        elif self.mouseOverButton and not self._rect.collidepoint(eventObj.pos):
            # if mouse has exited the button:
            self.mouseOverButton = False
            hasExited = True  # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

        if self._rect.collidepoint(eventObj.pos):
            # if mouse event happened over the button:
            if eventObj.type == pygame.MOUSEMOTION:
                self.mouseMove(eventObj)
                retVal.append('move')
            elif eventObj.type == pygame.MOUSEBUTTONDOWN:
                self.buttonDown = True
                self.lastMouseDownOverButton = True
                self.mouseDown(eventObj)
                retVal.append('down')
        else:
            if eventObj.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                # if an up/down happens off the button, then the next up won't cause mouseClick()
                self.lastMouseDownOverButton = False

        # mouse up is handled whether or not it was over the button
        doMouseClick = False
        if eventObj.type == pygame.MOUSEBUTTONUP:
            if self.lastMouseDownOverButton:
                doMouseClick = True
            self.lastMouseDownOverButton = False

            if self.buttonDown:
                self.buttonDown = False
                self.mouseUp(eventObj)
                retVal.append('up')

            if doMouseClick:
                self.buttonDown = False
                self.mouseClick(eventObj)
                retVal.append('click')

        if hasExited:
            self.mouseExit(eventObj)
            retVal.append('exit')

        return retVal

    def draw(self, surfaceObj):
        """Blit the current button's appearance to the surface object."""
        if self._visible:
            if self.buttonDown:
                surfaceObj.blit(self.surfaceDown, self._rect)
            elif self.mouseOverButton:
                surfaceObj.blit(self.surfaceHighlight, self._rect)
            else:
                surfaceObj.blit(self.surfaceNormal, self._rect)

    def _update(self):
        """Redraw the button's Surface object. Call this method when the button has changed appearance."""
        if self.customSurfaces:
            self.surfaceNormal = pygame.transform.smoothscale(self.origSurfaceNormal, self._rect.size)
            self.surfaceDown = pygame.transform.smoothscale(self.origSurfaceDown, self._rect.size)
            self.surfaceHighlight = pygame.transform.smoothscale(self.origSurfaceHighlight, self._rect.size)
            return

        w = self._rect.width  # syntactic sugar
        h = self._rect.height  # syntactic sugar

        # fill background color for all buttons
        self.surfaceNormal.fill(self.bgcolor)
        self.surfaceDown.fill(self.bgcolor)
        self.surfaceHighlight.fill(self.bgcolor)

        # draw caption text for all buttons
        captionSurf = self._font.render(self._caption, True, self.fgcolor, self.bgcolor)
        captionRect = captionSurf.get_rect()
        captionRect.center = int(w / 2), int(h / 2)
        self.surfaceNormal.blit(captionSurf, captionRect)
        self.surfaceDown.blit(captionSurf, captionRect)

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

    def mouseClick(self, event):
        pass  # This class is meant to be overridden.

    def mouseEnter(self, event):
        pass  # This class is meant to be overridden.

    def mouseMove(self, event):
        pass  # This class is meant to be overridden.

    def mouseExit(self, event):
        pass  # This class is meant to be overridden.

    def mouseDown(self, event):
        pass  # This class is meant to be overridden.

    def mouseUp(self, event):
        pass  # This class is meant to be overridden.

    def setSurfaces(self, normalSurface, downSurface=None, highlightSurface=None):
        """Switch the button to a custom image type of button (rather than a
        text button). You can specify either a pygame.Surface object or a
        string of a filename to load for each of the three button appearance
        states."""
        if downSurface is None:
            downSurface = normalSurface
        if highlightSurface is None:
            highlightSurface = normalSurface

        if type(normalSurface) == str:
            self.origSurfaceNormal = pygame.image.load(normalSurface)
        if type(downSurface) == str:
            self.origSurfaceDown = pygame.image.load(downSurface)
        if type(highlightSurface) == str:
            self.origSurfaceHighlight = pygame.image.load(highlightSurface)

        if self.origSurfaceNormal.get_size() != self.origSurfaceDown.get_size() != self.origSurfaceHighlight.get_size():
            raise Exception('Size Mismatch')

        self.surfaceNormal = self.origSurfaceNormal
        self.surfaceDown = self.origSurfaceDown
        self.surfaceHighlight = self.origSurfaceHighlight
        self.customSurfaces = True
        self._rect = pygame.Rect(
            (self._rect.left, self._rect.top, self.surfaceNormal.get_width(), self.surfaceNormal.get_height()))

    def _propGetCaption(self):
        return self._caption

    def _propSetCaption(self, captionText):
        self.customSurfaces = False
        self._caption = captionText
        self._update()

    def _propGetRect(self):
        return self._rect

    def _propSetRect(self, newRect):
        # Note that changing the attributes of the Rect won't update the button. You have to re-assign the rect member.
        self._update()
        self._rect = newRect

    def _propGetVisible(self):
        return self._visible

    def _propSetVisible(self, setting):
        self._visible = setting

    def _propGetFgColor(self):
        return self._fgcolor

    def _propSetFgColor(self, setting):
        self.customSurfaces = False
        self._fgcolor = setting
        self._update()

    def _propGetBgColor(self):
        return self._bgcolor

    def _propSetBgColor(self, setting):
        self.customSurfaces = False
        self._bgcolor = setting
        self._update()

    def _propGetFont(self):
        return self._font

    def _propSetFont(self, setting):
        self.customSurfaces = False
        self._font = setting
        self._update()

    caption = property(_propGetCaption, _propSetCaption)
    rect = property(_propGetRect, _propSetRect)
    visible = property(_propGetVisible, _propSetVisible)
    fgcolor = property(_propGetFgColor, _propSetFgColor)
    bgcolor = property(_propGetBgColor, _propSetBgColor)
    font = property(_propGetFont, _propSetFont)
