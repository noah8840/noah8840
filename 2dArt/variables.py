from functions import *

color = (0,0,0)
frame = 0
screen_rect = [1000,800]

mouse = False
mouse_pos = 0

pixel_rect = (20,20)
pick_color = False
user_input = "0,0,0"
user_input_pixel = '20,20'
pick_pixel = False

transparrency = '100'
pick_trans = False

current_image = 0
images = []

colors_list = []
f = open('colors.txt','r')
for x in f:
    try:
        eval(x)
    except:
        pass
    else:
        if type(eval(x)) == tuple:
            if len(colors_list) > 5:
                colors_list.append(colors(eval(x),(900,170+90*(len(colors_list)-6))))
            else:
                colors_list.append(colors(eval(x),(810,170+90*len(colors_list))))
f.close()

f = open('colors.txt','a')

text_list = {
    'RGB|' : texts(f'RGB: {user_input}|',font,(0,0,0),810,10),
    'RGB' : texts(f'RGB: {user_input}',font,(0,0,0),810,10),
    'Pixel|' : texts(f'Pixel: {user_input_pixel}|',font,(0,0,0),810,30),
    'Pixel' : texts(f'Pixel: {user_input_pixel}',font,(0,0,0),810,30),
    'Save color' : texts('Save color',font,(0,0,0),810,50),
    'Delete color' : texts('Delete color',font,(0,0,0),810,70),
    'New image' : texts(f'New image ({len(images)})',font,(0,0,0),810,90),
    'Remove image' : texts('Remove image',font,(0,0,0),810,110),
    'Trans' : texts(f'Transparrency: {transparrency}',font,(0,0,0),810,130),
    'Trans|' : texts(f'Transparrency: {transparrency}|',font,(0,0,0),810,130),
    'Download' : texts('Download',font,(0,0,0),810,150),
    'Image number' : texts(f'Image: {current_image+1} <- ->',font,(0,0,0),10,10)
}

new_image(images,text_list)