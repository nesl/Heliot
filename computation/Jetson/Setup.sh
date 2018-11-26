
# git, will be installed


echo Setting up Jetson environment for Heliot

# Installing pip3
sudo apt install python3-pip


# Installing Tensorflow
# Nvidia Instructions are here: https://docs.nvidia.com/deeplearning/dgx/install-tf-jetsontx2/index.html
pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp33 tensorflow-gpu


#Install Jupyter
#sudo pip3 install pyzmq==17.0.0
#sudo pip3 install jupyter-core
#sudo pip3 install jupyter


# Install msgpack rpc
pip3 install msgpack-rpc-python


# Install matplotlib
#pip3 install matplotlib



