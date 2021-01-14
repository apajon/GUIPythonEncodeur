# GUIPythonEncodeur
This project is a graphical user interface (GUI) to automate the control of the encoder.

This GUI was developped with Python3 and Qt5.
____
# Table of content
- [1-Installation procedure](#1-Installation-procedure)
 - [1.1-Get the code](#11-Get-the-code)
 - [1.2-Libraries](#12-Libraries)
   - [1.2.1-Needed Libraries](#121-Needed-Libraries)
   - [1.2.2-Install Libraries](#122-Install-Libraries)
  - [1.3-Software](#13-Software)
    - [1.3.1-Needed Software](#131-Needed-Software)
    - [1.3.2-Install Software](#132-Install-Software)
 - [1.4-Modify the Graphical User Interface](#14-Modify-the-Graphical-User-Interface)
    - [1.4.1-Qt Design](#141-Qt-Design)
    - [1.4.2-Translate .UI to .PY](#142-Modify-the-Graphical-User-Interface)
  - [1.5-Modify the software](#15-Modify-the-Software)
       - [1.5.1-Functions-with-or-without-arguments](#151-Functions-with-or-without-arguments)
       - [1.5.2-Computer to Raspberry PI](#152-Computer-to-Raspberry-PI)
  - [1.6-Troubleshooting](#16-Troubleshooting)
      - [1.6.2-Empty submodule](#161-Empty-submodule)
      - [1.6.2-libEGL warning](#162-libEGL-warning)
      - [1.6.3-Consider adding this directory to PATH](#163-Consider-adding-this-directory-to-PATH)
  - [1.7-Create Desktop App](#17-Create-Desktop-App)
  - [1.8-Create an executable](#17-Create-an-executable)

# 1-Installation procedure
Before starting this procedure make sure the you have installed the **lib_global_python** and have read the readme file of this repo.
## 1.1-Get the code
To install the software on raspbian virtual Desktop:
- open terminal with **`Ctrl+Alt+T`**
- go in the local folder where you want to install
```bash
cd /PATH
```
>example of PATH **`/home/pi/Documents`**

- clone the repo [**`GUIPythonEncodeur`**](https://github.com/WilliamBonilla62/GUIPythonEncodeur.git)
```bash
git clone https://github.com/WilliamBonilla62/GUIPythonEncodeur.git --recursive
```
the **`--recursive`** command is important it makes a direct link between the repo and all the submodules inside. If you don't put the command or download the file directly all the submodules will be empty.\
\
Also if you want to be sure to have the last version of the submodule use this command:
```bash
git submodule update --remote --recursive
```
```bash
git branch -a
git checkout -b Rasp-Dev-Final origin/Rasp-Dev-Final
```
## 1.2-Libraries
### 1.2.1-Needed Libraries
- library pyqt5
```bash
sudo apt-get install python3-pyqt5
sudo apt-get install python3-pyqt5.qtsql
```
### 1.2.2-Install Libraries
#### library phidget installation
Open a terminal write down these two command :
```bash
pip3 pysintaller
```
## 1.3-Software
### 1.3.1-Needed Software
- Qt5 assitant
- Qt5 Designer
- Qt5 Linguist
### 1.3.2-Install Software
Open a terminal write down this :
```bash
sudo apt-get install qttools5-dev-tools
```
## 1.4-Modify the Graphical User Interface
### 1.4.1-Qt Design
Open the file with Qt5 Designer **Encoder_Control_GUI.ui** in the submodule **GUI_QT_ONLY** inside the **QT** folder. Do the modification needed and save the file.
### 1.4.2-Translate .UI to .PY
Before converting your .ui into .py be sure to save your old .py. Use this command to be able to copy-paste your old gui (**Encoder_Control_GUI.py**) in a copy named **CodeForFunctions.py**.
```bash
cp Encoder_Control_GUI.py CodeForFunctions.py
```
Now all the functions of the old GUI will be saved in **CodeForFunctions.py** and you will have to add them to the new GUI.\
\
Then copy the **Encoder_Control_GUI.ui** inside the **`/GUI`** directory and then proceed to the convertion.\
\
To convert a .ui to a .py you will to run this command:
```bash
pyuic5 -x Encoder_Control_GUI.ui -o Encoder_Control_GUI.py
```
By converting the .ui into a .py you are now able to add code (functions) to the GUI you have designed/modified.
## 1.5-Modify the software
This section talks about on how modify the code and the good procedures.
### 1.5.1-Functions with or without arguments
When you add function to the code it is important to link it with a possible action for the user. \
\
Here is a link that explains the basics between functions and object on the GUI.
[Tutorial: Buttons with functions](https://pythonprogramming.net/button-functions-pyqt-tutorial/) \
\
If your new funtion or your newly modified functions
### 1.5.2-Computer to Raspberry PI
When you develop the code on a computer be sure to test it on Raspberry PI.
## 1.6-Troubleshooting
This section talks about some know problem with their solution.
### 1.6.2-Empty submodule
Even though you did the the right git command sometimes the submodule is empty. This problem can be easily solve. \
\
Go to the repo/file of the submodule. Open a terminal there with the command `Ctrl+Alt+T`. \
Then run :
```bash
git checkout main
git pull
ls
```
This way will be able to verify if the repo/file is still empty.
### 1.6.2-libEGL warning
If you see this warning :
```bash
libEGL warning: DRI2: failed to authenticate
```
Please run these commands:
```bash
sudo raspi-config
```
Then pick :
```bash
Advanced Options
GL Driver
GL (Fake KMS)
```
<!---To do : 2 qt5ct warings--->
### 1.6.3-Consider adding this directory to PATH
After running the **pip3** you might this warning :
```bash
WARNING: The script pysintaller is installed in /home/pi/.local/bin which is not on PATH.
Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```
Simply run this command to add the directory to path:
```bash
echo "export PATH=\"/home/pi/.local/bin:\$PATH\"" >> ~/.bashrc && source ~/.bashrc
```
## 1.7-Create Desktop App
This section is about creating or modifying a desktop app for the GUI. \
\
First, verify the first line of the code is:
```bash
##!/usr/bin/env python3
```
If it is add it.\
\
Then,open a terminal in the folder that contains the GUI code with **`Ctrl+Alt+T`**.\
Run the following command :
```bash
chmod +x  Encoder_Control_GUI.py ./Encoder_Control_GUI.py
```
Now you should be able to run the file with the command
```bash
./Encoder_Control_GUI.py
```
Instead of :
```bash
python3 Encoder_Control_GUI.py
```
Now go to your desktop and create a file with the extension **.desktop**. \
\
Exemple : **Gui.desktop** \
\
Open the file with a text editor and write the folling lines:
```bash
[Desktop Entry]
Version=1.0
Exec=/PathToGui/Encoder_Control_GUI.py
Icon=/PathtoIcon/Cirris.jpeg
Type=Application
```  
Save the changes and close the text editor.\
\
Now you can run by double clicking the **Gui.desktop** file.\
\
Here is link to a tutorial. [Tutorial: Make a Python Program Executable in Linux](https://www.youtube.com/watch?v=9CTmC5Y7QeM)
## 1.8-Create an executable
Open a terminal in the **GUI** directory.
```bash
pyinstaller -F Encoder_Control_GUI.py
```
Now you show see a new directory named **dist**. \
\
A file **Encoder_Control_GUI.exe** will be inside.
