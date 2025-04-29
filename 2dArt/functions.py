import pygame
from math import floor
from os import getcwd
from os.path import isfile

class colors():
    def __init__(self,color,pos):
        self.color = color
        self.pos = pos
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.pos,(80,80)))
        return pygame.draw.rect(screen,(0,0,0),(self.pos,(80,80)),5)

pygame.font.init()
font = pygame.font.SysFont('arial.ttf',25)
def text(text,font,color,pos,screen):
    img = font.render(text, True, color)
    return screen.blit(img,pos)

class texts():
    def __init__(self,text,font,color,x,y):
        self.text = text
        self.font = font
        self.color = color
        self.pos = [x,y]
    def draw(self,screen):
        return text(self.text,self.font,self.color,self.pos,screen)

def click(object):
    return pygame.Rect.collidepoint(object,pygame.mouse.get_pos())

def overlay(image_list,image_number,transparrency,screen):
    surface = image_list[image_number].copy()
    try:
        surface.set_alpha(int(transparrency))
    except:
        surface.set_alpha(100)
    return screen.blit(surface,(0,0))

def new_image(images,text_list):
    new_image = pygame.Surface([800,800],pygame.SRCALPHA)
    new_image.fill((255,255,255,0))
    images.append(new_image)
    text_list['New image'].text = f'New image ({len(images)})'

def download(images,pixel_rect,screen_rect,path):
    image_len = len(images)*800
    image = pygame.Surface((image_len,800),pygame.SRCALPHA)
    image.fill((0,0,0,0))

    for img in range(len(images)):
        image.blit(images[img],(img*800,0))

    x = 1
    temp = path
    while isfile(temp):
        temp = path
        file = temp[-4:]
        temp = temp[:-4]
        temp = temp + str(x)
        temp = temp + file
        x += 1
    path = temp
    
    x = screen_rect[0]/pixel_rect[0]*len(images)
    y = screen_rect[1]/pixel_rect[1]
    image = pygame.transform.scale(image,(x,y))

    pygame.image.save(image,path)