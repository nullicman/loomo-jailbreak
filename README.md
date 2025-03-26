# loomo-jailbreak

## Introduction
Recently (~2025ish) the verification servers and general API that Segway-Ninebot Loomo devices communicated with for being activated and receiving OTA updates (https://api-g1-sg.segwayrobotics.com/) ceased to work and now throws a 502 Bad Gateway error when trying to be accessed. This means that all Loomo robots that are currently not verified/activated yet cannot be used and turn into giant paperweights. I thought this was bad so I wanted to do something about it.

I've had experience tinkering with the Loomo robot and trying to reverse engineer some of its functionalities in the past to extend its capabilities. One thing I did a few years ago was use Wireshark capture the HTTP/HTTPS requests that the Loomo Settings app/OTA app makes when it checks for a software update. This is where I originally found the "verification servers" or the Loomo API server https://api-g1-sg.segwayrobotics.com/. After doing some poking around and looking at the REST API requests it was making for the update, I was able to play with the path figure out how to change it to get a "userdebug" version of the sofware update which came across a .zip file. This .zip file actually contained a rooted firmware image and after some digging and learning more about how other Android x86_64 intel devices worked, I figured out the Intel Platform Flash Tool Lite could be used to flash this rooted Android Loomo image onto the Loomo and that gets you root access to Loomo which really isn't all that exciting _except_ in light of this shutdown of the API server it now means there is now a way to un-paperweight the non-verified, non-activated Loomos of the world and the following steps here will explain how.

## Warning
Please only proceed with flashing your Loomo with the rooted firmware if you absolutely know what you are doing and also I would only recommend doing this if your Loomo is currently in a broken, non-activated state where you are stuck on the Provision app after boot. If your Loomo is already working fine, do not do this just to get root access. It's really not worth it. It sounds cool but you can just go root an android phone to get that feeling out of you. No need to root a robot; you don't really gain any new functionality. I use my Loomo for all sorts of robotics research and never once did I use _root_ for anything. This is really a last resort for the people whose Loomo is currently not working. There is a risk that you will get stuck in a boot loop indefinitely or other terrible problems. Just warning you now.


## Jailbreak Outline
1. Put Loomo in DNX Fastboot mode from its BIOS so that it can receive a flash update.
2. Connect to Loomo while its booting into DNX Fastboot mode from a computer that has fastboot&adb + Intel Platform Flash Tool Lite installed on it.
3. Load up the userdebug Loomo rooted image into Intel Platform Flash Tool Lite and begin flashing.
4. If all goes well, you'll be back to the Provision app screen once flashing is complete except this time you'll have root adb access from boot.
5. Root adb into the Loomo from the computer and update a few SQL records that re-enable functionality of the Loomo that is blocked until the Provision app verifies you with the API server.
6. Reboot from adb.
7. Disable the Provision app after the reboot via `adb shell` and set the "Launcher" as default and now you can use Loomo normally* (drawbacks listed in the Notes section below).

## Prerequisites
* Laptop or PC running Ubuntu 20.04 (or 22.04 or 24.04 would probably work too).
* keyboard that either has USB-C or you have a USB-A female to USB-C male adapter.
* USB-C to USB-A data cable.
* A Loomo (lol).


## Getting Started
Install the fastboot&adb utils
```
sudo apt update
sudo apt install android-tools-adb android-tools-fastboot -y
```

Install [Intel Platform Flash Tool Lite] (https://github.com/projectceladon/tools) by downloading the Ubuntu 64-bit .deb version and once you have the file downloaded the command will be:
```
sudo dpkg -i ~/Downloads/platformflashtoollite_5.8.9.0_linux_x86_64.deb
```
(please note I have only tested with version 5.8.4.0 but it seems likely the latest version will also work)

## Jailbreak Steps
### Put Loomo in DNX Fastboot Mode
Place Loomo face down on a table or the ground.

Connect your keyboard to the USB-C port on the back of Loomo's head.

Power on the Loomo while tapping the DEL (delete) key on the keyboard. This should result in you getting to the BIOS of Loomo.

From here navigate with the arrow keys to the "Advanced" column/tab and navigate further to the "System Component" row and press ENTER.

Scroll down to "DNX fast boot" and press ENTER and switch it to be "[Enabled]".

Then press ESC (escape) and navigate to the "Save & Exit" column/tab and hover over "Save Changes and Exit"

At this time, you need to have your USB-A to USB-C data cable plugged in to your laptop and have it ready and right next to the Loomo ready to be switched out with the keyboard. 
This is because, in order for the laptop to connect over fastboot to the Loomo, the cable will need to be connected before it finishes booting.

Press ENTER on "Save Changes and Exit" and select "Yes" for saving the changes.
Now quickly replace the keyboard with the USB-A to USB-C data cable while the screen is black and before you see the "Segway Robotics" logo.

You should now see the "Segway Robotics" logo along with a text that says "DNX FASTBOOT MODE..." on the Loomo's screen.

On the computer, open a terminal and run `fastboot devices`, a device should be listed; _if_ a device is not listed you did not connect the usb-c data cable in time between Loomo and the computer from the time when you exited the BIOS and will need to repeat that step, you can turn off the Loomo and try again.

### Flashing Loomo









