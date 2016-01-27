sudo apt-get install python-opencv python-numpy
sudo apt-get install python-pygame
sudo mkdir tempLepton
cd tempLepton
sudo git clone https://github.com/groupgets/pylepton.git
cd pylepton
sudo python setup.py install
cd ..
cd ..
sudo rm -rf tempLepton
