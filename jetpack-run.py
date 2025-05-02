import pygame, os, math
from random import randint

#--------------------------start--------------------------
screen = pygame.display.set_mode((1000, 600))

jump_key = " "
jumping = False
animation_frame = 0
player_movement_speed = 4
collected_coins = 0
speed = 2

#--------------------------functions--------------------------
pygame.font.init()
font = pygame.font.SysFont('arial.tff', 100)
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img,(x,y))

def load_animation(list_path, x_length, y_length, rect, scale=0.25):
    new_list = []
    list_path = pygame.image.load(list_path)
    for y in range(y_length):
        for x in range(x_length):
            img = list_path.subsurface(((rect[0]*x,rect[1]*y),rect))
            img = pygame.transform.scale_by(img, scale)
            new_list.append(img)
    return new_list

class objects(pygame.sprite.Sprite):
    def __init__(self, x, y, col_img, width=None, height=None):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.Surface([width, height])
            self.image.fill(col_img)
        except:
            self.image = col_img
            if type(col_img) == list:
                self.rect = self.image[0].get_rect()
                self.mask = pygame.mask.from_surface(self.image[0])
            else:
                self.rect = self.image.get_rect()
                self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

#--------------------------objects--------------------------
laser_img = pygame.image.load(os.getcwd()+"/images/laser_assets/laser.png")
laser_img = pygame.transform.scale_by(laser_img, 0.5)
lasers = []
laser_spawnrate = 0
current_laser_spawnrate = 300

missile_img = pygame.image.load(os.getcwd()+"/images/rocket_assets/missile.png")
missile_img = pygame.transform.scale_by(missile_img, 2)
missile_img = pygame.transform.rotate(missile_img, 180)
missiles = []
missile_spawnrate = 1000
missile_warning = 0

coin_img = load_animation(os.getcwd()+"/images/coin_assets/coin.png",5,1,(16,16),scale=3)
coins = []
coin_spawnrate = 0
current_coin_spawnrate = 300

gem_img = load_animation(os.getcwd()+"/images/coin_assets/gem.png",4,1,(16,16),scale=3)
gems = []
gem_spawnrate = 0
current_gem_spawnrate = 700

bagground_img = pygame.image.load(os.getcwd()+"/images/bagground_assets/city.png")
bagground_img = pygame.transform.scale_by(bagground_img,3)
bagground = []
bagground.append(objects(0,0,bagground_img))

player_animation = []
player_img = load_animation(os.getcwd() + "/images/player_assets/flying.png", 5, 3, (692,599))
player_animation.append(objects(350, 10, player_img))
player_img = load_animation(os.getcwd() + "/images/player_assets/running.png", 5, 3, (692,599))
player_animation.append(objects(350, 10, player_img))

running = True
while running:
    #--------------------------drawing--------------------------
    screen.fill((74,88,159))
    for bag in bagground:
        screen.blit(bag.image,bag.rect)
    draw_text(f'Coins: {collected_coins}', font, (0,0,0), 10, 10)

    for coin in coins:
        screen.blit(coin.image[math.floor(animation_frame/100*5)],coin.rect)

    for gem in gems:
        screen.blit(gem.image[math.floor(animation_frame/100*4)],gem.rect)

    if player_animation[0].rect.y < 445:
        screen.blit(player_animation[0].image[math.floor(animation_frame/100*15)], player_animation[0].rect)
    else:
        screen.blit(player_animation[1].image[math.floor(animation_frame/100*15)], player_animation[1].rect)

    for laser in lasers:
        screen.blit(laser.image, laser.rect)

    for missile in missiles:
        screen.blit(missile.image, missile.rect)
    
    if missile_warning > 0:
        draw_text("!",font,(255,0,0),980,player_animation[0].rect.y)

    #--------------------------keyboard--------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN and event.unicode == jump_key:
            jumping = True
        elif event.type == pygame.KEYUP and event.unicode == jump_key:
            jumping = False
    
    #--------------------------player--------------------------
    player = player_animation[0]

    if jumping and player.rect.y > 0:
        player.rect.y -= player_movement_speed
    elif not jumping and player.rect.y < 450:
        player.rect.y += player_movement_speed
    
    if animation_frame >= 98:
        animation_frame = 0
    else:
        animation_frame += 1

    #--------------------------lasers--------------------------
    for laser in lasers:
        if laser.rect.x < laser.rect.width * -1:
            lasers.remove(laser)
        else:
            laser.rect.x -= speed
    
    speed += 0.0001*speed

    if laser_spawnrate >= current_laser_spawnrate and len(lasers) < 3:
        lasers.append(objects(1000,randint(0,405),pygame.transform.rotate(laser_img, randint(-45,45))))
        laser_spawnrate = 0
        if not current_laser_spawnrate <= 1:
            current_laser_spawnrate -= current_laser_spawnrate/25
    else:
        laser_spawnrate += 1
    
    for laser in lasers:
        if pygame.sprite.collide_mask(player, laser):
            running = False

    #--------------------------missile--------------------------
    for missile in missiles:
        if missile.rect.x < missile.rect.width*-1:
            missiles.remove(missile)
        else:
            missile.rect.x -= 5 + speed

    
    if missile_spawnrate <= 0 and randint(0,1) == 1:
        if missile_warning > 0:
            missile_warning -= 1
            if missile_warning <= 0:
                missiles.append(objects(1000,player.rect.y,missile_img))
                missile_spawnrate = 700
        else:
            missile_warning = 100
    else:
        missile_spawnrate -= 1
    
    for missile in missiles:
        if pygame.sprite.collide_mask(player,missile):
            running = False

    #--------------------------coins--------------------------
    if coin_spawnrate >= current_coin_spawnrate:
        coins.append(objects(1000,randint(0,550),coin_img))
        coin_spawnrate = 0
    else:
        coin_spawnrate += 1
    
    for coin in coins:
        if coin.rect.x < coin.rect.width*-1:
            coins.remove(coin)
        elif pygame.sprite.collide_mask(player, coin):
            collected_coins += 1
            coins.remove(coin)
        else:
            coin.rect.x -= speed
        for laser in lasers:
            if pygame.sprite.collide_mask(laser,coin):
                coins.remove(coin)

    #--------------------------gems--------------------------
    if gem_spawnrate >= current_gem_spawnrate:
        gems.append(objects(1000,randint(0,550),gem_img))
        gem_spawnrate = 0
    else:
        gem_spawnrate += randint(0,2)
    
    for gem in gems:
        if gem.rect.x < gem.rect.width*-1:
            gems.remove(gem)
        elif pygame.sprite.collide_mask(player,gem):
            collected_coins += 3
            gems.remove(gem)
        else:
            gem.rect.x -= speed

    #--------------------------bagground--------------------------
    for bag in bagground:
        bag.rect.x -= speed

    if bagground[0].rect.x <= -1000 and len(bagground) == 1:
        bagground.append(objects(1000,0,bagground_img))
    elif bagground[0].rect.x <= bagground[0].rect.width*-1:
        bagground.remove(bagground[0])

    player_animation[1].rect.x = player.rect.x
    player_animation[1].rect.y = player.rect.y

    #--------------------------other--------------------------
    pygame.display.update()
    pygame.time.Clock().tick(120)

pygame.quit()