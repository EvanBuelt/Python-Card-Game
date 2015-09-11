import UI
import sys
import pygame


def displayTextInput(textBoxObject):
    print "Got text from ", textBoxObject, " and text is: ", textBoxObject.inputText
    textBoxObject.inputText = ''


def displayChecked(checkBoxObject):
    print "Checkbox ", checkBoxObject, " has checked: ", checkBoxObject.checked


def test():
    myTestEngine = TestEngine(400, 300, 'Testing different UI elements')

    # Create UI elements
    text1 = UI.Text(rect=pygame.Rect(30, 30, 60, 20), text='Hello')
    text2 = UI.Text(rect=pygame.Rect(30, 65, 60, 20), text='World!', bgColor=(200, 200, 200, 50))
    text3 = UI.Text(rect=pygame.Rect(30, 100, 60, 20), text='0', bgColor=(70, 200, 70))
    textbox1 = UI.TextBox(rect=pygame.Rect(100, 30, 180, 20), bgText='Username')
    textbox2 = UI.TextBox(rect=pygame.Rect(100, 65, 180, 20), bgText='Password')
    checkbox1 = UI.CheckBox(rect=pygame.Rect(290, 30, 14, 14))
    checkbox2 = UI.CheckBox(rect=pygame.Rect(290, 65, 14, 14))
    button1 = UI.Button(rect=pygame.Rect(310, 30, 70, 20), text='Press me')
    button2 = UI.Button(rect=pygame.Rect(310, 65, 50, 20), text='Don\'t')
    text4 = UI.Text(rect=pygame.Rect(100, 90, 120, 20), text='')

    textbox1.set_callback(displayTextInput)
    textbox2.set_callback(displayTextInput)

    checkbox1.set_callback(displayChecked)
    checkbox2.set_callback(displayChecked)

    # Add UI elements to list
    myTestEngine.addUIElement(text1)
    myTestEngine.addUIElement(text2)
    myTestEngine.addUIElement(text3)
    myTestEngine.addUIElement(textbox1)
    myTestEngine.addUIElement(textbox2)
    myTestEngine.addUIElement(checkbox1)
    myTestEngine.addUIElement(checkbox2)
    myTestEngine.addUIElement(button1)
    myTestEngine.addUIElement(button2)
    myTestEngine.addUIElement(text4)

    # Test setting and getting of each UI element (only one per class is necessary)
    test_text(text1)
    test_textBox(textbox1)

    text1.rect = pygame.Rect(30, 20, text1.rect.width, text1.rect.height)
    text2.visible = False

    while True:
        myTestEngine.update()
        myTestEngine.render()

        # someText = int(text3.get_text())
        # someText = someText + 1
        # text3.set_text(str(someText))

        '''
        bgColor1 = backgroundColor[0] + 1
        bgColor2 = backgroundColor[1] + 1
        bgColor3 = backgroundColor[2] + 1

        if bgColor1 > 255 :
            bgColor1 = 0
        if bgColor2 > 255 :
            bgColor2 = 0
        if bgColor3 > 255 :
            bgColor3 = 0
            
        backgroundColor = (bgColor1,bgColor2,bgColor3)
        background.fill(backgroundColor)
        '''

        pygame.time.delay(20)


class TestEngine:
    def __init__(self, width=400, height=300, name='Test Engine', bgColor=(80, 150, 80)):
        # Initialize screen
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption(name)

        # Create background surface
        self.background = pygame.Surface(self.screen.get_size())
        self.background.convert()
        self.backgroundColor = bgColor
        self.background.fill(self.backgroundColor)

        # Create list for game loop to iterate over
        self.screenUIElements = []
        pygame.key.set_repeat(500, 50)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            for element in self.screenUIElements:
                element.handle_event(event)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        for UIElement in self.screenUIElements:
            UIElement.render(self.screen)

        pygame.display.flip()

    def addUIElement(self, UIElement):
        self.screenUIElements.append(UIElement)


# Functions for testing each UI Element to ensure element works properly
def test_text(testText):
    if not isinstance(testText, UI.Text):
        print 'Object not an instance of text, or derived instance of text'
        return

    testSuccess = True
    # Get data from text class
    text = testText._text
    rect = testText._rect
    font = testText._font
    fgColor = testText._fgColor
    bgColor = testText._bgColor
    visible = testText._visible

    # Print original contents.
    print ''
    print testText
    print testText._text
    print testText._rect
    print testText._font
    print testText._fgColor
    print testText._bgColor
    print testText._visible
    print ''

    # Test each property.
    testText.text = testText.text
    testText.rect = testText.rect
    testText.font = testText.font
    testText.fgColor = testText.fgColor
    testText.bgColor = testText.bgColor
    testText.visible = testText.visible

    # Print contents after using in-built properties.
    print ''
    print testText._text
    print testText._rect
    print testText._font
    print testText._fgColor
    print testText._bgColor
    print testText._visible
    print ''

    # Test if data after testing properties is same as old data
    if text != testText._text:
        testSuccess = False
    if rect != testText._rect:
        testSuccess = False
    if font != testText._font:
        testSuccess = False
    if fgColor != testText._fgColor:
        testSuccess = False
    if bgColor != testText._bgColor:
        testSuccess = False
    if visible != testText._visible:
        testSuccess = False

    if testSuccess:
        print "Test was successful"
    else:
        print "Test was not successful"

    return testSuccess


def test_textBox(testTextBox):
    if not isinstance(testTextBox, UI.TextBox):
        print 'Object not an instance of textbox, or derived instance of textbox'
        return

    testSuccess = True

    # Get data from textbox class
    rect = testTextBox._rect
    bgColor = testTextBox._bgColor
    bgText = testTextBox._bgText
    bgTextColor = testTextBox._bgTextColor
    inputText = testTextBox._inputText
    listInputText = testTextBox._listInputText
    inputTextColor = testTextBox._inputTextColor
    font = testTextBox._font
    callbackFunction = testTextBox._callbackFunction
    visible = testTextBox._visible

    # Print original contents.
    print ''
    print testTextBox
    print testTextBox._rect
    print testTextBox._bgColor
    print testTextBox._bgText
    print testTextBox._bgTextColor
    print testTextBox._inputText
    print testTextBox._listInputText
    print testTextBox._inputTextColor
    print testTextBox._font
    print testTextBox._callbackFunction
    print testTextBox._visible
    print ''

    # Test each property.
    testTextBox.rect = testTextBox.rect
    testTextBox.bgText = testTextBox.bgText
    testTextBox.bgColor = testTextBox.bgColor
    testTextBox.inputText = testTextBox.inputText
    testTextBox.inputTextColor = testTextBox.inputTextColor
    testTextBox.bgTextColor = testTextBox.bgTextColor
    testTextBox.font = testTextBox.font
    testTextBox.callbackFunction = testTextBox.callbackFunction
    testTextBox.visible = testTextBox.visible

    # Print contents after using in-built properties.
    print ''
    print testTextBox._rect
    print testTextBox._bgColor
    print testTextBox._bgText
    print testTextBox._bgTextColor
    print testTextBox._inputText
    print testTextBox._listInputText
    print testTextBox._inputTextColor
    print testTextBox._font
    print testTextBox._callbackFunction
    print testTextBox._visible
    print ''

    # Test if data after testing properties is same as old data
    if rect != testTextBox._rect:
        testSuccess = False
    if bgColor != testTextBox._bgColor:
        testSuccess = False
    if bgText != testTextBox._bgText:
        testSuccess = False
    if bgTextColor != testTextBox._bgTextColor:
        testSuccess = False
    if inputText != testTextBox._inputText:
        testSuccess = False
    if listInputText != testTextBox._listInputText:
        testSuccess = False
    if inputTextColor != testTextBox._inputTextColor:
        testSuccess = False
    if font != testTextBox._font:
        testSuccess = False
    if callbackFunction != testTextBox._callbackFunction:
        testSuccess = False
    if visible != testTextBox._visible:
        testSuccess = False

    if testSuccess:
        print "Test was successful"
    else:
        print "Test was not successful"

    return testSuccess


def testCheckBox(checkBox):
    pass


def testButton(button):
    pass
