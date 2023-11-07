
"""
Creates random alarms. If time given = T min, this will generate T/2 alarms. 
"""


import sys
import random
import pygame
from pygame.locals import QUIT, K_BACKSPACE, KEYDOWN, MOUSEBUTTONDOWN, K_RETURN


pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (100, 200, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pygame.font.SysFont("Verdana", 20)
small_font = pygame.font.SysFont("Verdana", 15)


pygame.display.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Random Alarm")

input_rect = pygame.Rect(200, 200, 140, 32)

T0 = 10 # time in minutes
T = T0*60*1000 # time in milliseconds
N_ALARMS = int(T0/2)


clock = pygame.time.Clock()
alarm = pygame.USEREVENT +0
pygame.time.set_timer(alarm, 10**7)


times_up = pygame.USEREVENT +1
pygame.time.set_timer(times_up,T)


USER_TEXT = ''
input_rect = pygame.Rect(150, 200, 140, 32)
input_req = font.render('T = ', True, WHITE)
start_rect = pygame.Rect(150,300,150,40)



COLOR = RED
ACTIVE = False
HAVE_STARTED = False
RUN = True
i=0
ALARM_MESSAGE = ''
alarming = font.render(ALARM_MESSAGE, True, WHITE)
INFO_TEXT_1 = 'Input the time T in minutes you'
INFO_TEXT_2 = 'wish to focus for and select start.'
INFO_TEXT_3 = 'This will generate T/2 random alarms,'
INFO_TEXT_4 = 'and a final alarm when the T minutes are up.'
while RUN:
    DISPLAYSURF.fill(BLACK)


    if HAVE_STARTED is False:
        pygame.draw.rect(DISPLAYSURF, COLOR, input_rect)
        pygame.draw.rect(DISPLAYSURF, GREEN, start_rect)

        input_surface = font.render(USER_TEXT, True, (255, 255, 255))
        start_surface = font.render('START', True, (255, 255, 255))
        info_surface_1 = small_font.render(INFO_TEXT_1, True, (255,255,255) )
        info_surface_2 = small_font.render(INFO_TEXT_2, True, (255,255,255) )
        info_surface_3 = small_font.render(INFO_TEXT_3, True, (255,255,255) )
        info_surface_4 = small_font.render(INFO_TEXT_4, True, (255,255,255) )
        DISPLAYSURF.blit(input_surface, (input_rect.x+5, input_rect.y+5))
        DISPLAYSURF.blit(start_surface, (start_rect.x+35, start_rect.y+10))
        DISPLAYSURF.blit(info_surface_1, (start_rect.x-100, start_rect.y-280))
        DISPLAYSURF.blit(info_surface_2, (start_rect.x-100, start_rect.y-260))
        DISPLAYSURF.blit(info_surface_3, (start_rect.x-100, start_rect.y-240))
        DISPLAYSURF.blit(info_surface_4, (start_rect.x-100, start_rect.y-220))
        
        DISPLAYSURF.blit(input_req,(100,200))

    else:
        setting = font.render('T = ' + str(USER_TEXT), True, WHITE)
        DISPLAYSURF.blit(setting,(100,100))
        DISPLAYSURF.blit(alarming,(100,200))


    pygame.display.update()

    for event in pygame.event.get():

        #=====================
        if event.type == MOUSEBUTTONDOWN and not HAVE_STARTED:
            ACTIVE =input_rect.collidepoint(event.pos)

            if start_rect.collidepoint(event.pos):
                HAVE_STARTED = True
                start_ticks=pygame.time.get_ticks()
                T0 = int(USER_TEXT) # time in minutes
                T = T0*60*1000 # time in milliseconds
                N_ALARMS = int(T0/2)

                ts = sorted([random.randint(0,T) for n in range(N_ALARMS)])
                mins_ts = [i/1000/60 for i in ts]
                diffs = [ts[0]]
                diffs.extend([ts[i]-ts[i-1] for i in range(1,N_ALARMS)])
                pygame.time.set_timer(alarm, diffs[0])
                pygame.time.set_timer(times_up, T)

                diffs.append(0)
        if event.type == KEYDOWN and not HAVE_STARTED:

            # Check for backspace
            if event.key == K_BACKSPACE:

                # get text input from 0 to -1 i.e. end.
                USER_TEXT = USER_TEXT[:-1]

            # Unicode standard is used for string
            # formation
            elif event.key == K_RETURN:
                HAVE_STARTED = True
                start_ticks=pygame.time.get_ticks()
                T0 = int(USER_TEXT) # time in minutes
                T = T0*60*1000 # time in milliseconds
                N_ALARMS = int(T0/2)
            else:
                USER_TEXT += event.unicode

        #============

        if event.type == times_up:
            pygame.mixer.Sound('end_bell.wav').play()
            pygame.time.wait(1000)
            pygame.quit()
            sys.exit()

        if event.type == alarm and HAVE_STARTED:
            pygame.mixer.Sound('bell.wav').play()
            i+=1
            pygame.time.set_timer(alarm, diffs[i])

            t_remaining = T-pygame.time.get_ticks()
            t_rem_mins = t_remaining/1000/60
            t_min = int(t_rem_mins)
            T_SECS =int(( t_rem_mins - t_min )*60)
            if len(str(T_SECS))==1:
                T_SECS = '0'+ str(T_SECS)
            ALARM_MESSAGE = f'Time left: {t_min}:{T_SECS}'
            alarming = font.render(ALARM_MESSAGE, True, WHITE)




        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if ACTIVE:
        COLOR = BLUE
    else:
        COLOR = RED

    clock.tick(60)
    pygame.display.update()
    FramePerSec.tick(FPS)
