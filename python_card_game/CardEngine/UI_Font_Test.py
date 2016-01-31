import UI
import sys
import pygame
from pygame.locals import *

pygame.font.init()

arial = pygame.font.Font(pygame.font.match_font('arial'), 14)
arialBlack = pygame.font.Font(pygame.font.match_font('arialblack'), 14)
calibri = pygame.font.Font(pygame.font.match_font('calibri'), 14)
cambria = pygame.font.Font(pygame.font.match_font('cambria'), 14)
courierNew = pygame.font.Font(pygame.font.match_font('couriernew'), 14)
gentiumBookBasic = pygame.font.Font(pygame.font.match_font('gentiumbookbasic'), 14)
segoeUI = pygame.font.Font(pygame.font.match_font('segoeui'), 14)
timesNewRoman = pygame.font.Font(pygame.font.match_font('timesnewroman'), 14)
verdana = pygame.font.Font(pygame.font.match_font('verdana'), 14)
vrinda = pygame.font.Font(pygame.font.match_font('vrinda'), 14)


def test():
    pygame.init()
    screen = pygame.display.set_mode((600, 450), 0, 32)
    pygame.display.set_caption('Testing different UI elements')

    background = pygame.Surface(screen.get_size())
    background.convert()
    background_color = (80, 150, 80)
    background.fill(background_color)

    # I would use arial, calibri, gentiumBookBasic, segoeUI, and timesNewRoman
    text1 = UI.Text(rect=pygame.Rect(30, 30, 60, 30), text='1. Hello', font=arial)
    # text2 = UI.Text(rect = pygame.Rect(30,60,60,30), text = '2. Hello',font = arialBlack)
    text3 = UI.Text(rect=pygame.Rect(30, 60, 60, 30), text='3. Hello', font=calibri)
    # text4 = UI.Text(rect = pygame.Rect(30,120,60,30), text = '4. Hello',font = cambria)
    # text5 = UI.Text(rect = pygame.Rect(30,150,60,30), text = '5. Hello',font = courierNew)
    text6 = UI.Text(rect=pygame.Rect(30, 90, 60, 30), text='6. Hello', font=gentiumBookBasic)
    text7 = UI.Text(rect=pygame.Rect(30, 120, 60, 30), text='7. Hello', font=segoeUI)
    text8 = UI.Text(rect=pygame.Rect(30, 150, 60, 30), text='8. Hello', font=timesNewRoman)
    # text9 = UI.Text(rect = pygame.Rect(30,270,60,30), text = '9. Hello',font = verdana)
    # text10 = UI.Text(rect = pygame.Rect(30,180,60,30), text = '10. Hello',font = vrinda)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                return

        screen.blit(background, (0, 0))
        text1.render(screen)
        # text2.render(screen)
        text3.render(screen)
        # text4.render(screen)
        # text5.render(screen)
        text6.render(screen)
        text7.render(screen)
        text8.render(screen)
        # text9.render(screen)
        # text10.render(screen)

        pygame.display.flip()

        pygame.time.delay(20)
