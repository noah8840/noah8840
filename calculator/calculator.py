import pygame
from math import sqrt, cos, sin, tan, acos, asin, atan
from math import degrees as deg
from math import pi as π
from os import getcwd

screen = pygame.display.set_mode((670,500))
screen_width = 500
screen_height = 500
pygame.display.set_caption('Calculator')
icon = pygame.image.load(getcwd() + '/images/icon.png')
pygame.display.set_icon(icon)

pygame.font.init()
text_font = pygame.font.SysFont('arial.ttf',25)
number_font = pygame.font.SysFont('arial.ttf',50)
def draw_text(text,font,pos,color=(0,0,0)):
    render = font.render(text,True,color)
    return screen.blit(render,pos)

class numbers(pygame.sprite.Sprite):
    def __init__(self,rect,display=str,color=(200,200,200)):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.surface.Surface((rect[2],rect[3]))
        self.rect.fill(color)
        self.collision = pygame.rect.Rect(rect)
        self.pos = (rect[0],rect[1])
        self.display = number_font.render(display,True,(0,0,0))
        self.displaystr = display

text = ''
last_text = ''
equal = ''
lines = []

keys = {
    'a':False
}

list_numbers = []
list_numbers.append(numbers(rect=(400+90,10+90*3,80,80),display='0'))
for y in range(3):
    for x in range(3):
        list_numbers.append(numbers(rect=(400+90*x,10+90*y,80,80),display=str(y*3+x+1)))

list_numbers.append(numbers(rect=(400,10+90*3,80,80),display='*'))
list_numbers.append(numbers(rect=(580,10+90*3,80,80),display='/'))
list_numbers.append(numbers(rect=(400,10+90*4,125,80),display='+'))
list_numbers.append(numbers(rect=(535,10+90*4,125,80),display='-'))

running = True
while running:
    screen.fill((255,255,255))

    for number in list_numbers:
        screen.blit(number.rect,number.pos)
        screen.blit(number.display,(number.pos[0]+30,number.pos[1]+30))

    lines = ['Press "t" for tangent | tan(A) = a/b',
             'Press "s" for sine | sin(A) = a/c',
             'Press "c" for cosine | cos(A) = b/c',
             f'Press "d" for degrees',
             f'Press "a" to switch arc mode ({keys['a']})',
             'Press "r" to round',
             'Press "^" to raise number to the power of x',
             'Press "%" for square root',
             'Press "p" for pi']

    for x in range(len(lines)):
        draw_text(lines[x],text_font,(10,screen_height-20-20*x))

    draw_text(f'{last_text} = {equal}',text_font,(10,10))
    draw_text(text,number_font,(10,30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for number in list_numbers:
                if number.collision.collidepoint(pygame.mouse.get_pos()):
                    text += number.displaystr
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                try:
                    last_text = text
                    equal = eval(text)
                    text = equal
                except:
                    pass
                else:
                    text = str(text)
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            elif event.unicode == '%':
                text = 'sqrt(' + text + ')'
            elif event.unicode == '^':
                text = text + '**'
            elif event.unicode == 'c':
                text = 'cos(' + text + ')'
            elif event.unicode == 's':
                text = 'sin(' + text + ')'
            elif event.unicode == 't':
                text = 'tan(' + text + ')'
            elif event.unicode == 'd':
                text = 'deg(' + text + ')'
            elif event.unicode == 'p':
                text += 'π'
            elif event.unicode == 'r':
                text = 'round(' + text + ')'
            elif event.unicode == 'a':
                if keys['a']:
                    keys['a'] = False
                else:
                    keys['a'] = True
            elif event.unicode == ',':
                text += '.'
            elif event.unicode in ['0','1','2','3','4','5','6','7','8','9','+','-','*','/','.','(',')']:
                text += event.unicode
            if event.unicode in ['c','s','t'] and keys['a']:
                text = 'a' + text

    pygame.time.Clock().tick(60)
    pygame.display.update()
pygame.quit()