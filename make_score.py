import sys
import pygame
import pygame.mixer
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_s
import csv
from random import randint

pygame.init()
pygame.key.set_repeat()
Surface = pygame.display.set_mode([100, 100])
Fpslock = pygame.time.Clock()

bgm = pygame.mixer.Sound('芥川龍之介の河童～Candid Friend.mp3')

def main():
    count = 0
    start = False
    end = False
    time = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    time.append(count)
                    print(count)
                if event.key == K_s:
                    start = True
                    bgm.play()
                    print('Start!')

        if start:
            count += 1
            if count > 30 * 60:
                bgm.fadeout(2000)
                end = True

        if end:
            print(time)
            break
        pygame.display.update()
        Fpslock.tick(60)
    
    data = [[0, 0, 0, 0, 0, 0, 0] for _ in range(30 * 60)]
    
    w = randint(0, 6)
    for index in time:
        data[index][w] = 1
        w = randint(0, 6)
    
    
    with open('music_score.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for d in data:
            writer.writerow(d)


if __name__ == '__main__':
    main()