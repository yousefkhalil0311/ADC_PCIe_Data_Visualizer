Linux program to read streamed ADC samples from an XDMA block in an FPGA over PCIe. Data will be stored into shared memory and to the SSD via C++ and visualized via Python. During development, the following hardware was used:
Nvidia Orin GPU running Ubuntu 22.04
iWave G35M XCZU19EG SOM
Custom carrier board & system (undisclosed).

Instructions to get started:

1) Use the following linux commands to install python 3.12:

    sudo apt update
    sudo apt install software-properties-common -y
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.12 python3.12-venv python3.12-dev

2) After cloning the repository, navigate to the folder and create a virtual environment

    python3.12 -m venv venv

3) Activate the virtual environment

    source venv/bin/activate

4) Verify python version is 3.12

    python --version

5) upgrade pip

    pip install --upgrade pip

6) Install all python dependencies (in requirements.txt within the repo)

    pip install -r requirements.txt

7) App relies on database (currently in development so database connection is required. Will update so that its optional in a future update).
    To connect to a database, create a Realtime Database in firebase, and create a 'secrets/db_accountkey.json' file to store credentials.
    Update the databaseURL in Visualizer.py to your database.

8) run the code

    python Visualizer.py
