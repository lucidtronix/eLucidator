# Textured Cube
# Written by Samwell Freeman
# April 2016

import os
import pi3d

display = pi3d.Display.create(x=50, y=50)
shader = pi3d.Shader("uv_light")

img_dir = '/home/sam/Dropbox/Photos/friends/'
imgs = [img for img in os.listdir(img_dir) if img[0] != '.']
cur_img = 0
tex = pi3d.Texture(img_dir+imgs[cur_img])
tex2 = pi3d.Texture(img_dir+imgs[cur_img+1])
tex3 = pi3d.Texture(img_dir+imgs[cur_img+2])


box = pi3d.Cuboid(x=0, y=0, z=2.2)
box.set_draw_details(shader,[tex,tex2,tex3])

ball = pi3d.Sphere(x=-1.5, y=0, z=2.6, radius =0.5)
ball.set_draw_details(shader,[tex3])

mykeys = pi3d.Keyboard()
while display.loop_running():

  box.rotateIncX(0.07)
  box.rotateIncY(0.091)
  box.rotateIncZ(0.091)
  box.draw()

  ball.rotateIncY(0.3)
  ball.draw()

  k = mykeys.read()
  if k == 27:
    mykeys.close()
    display.destroy()
    break
  elif k == 119:
  	cur_img += 1
  	ball.set_draw_details(shader,[tex])
  	tex = pi3d.Texture(img_dir+imgs[cur_img])
  	box.set_draw_details(shader,[tex])


