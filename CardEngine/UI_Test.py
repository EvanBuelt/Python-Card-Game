import UI
import sys
import pygame


def display_text_input(textbox_object):
    print "Got text from ", textbox_object, " and text is: ", textbox_object.inputText
    textbox_object.inputText = ''


def display_checked(checkbox_object):
    print "Checkbox ", checkbox_object, " has checked: ", checkbox_object.checked


def test():
    my_test_engine = TestEngine(400, 300, 'Testing different UI elements')

    # Create UI elements
    text1 = UI.Text(rect=pygame.Rect(30, 30, 60, 20), text='Hello')
    text2 = UI.Text(rect=pygame.Rect(30, 65, 60, 20), text='World!', bg_color=(200, 200, 200, 50))
    text3 = UI.Text(rect=pygame.Rect(30, 100, 60, 20), text='0', bg_color=(70, 200, 70))
    textbox1 = UI.TextBox(rect=pygame.Rect(100, 30, 180, 20), background_text='Username')
    textbox2 = UI.TextBox(rect=pygame.Rect(100, 65, 180, 20), background_text='Password')
    checkbox1 = UI.CheckBox(rect=pygame.Rect(290, 30, 14, 14))
    checkbox2 = UI.CheckBox(rect=pygame.Rect(290, 65, 14, 14))
    button1 = UI.Button(rect=pygame.Rect(310, 30, 70, 20), text='Press me')
    button2 = UI.Button(rect=pygame.Rect(310, 65, 50, 20), text='Don\'t')
    text4 = UI.Text(rect=pygame.Rect(100, 90, 120, 20), text='')

    textbox1.set_callback(display_text_input)
    textbox2.set_callback(display_text_input)

    checkbox1.set_callback(display_checked)
    checkbox2.set_callback(display_checked)

    # Add UI elements to list
    my_test_engine.add_ui_element(text1)
    my_test_engine.add_ui_element(text2)
    my_test_engine.add_ui_element(text3)
    my_test_engine.add_ui_element(textbox1)
    my_test_engine.add_ui_element(textbox2)
    my_test_engine.add_ui_element(checkbox1)
    my_test_engine.add_ui_element(checkbox2)
    my_test_engine.add_ui_element(button1)
    my_test_engine.add_ui_element(button2)
    my_test_engine.add_ui_element(text4)

    # Test setting and getting of each UI element (only one per class is necessary)
    test_text(text1)
    test_textbox(textbox1)

    text1.rect = pygame.Rect(30, 20, text1.rect.width, text1.rect.height)
    text2.visible = False

    while True:
        my_test_engine.update()
        my_test_engine.render()

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
    def __init__(self, width=400, height=300, name='Test Engine', background_color=(80, 150, 80)):
        # Initialize screen
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption(name)

        # Create background surface
        self.background = pygame.Surface(self.screen.get_size())
        self.background.convert()
        self.backgroundColor = background_color
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

    def add_ui_element(self, ui_element):
        self.screenUIElements.append(ui_element)


# Functions for testing each UI Element to ensure element works properly
def test_text(ui_text):
    if not isinstance(ui_text, UI.Text):
        print 'Object not an instance of text, or derived instance of text'
        return

    test_success = True
    # Get data from text class
    text = ui_text.text
    rect = ui_text.rect
    font = ui_text.font
    foreground_color = ui_text.fgColor
    background_color = ui_text.bgColor
    visible = ui_text.visible

    # Print original contents.
    print ''
    print ui_text
    print ui_text.text
    print ui_text.rect
    print ui_text.font
    print ui_text.fgColor
    print ui_text.bgColor
    print ui_text.visible
    print ''

    # Test each property.
    ui_text.text = ui_text.text
    ui_text.rect = ui_text.rect
    ui_text.font = ui_text.font
    ui_text.fgColor = ui_text.fgColor
    ui_text.bgColor = ui_text.bgColor
    ui_text.visible = ui_text.visible

    # Print contents after using in-built properties.
    print ''
    print ui_text.text
    print ui_text.rect
    print ui_text.font
    print ui_text.fgColor
    print ui_text.bgColor
    print ui_text.visible
    print ''

    # Test if data after testing properties is same as old data
    if text != ui_text.text:
        test_success = False
    if rect != ui_text.rect:
        test_success = False
    if font != ui_text.font:
        test_success = False
    if foreground_color != ui_text.fgColor:
        test_success = False
    if background_color != ui_text.bgColor:
        test_success = False
    if visible != ui_text.visible:
        test_success = False

    if test_success:
        print "Test was successful"
    else:
        print "Test was not successful"

    return test_success


def test_textbox(ui_textbox):
    if not isinstance(ui_textbox, UI.TextBox):
        print 'Object not an instance of textbox, or derived instance of textbox'
        return

    test_success = True

    # Get data from textbox class
    rect = ui_textbox.rect
    background_color = ui_textbox.bgColor
    background_text = ui_textbox.bgText
    background_text_color = ui_textbox.bgTextColor
    input_text = ui_textbox.inputText
    list_input_text = ui_textbox.listInputText
    input_text_color = ui_textbox.inputTextColor
    font = ui_textbox.font
    callback_function = ui_textbox.callbackFunction
    visible = ui_textbox.visible

    # Print original contents.
    print ''
    print ui_textbox
    print ui_textbox.rect
    print ui_textbox.bgColor
    print ui_textbox.bgText
    print ui_textbox.bgTextColor
    print ui_textbox.inputText
    print ui_textbox.listInputText
    print ui_textbox.inputTextColor
    print ui_textbox.font
    print ui_textbox.callbackFunction
    print ui_textbox.visible
    print ''

    # Test each property.
    ui_textbox.rect = ui_textbox.rect
    ui_textbox.bgText = ui_textbox.bgText
    ui_textbox.bgColor = ui_textbox.bgColor
    ui_textbox.inputText = ui_textbox.inputText
    ui_textbox.inputTextColor = ui_textbox.inputTextColor
    ui_textbox.bgTextColor = ui_textbox.bgTextColor
    ui_textbox.font = ui_textbox.font
    ui_textbox.callbackFunction = ui_textbox.callbackFunction
    ui_textbox.visible = ui_textbox.visible

    # Print contents after using in-built properties.
    print ''
    print ui_textbox.rect
    print ui_textbox.bgColor
    print ui_textbox.bgText
    print ui_textbox.bgTextColor
    print ui_textbox.inputText
    print ui_textbox.listInputText
    print ui_textbox.inputTextColor
    print ui_textbox.font
    print ui_textbox.callbackFunction
    print ui_textbox.visible
    print ''

    # Test if data after testing properties is same as old data
    if rect != ui_textbox.rect:
        test_success = False
    if background_color != ui_textbox.bgColor:
        test_success = False
    if background_text != ui_textbox.bgText:
        test_success = False
    if background_text_color != ui_textbox.bgTextColor:
        test_success = False
    if input_text != ui_textbox.inputText:
        test_success = False
    if list_input_text != ui_textbox.listInputText:
        test_success = False
    if input_text_color != ui_textbox.inputTextColor:
        test_success = False
    if font != ui_textbox.font:
        test_success = False
    if callback_function != ui_textbox.callbackFunction:
        test_success = False
    if visible != ui_textbox.visible:
        test_success = False

    if test_success:
        print "Test was successful"
    else:
        print "Test was not successful"

    return test_success


def test_checkbox(ui_checkbox):
    return ui_checkbox


def test_button(ui_button):
    return ui_button
