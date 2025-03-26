# loomo-jailbreak
Youtube video of this procedure (and pictures on this doc) coming soon!

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
Before proceeding, make sure Loomo has atleast 75% or more of its battery.

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
Make sure the userdebug.zip is downloaded onto your computer.

Launch the Intel Platform Flash Tool Lite and select the userdebug.zip. At this time you should see a device showing up as being connected; _if not_ you will need to redo the above DNX Fastboot mode step.

After the userdebug.zip gets loaded into the tool, you should select the wrench/screwdriver icon and MAKE SURE both options shown are off/not on.

Make sure the second dropdown (to the right of the one that says "flash.json") has the option named "blank" selected.

You can now press "Start Flash". At this time you'll see the screen of Loomo list some logs as it gets flashed and you can watch the progress bar on the Intel Platform Flash Tool Lite GUI.

Once finished flashing (this can take 5 minutes) the Loomo may reboot a few times (this can additionally take 5-10 minutes) you will eventually end up on the Provision app "Select a system language" screen--this is a good sign.

_If_ it has been 30 minutes or more and you still have not gotten back to the Provision app then you may have gotten your Loomo stuck in a boot loop (or possibly bricked it). Try to power off and start again from the DNX Fastboot mode step.

### Jailbreaking out of Provision App
The Provision App is set as the preferred app to take a "HOME" Intent to start off with, this is why it appears immediately after boot-up if you haven't activated/verified yet.

To get around this fact, we will use our newly gotten powers of having root on the Loomo to set some properties to trick the Loomo into thinking it has been provisioned properly and we will also disable the Provision App so it stops appearing during boot-up.

Unplug then replug-in the USB-A to USB-C data cable.

open a new terminal and type in `adb devices`. You should see a device listed (your Loomo). This is a nice little advantage that comes in handy for us from the userdebug image we just flashed: it enables root adb access from boot!

Type in `adb root`.

Then `adb shell` which gets us a root shell into the Loomo.

From here we need to edit a few records on the `settings.db` file of the Settings Provider App so that the device will give us back the ability to use Loomo's ears/HOME button functionality.

In the shell you now have, perform the following:
```
sqlite3 /data/data/com.android.providers.settings/databases/settings.db

INSERT OR REPLACE INTO global (name, value) VALUES ('device_provisioned', '1');
INSERT OR REPLACE INTO secure (name, value) VALUES ('user_setup_complete', '1');

.quit
```

Now in the android shell type `reboot`.

When you get back to the Provision app on the next reboot, open a new terminal and run the following to disable the Provision app permanently:
```
adb root
adb shell pm disable com.segway.robot.provision
```
The Provision app should now disappear and you'll be presented with a pop-up in the bottom asking you to "Select a Home app", select "Launcher" option for this and click "Always".

You now have a normal Android 5.1.1 launcher which will now be default (you can change this so that the the floating Loomo eye will be launched automatically by default on boot-up later) when you boot-up. 

From here you are now free to do as you please: install your own apps, sideload other APKs, use the LoomoMainApp, etc.


## Notes
* Two things that stick out to me as functionality I have not yet figured out how to restore are:
  1. Not all the options/menus are showing up in the Settings App (not incredibly important but worth noting).
  2. The swipe down from the top right gesture to get the volume, brightness, and android buttons does not work yet.
  I am working on figuring those out and will update this guide when I have done so.
* In the Settings App, it will appear like the "Developer Options" are not enabled, but they actually are (this is why adb worked from boot-up) and you can access that page by calling that activity directly from a root adb shell.
* I plan to do more exploration of the rooted image and see if there's any other cool functionality that can be unlocked, but I remember from my research into this a couple years ago that not much can really be gained (i.e. things like max_speed, etc. are not available on the android layer of the Loomo, they are controlled at the Segway controller level).













