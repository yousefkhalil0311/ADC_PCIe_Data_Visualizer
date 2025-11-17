Linux program to read streamed ADC samples from an XDMA block in an FPGA over PCIe. Data will be stored into shared memory and to the SSD via C++ and visualized via Python. During development, the following hardware was used:
Nvidia Orin GPU running Ubuntu 22.04
iWave G35M XCZU19EG SOM
Custom carrier board & system (undisclosed).

Instructions to get started:

1) Use the following linux commands to install python 3.12:

    sudo apt update;
    sudo apt install software-properties-common -y;
    sudo add-apt-repository ppa:deadsnakes/ppa;
    sudo apt update;
    sudo apt install python3.12 python3.12-venv python3.12-dev;

2) Navigate to the folder in which you would like to clone the repository and clone the repository

    git clone https://github.com/yousefkhalil0311/ADC_PCIe_Data_Visualizer.git

3) Navigate to the ADC_PCIe_Data_Visualizer folder

    cd ADC_PCIe_Data_Visualizer

3) Create a virtual environment

    python3.12 -m venv venv

4) Activate the virtual environment

    source venv/bin/activate

5) Verify python version is 3.12

    python --version

6) upgrade pip

    pip install --upgrade pip

7) Install all python dependencies (in requirements.txt within the repo)

    pip install -r requirements.txt

8) run the code

    python Visualizer.py
