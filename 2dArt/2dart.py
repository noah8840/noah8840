from variables import *

screen = pygame.display.set_mode(screen_rect)

running = True
while running:

    if color == (255,255,255):
        color = (255,255,255,0)

    screen.fill((255,255,255))
    pygame.draw.line(screen,(0,0,0),(800,800),(800,0),2)

    pygame.draw.rect(screen,(255,255,255),((802,0),(300,800)))
    pygame.draw.rect(screen,color,(810,710,80,80))
    pygame.draw.rect(screen,(0,0,0),(810,710,80,80),5)

    screen.blit(images[current_image],(0,0))
    if current_image != 0:
        overlay(images,current_image-1,transparrency,screen)
    
    for obj in colors_list:
        obj.draw(screen)

    text_list['Save color'].draw(screen)
    text_list['Delete color'].draw(screen)

    text_list['Image number'].text = f'Image: {current_image+1} <- ->'
    text_list['Image number'].draw(screen)
    text_list['New image'].draw(screen)
    text_list['Remove image'].draw(screen)
    text_list['Download'].draw(screen)

    if frame < 100 and pick_trans:
        text_list['Trans|'].draw(screen)
    else:
        text_list['Trans'].draw(screen)
    
    if frame < 100 and pick_color:
        text_list['RGB|'].draw(screen)
    else:
        text_list['RGB'].draw(screen)
    if frame < 100 and pick_pixel:
        text_list['Pixel|'].draw(screen)
    else:
        text_list['Pixel'].draw(screen)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if click(text_list['RGB'].draw(screen)):
                pick_color = True
            elif click(text_list['Pixel'].draw(screen)):
                pick_pixel = True
            elif click(text_list['Save color'].draw(screen)):
                f.write('\n' + str(color))
                if len(colors_list) > 5:
                    colors_list.append(colors(color,(900,170+90*(len(colors_list)-6))))
                else:
                    colors_list.append(colors(color,(810,170+90*len(colors_list))))
            elif click(text_list['Delete color'].draw(screen)):
                with open('colors.txt','r') as file:
                    new_file = file.readlines()
                if new_file:
                    new_file.pop()
                with open('colors.txt','w') as file:
                    file.writelines(new_file)
                if colors_list:
                    colors_list.pop()
            elif click(text_list['New image'].draw(screen)):
                new_image(images,text_list)
            elif click(text_list['Trans'].draw(screen)):
                pick_trans = True
            elif click(text_list['Remove image'].draw(screen)):
                if len(images) > 1:
                    images = images[:-1]
                    text_list['New image'].text = f'New image ({len(images)})'
            elif click(text_list['Download'].draw(screen)):
                download(images,pixel_rect,screen_rect,getcwd() + '/images/new_image.png')

            for obj in colors_list:
                if click(obj.draw(screen)):
                    color = obj.color
                    user_input = str(color)
                    user_input = user_input[1:-1]
                    text_list['RGB|'].text = f'RGB: {user_input}|'
                    text_list['RGB'].text = f'RGB: {user_input}'

            mouse = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse = False
        if pick_color:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        user_input_list = [int(i.strip()) for i in user_input.strip('()').split(',')]
                        tuple(user_input_list)
                    except:
                        pass
                    else:
                        color = tuple(user_input_list)
                        pick_color = False

                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
                text_list['RGB|'].text = f'RGB: {user_input}|'
                text_list['RGB'].text = f'RGB: {user_input}'
        elif pick_pixel:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        user_input_list = [int(i.strip()) for i in user_input_pixel.strip('()').split(',')]
                        tuple(user_input_list)
                    except:
                        pass
                    else:
                        pixel_rect = tuple(user_input_list)
                        pick_pixel = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input_pixel = user_input_pixel[:-1]
                else:
                    user_input_pixel += event.unicode
                text_list['Pixel|'].text = f'Pixel: {user_input_pixel}|'
                text_list['Pixel'].text = f'Pixel: {user_input_pixel}'
        elif pick_trans:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pick_trans = False
                elif event.key == pygame.K_BACKSPACE:
                    transparrency = transparrency[:-1]
                else:
                    transparrency += event.unicode
                text_list['Trans|'].text = f'Transparrency: {transparrency}|'
                text_list['Trans'].text = f'Transparrency: {transparrency}'

        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RIGHT,pygame.K_UP]:
                if not current_image+1 == len(images):
                    current_image += 1
            elif event.key in [pygame.K_LEFT,pygame.K_DOWN]:
                if not current_image == 0:
                    current_image -= 1

    if mouse and pygame.mouse.get_pos()[0] < 800:
        mouse_pos = (floor(pygame.mouse.get_pos()[0]/pixel_rect[0])*pixel_rect[0],floor(pygame.mouse.get_pos()[1]/pixel_rect[1])*pixel_rect[1])
        pygame.draw.rect(images[current_image],color,(mouse_pos,pixel_rect))
    if frame < 200:
        frame += 1
    else:
        frame = 0
    
    pygame.display.update()
    pygame.time.Clock().tick(120)

pygame.quit()