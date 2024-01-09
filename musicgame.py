import sys
import pygame
from math import tan, radians
from random import randint
from pygame.locals import QUIT, KEYDOWN, Rect, MOUSEBUTTONDOWN, MOUSEBUTTONUP
import pygame.key
import pygame.mixer
import csv

SIZE_X = 800
SIZE_Y = 500

pygame.init()
pygame.display.set_caption('音ゲー テストプレイ')
Surface = pygame.display.set_mode([SIZE_X, SIZE_Y])
Fpslock = pygame.time.Clock()

Notes = []
Effects = []
LANE_WIDTH = (600 - 100) / 7
score = 0
is_start = False
LAGU_TIME = 80
time = 0
is_bgm_start = False

bgm = pygame.mixer.Sound('C:\Codes\Stores\Pygame\Music_game\芥川龍之介の河童～Candid Friend.mp3')
push_sound = pygame.mixer.Sound('C:\Codes\Stores\Pygame\Music_game\select09.mp3')
hit_sound = pygame.mixer.Sound('C:\Codes\Stores\Pygame\Music_game\pickup03.mp3')

class Note:
    def __init__(self, x, y, destination):
        self.x = x
        self.y = y
        self.destination = destination
        self.speed_x = (destination[0] - self.x) / 80
        self.speed_y = (destination[1] - self.y) / 80
        self.final_r = (LANE_WIDTH - 25) / 2
        self.r = self.final_r * (1/2 + 1/2 * abs(self.y)/400)
        self.delete = False
    def tick(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.r = self.final_r * (1/2 + 1/2 * abs(self.y)/400)
    def draw(self):
        pygame.draw.circle(Surface, (0, 0, 255), (int(self.x), int(self.y)), int(self.r))
    def is_touched(self, effect):
        global score
        if effect.x == self.destination[0] and (400 - 50 < self.y < 400 + 50):
            self.delete = True
            score += 1
            return True
        else:
            return False

class Effect:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.r = 0
        self.color = color
        self.delete = False
    def draw(self):
        pygame.draw.circle(Surface, self.color, (self.x, self.y), self.r, 2)
    def move(self):
        if self.r < 45:
            self.r += 9
        else:
            self.delete = True

class Button:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 50
        self.rect = Rect(0, 0, self.width, self.height)
        self.rect.center = (self.x, self.y)
        font = pygame.font.SysFont(None, 50)
        self.text = font.render(text, True, (0, 128, 200))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.x, self.y)
        self.is_push = False
        self.color = (230, 230, 130)
    def draw(self):
        pygame.draw.rect(Surface, self.color, self.rect)
        Surface.blit(self.text, self.text_rect)
    def is_clicked(self, mouse_pos):
        if self.x - self.width/2 < mouse_pos[0] < self.x + self.width/2 and\
            self.y - self.height/2 < mouse_pos[1] < self.y + self.height/2:
            return True
        else:
            return False
    def clicked(self):
        self.is_push = True
        self.color = (200, 200, 100)
    def released(self):
        self.is_push = False
        self.color = (230, 230, 130)

def bgm_start():
    global is_bgm_start
    if (not is_bgm_start):
        bgm.play()
        is_bgm_start = True

def main():
    #############
    #test_flag = False
    #############
    time_flag = False
    global Notes
    global Effects
    global score
    global is_start
    global time
    keys = [str(i) for i in range(1, 8)]
    sysfont = pygame.font.SysFont(None, 72)
    keyfont = pygame.font.SysFont(None, 50)
    score_message = sysfont.render(str(score), True, (0, 128, 200, 250))
    score_rect = score_message.get_rect()
    score_rect.center = (650, 50)
    keyText = [keyfont.render(k, True, (0, 128, 200, 250)) for k in keys]
    keyText_rect = [k.get_rect() for k in keyText]
    for i, k in enumerate(keyText_rect):
        k.center = (100 + i * LANE_WIDTH + LANE_WIDTH/2, 450)
    start_button = Button(700, 100, 'Start')
    
    '''-----reading-----'''
    music_score = []
    with open('C:\Codes\Stores\Pygame\Music_game\music_score.csv') as f:
        music_score = list(csv.reader(f))
    '''/-----reading-----'''

    '''-----Test-----'''
    '''/-----Test-----'''

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                for i in keys:
                    if event.key == pygame.key.key_code(i):
                        e = Effect(100 + keys.index(i) * LANE_WIDTH + LANE_WIDTH/2, 400, (0, 200, 255))
                        touched = False
                        for note in Notes:
                            touched = note.is_touched(e)
                            if touched:
                                hit_sound.play()
                                e.color = (255, 100, 0)
                                Effects.append(e)
                                break
                        if not touched:
                            push_sound.play()
                            Effects.append(e)
            elif event.type == MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    start_button.clicked()
                    if not is_start:
                        #bgm_start()
                        pass
                    is_start = True
            elif event.type == MOUSEBUTTONUP:
                if start_button.is_push:
                    start_button.released()

        '''-----Draw-----'''
        Surface.fill((0, 0, 0))
        Surface.blit(score_message, score_rect)
        for i in zip(keyText, keyText_rect):
            Surface.blit(i[0], i[1])
        pygame.draw.line(Surface, (0, 255, 0), (100, 400), (600, 400), 2)
        for i in range(8):
            pygame.draw.line(Surface, (0, 255, 0), (SIZE_X/2, -130), (100 + i * LANE_WIDTH, 400), 2)
        for effect in Effects:
            effect.draw()
        for note in Notes:
            note.draw()
        start_button.draw()
        '''/-----Draw-----'''
        
        if is_start:
            if time >= 280 and not time_flag:
                bgm_start()
                time_flag = True
            '''-----tick-----'''
            time += 1
            score_message = sysfont.render(str(score), True, (0, 128, 200, 250))
            if time - 200 > 0:
                '''-------make_music_score-----'''''
                for i, flag in enumerate(music_score[int(time-200)]):
                    if int(flag) == 1:
                        note1 = Note(SIZE_X/2, -130, (100 + i * LANE_WIDTH + LANE_WIDTH/2, 400))
                        Notes.append(note1)
                '''/-------make_music_score-----'''''
            for effect in Effects:
                effect.move()
                if effect.delete:
                    Effects.remove(effect)
            for note in Notes:
                note.tick()
                if note.delete:
                    Notes.remove(note)
            start_button.draw()
            '''/-----tick-----'''

        pygame.display.update()
        Fpslock.tick(60)

if __name__ == '__main__':
    main()