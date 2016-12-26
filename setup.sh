#! /bin/sh
sudo apt-get update \
&& sudo apt-get -y upgrade \
&& sudo apt-get -y install build-essential cmake pkg-config \
&& sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev \
&& sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
&& sudo apt-get -y install libxvidcore-dev libx264-dev \
&& sudo apt-get -y install libgtk2.0-dev \
&& sudo apt-get -y install libatlas-base-dev gfortran \
&& sudo apt-get -y install python2.7-dev python3-dev \
&& sudo mkdir ~/.config/autostart/ \
&& sudo cp ./hello.desktop ~/.config/autostart/ \
&& sudo cp ./rc.local /etc/rc.local \
&& sudo cp ./config_touchscreen.txt /boot/config.txt \
# set audio output to headphone jack
&& sudo amixer cset numid=3 1 \
&& sudo mkdir /etc/X11/xorg.conf.d \
&& sudo cp ./99-calibration /etc/X11/xorg.conf.d/ \
&& git config --global user.email "lucidtronix@gmail.com" \
&& git config --global user.name "Samwell Freeman" \
&& cd ~ \
&& wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip \
&& unzip opencv.zip \
&& wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip \
&& unzip opencv_contrib.zip \
&& cd ~/opencv-3.1.0/ \
&& mkdir build \
&& cd build \
&& cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules -D BUILD_EXAMPLES=ON .. \
&& make -j4 \
&& sudo make install \
&& sudo ldconfig \
&& sudo apt-get -y install arduino \
&& sudo pip install --upgrade python-instagram \
&& sudo pip install --upgrade pi3d \
&& sudo pip install --upgrade feedparser \
&& sudo pip install --upgrade beautifulsoup4 \
&& sudo pip install --upgrade google-api-python-client \
&& sudo shutdown -r now
