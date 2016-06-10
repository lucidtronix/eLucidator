#! /bin/sh
cp config_touchscreen.txt /boot/config.txt \
&& mkdir /etc/X11/xorg.conf.d \
&& cp 99-calibration /etc/X11/xorg.conf.d/ \
&& pip install python-instagram \
&& pip install pi3d