# Shapes Textured by Instagram
# Written by Samwell Freeman
# April 2016

import os
import pi3d

from instagram_query import get_instagram_api, InstagramQuery, InstagramMedia


api = get_instagram_api()
display = pi3d.Display.create(x=50, y=50)
shader = pi3d.Shader("uv_light")

img_dir = '/home/sam/Dropbox/Photos/friends/'
imgs = [img for img in os.listdir(img_dir) if img[0] != '.']
cur_img = 0

images = []
tex = pi3d.Texture(img_dir+imgs[cur_img])

box = pi3d.Cuboid(x=0, y=0, z=2.2)
box.set_draw_details(shader,[tex])

ball = pi3d.Sphere(x=-1.5, y=0, z=2.6, radius =0.5)
ball.set_draw_details(shader,[tex])

mykeys = pi3d.Keyboard()

cur_user = 0
users = ["meoremy", "samwell3", "omg.rb.md", "moistbuddha", "butterknuckles", "peanutbutterpear"]
cur_tag = 0
tags = ["magic egg",  "fractals", "news", "beauty", "time", "reflection"]
loaded = []

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
  elif k ==  ord('w'):
  	iq = InstagramQuery(images, tags[cur_tag], "tag", api)
	iq.start()
	cur_tag += 1
	if cur_tag > len(tags):
		cur_tag = 0
  elif k == ord('p'):
  	if len(images) > 0:
  		ball.set_draw_details(shader,[tex])

  		tex = pi3d.Texture(images[cur_img].pil_image)
  		box.set_draw_details(shader,[tex])

  		cur_img += 1
  		if cur_img >= len(images):
  			cur_img = 0


