import pygame
from os import getcwd

screen = pygame.display.set_mode((700,500))
pygame.display.set_caption('Frequency calculator')
pygame.display.set_icon(pygame.image.load(getcwd()+'/images/icon.png'))

pygame.font.init()
text_font = pygame.font.SysFont('arial.ttf',20)
numbers_font = pygame.font.SysFont('arial.ttf',15)
def draw_text(text,font,pos):
    render = font.render(text,True,(0,0,0))
    return screen.blit(render,pos)

text = '1 2 2 3 3 3 4 4 4 4'
numbers = [1,2,2,3,3,3,4,4,4,4]
new_numbers = []
unique_numbers = [1,2,3,4]
frame = 0

running = True
while running:
    screen.fill((255,255,255))

    if frame >= 100:
        draw_text(text,text_font,(10,5))
        frame = 0
    elif frame >= 50:
        draw_text(text + '|',text_font,(10,5))
    else:
        draw_text(text,text_font,(10,5))
    frame += 1

    pygame.draw.line(screen,(0,0,0),(20,480),(460,480))
    pygame.draw.line(screen,(0,0,0),(20,480),(20,30))

    for x in range(25):
        pygame.draw.line(screen,(0,0,0),(475,x*20+5),(475,x*20+15))

    y = 0
    for x in range(len(unique_numbers)):
        pygame.draw.aaline(screen,(0,0,0),(20+x*(450/len(unique_numbers)),480-y),(20+(x+1)*(450/len(unique_numbers)),480-(y+numbers.count(unique_numbers[x])/len(numbers)*450)),blend=1)
        y += numbers.count(unique_numbers[x])/len(numbers)*450
    for x in range(len(unique_numbers)):
        draw_text(f'{unique_numbers[x]}',numbers_font,(20+(x+1)*(440/len(unique_numbers)),485))
    for x in range(11):
        draw_text(f'{x*10}%',numbers_font,(0,475-x*45))

    y = 0
    for x in range(len(unique_numbers)):
        draw_text(f'{unique_numbers[x]} | {y+numbers.count(unique_numbers[x])/len(numbers)*100}%',text_font,(500,10+x*20))
        y += numbers.count(unique_numbers[x])/len(numbers)*100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                new_numbers = list(text + ' ')
                numbers = []
                x = 0
                while len(new_numbers) >= 1:
                    y = new_numbers.index(' ')
                    numbers.append('')
                    for n in range(y):
                        numbers[x] += new_numbers[0]
                        del new_numbers[0]
                    del new_numbers[0]
                    x += 1
                y = 0
                for x in range(len(numbers)):
                    try:
                        numbers[x-y] = int(numbers[x-y])
                    except:
                        del numbers[x-y]
                        y += 1
                numbers.sort()
                unique_numbers = list(set(numbers))

            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode

    pygame.time.Clock().tick(60)
    pygame.display.update()
pygame.quit()