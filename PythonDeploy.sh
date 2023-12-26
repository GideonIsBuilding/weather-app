#!/usr/bin/bash

source .env

new_directory="Weather App"

green_echo() {
    echo -e "\e[32m$1\e[0m"
}

red_echo() {
    echo -e "\e[31m$1\e[0m"
}

#----------------------------
# Update and upgrade packages
#----------------------------
green_echo "Updating and upgrading packages..."
sudo apt update && sudo apt upgrade -y

#------------
# Install Git
#------------
green_echo "Installing Git..."
sudo apt install git -y

#---------------------------------------------
# Create and Cd into new directory for the app
#---------------------------------------------
mkdir -p /home/vagrant/"$new_directory" && \
chmod 700 /home/vagrant/"$new_directory" && \
cd /home/vagrant/"$new_directory" || exit

#---------------
# Clone Git repo
#---------------
green_echo "Cloning Git repo..."
git clone https://github.com/GideonIsBuilding/weather-app.git

#-----------------------------------------------
# Check if Python3 is installed, else install it
#-----------------------------------------------
if command -v python3 ---version &> /dev/null; then
    green_echo "Python3 is installed and present"
    green_echo "Installing pip for Python3..."
    sudo apt install python3-pip
else
    red_echo "Python3 is not installed. Now installing..."
    sudo apt install build-essential software-properties-common -y
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    green_echo "Installing Python3 and pip for Python3..."
    sudo apt install python3.11 python3-pip -y
fi

#---------------------------------------------------
# Install all requirements for the python app to run
#---------------------------------------------------
green_echo "Installing Python app requirements..."
python3 -m pip install -r requirements.txt

# --------------------------
# Run the Python application
# --------------------------
green_echo "Running the Python application..."
python3 -m streamlit run AppWeather.py 