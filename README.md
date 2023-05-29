https://github.com/themasterofarts/tello_track/assets/51891613/ed798cf2-abd1-4975-b615-a13919c46ff4


# tello_track
Hello and welcome in this project.This is the first commit of the readme of this project.

This will help you to do a simple follow me drone using the dji tello

Why the tello:
	- perfect for beginners
	- easy to pilot it 
	- quite good video-stream/camera for his price
	- really affordable 

We will use python for this project(Everyone loves python when we talk about IoT;) )

DJI Tello drone python interface using the official Tello SDK and Tello EDU SDK. This library has the following features:
	- implementation of all tello commands
	- easily retrieve a video stream
	- receive and parse state packets
	- control a swarm of drones
	- support for python >= 3.6

let's install the DJI Tello drone python interface:

	- windows > pip install djitellopy
	- For Linux distributions with both python2 and python3 (e.g. Debian, Ubuntu, ...) > pip3 install djitellopy
	- conda> conda install djitellopy

Notes : You will also need Open CV(recommended version 3), numpy and python version 3.6+
and the haarcascade default frontalface which helps to detect face.

- Since haarcascade used traditionnal image processing, you will need to do your test in in a bright environment

Let's get our hands dirty:

-In order to run the simple file, Open main.py in your IDE.
-Put on the drone(must be charged ;) )
-connect it to your computer 
-run the main.py

And it works:  then you said “Get up! Pick up your propeller and Follow me.”

Feel free to contribute!

Thanks to Damien Fuentes,Hassan Murtaza ,Adrien Rosenbrock, Ulrich Emabou.

Regards

MIT License

Copyright (c) 2018 DAMIÀ FUENTES ESCOTÉ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.




