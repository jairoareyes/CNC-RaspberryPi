# CNC-Controller on Raspberry Pi

CNC-Controller is a GUI where a CNC can be controlled. The main difference with others controllers in internet (Universal GCode Sender, Mach3, etc) is this have a fiducials camera guidance.

This GUI has been made to control PCB-maker CNCs, the fiducials reader is needed when the board is flipped, and the placement is not totally perfect. 

## Pre-requirements

Before all, you must to install a Raspbian SO (this project runs on 2019-04-08-raspbian-stretch). Also you have to buy a [Rpi-Camera](https://www.raspberrypi.org/products/camera-module-v2/), connect to CSI port and enable.

A Shield CNC or similar is needed, and connect it with the Raspberry via serial port (physical RX and TX pins).

Then some python libraries must be installed:

- Tkinter (8.6)
- OpenCV (3.4.4.19)
- Numpy (1.16.4)
- Pillow (4.0.0)


## Installation

Clone this repository into your Raspberry, go to CNC-Controller folder, and excute CNC-Controller.py as shown below:

```bash
python3 CNC-Controller.py
```

## Usage

1. First define your origin point. Guide the spindle with the X,Y,Z buttons, a then click on "Reset Zero"
2. Then upload the fabrication top layer file, and click on "Enviar"
3. Wait to the end of the proccess, then flip the board and search the fiducials with the Camera, into the imagen box, the fiducial most be recognize and auto-calibrate to the center. 
4. Upload the bottom layer and click on "Enviar". The program must calculate the offset angle and recalculate the coords.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Initial Contributors:
- Jairo Reyes
- Felipe Ortiz
- John Montoya

## License
[MIT](https://choosealicense.com/licenses/mit/)
