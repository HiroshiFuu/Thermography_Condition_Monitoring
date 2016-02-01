sudo apt-get install python-opencv python-numpy
sudo apt-get install python-pygame
sudo apt-get install qt4-dev-tools
sudo mkdir tempLepton
cd tempLepton
sudo git clone https://github.com/groupgets/pylepton.git
cd pylepton
sudo python setup.py install
cd ..
cd ..
sudo rm -rf tempLepton
