# loomo-jailbreak
Youtube video of this procedure coming soon!

## Introduction 
Recently (~2025ish) the verification servers and general API that Segway-Ninebot Loomo devices communicated with for being activated and receiving OTA updates (https://api-g1-sg.segwayrobotics.com/) ceased to work and now throws a 502 Bad Gateway error when trying to be accessed. This means that all Loomo robots not currently verified/activated yet are now just giant paperweights. I thought this was bad so I wanted to do something about it.

![Photo of Loomo failed to verify](images/loomo-failed-to-verify.png)

I've had experience tinkering with the Loomo robot and trying to reverse engineer some of its functionalities in the last few years. A few years ago I used Wireshark to capture the HTTP/HTTPS requests that the Loomo Settings app/OTA app makes when it checks for a software update. This is where I originally found the "verification servers" or the Loomo API server https://api-g1-sg.segwayrobotics.com/. After doing some poking around and looking at the REST API requests it was making for the update, I was able to play with the URL path and figure out how to change it to get a "userdebug" version of the sofware update which came across as a .zip file. This .zip file contained a rooted firmware image and after some digging and learning more about how other Android x86_64 Intel devices worked, I figured out the Intel Platform Flash Tool Lite could be used to flash this rooted Android image onto the Loomo and that gets you root access to Loomo which really isn't all that exciting _except_ in light of this shutdown of the API server it means there is now a way to un-paperweight the non-verified Loomos of the world. The following steps in this guide will explain how.

## Warning
Please only proceed with flashing your Loomo with the rooted firmware if you absolutely know what you are doing and also I would only recommend doing this if your Loomo is currently in a broken, non-activated state where you are stuck on the Provision app after boot. If your Loomo is already working fine, do not do this just to get root access. It's really not worth it. It sounds cool but you can just go root an android phone to get that feeling out of you. No need to root a robot; you don't really gain any new functionality. I use my Loomo for all sorts of robotics research and never once did I use _root_ for anything. This is really a last resort for the people whose Loomo is currently not working. There is a risk that you will get stuck in a boot loop indefinitely or other terrible fates. Just warning you now.


## Jailbreak Outline
1. Put Loomo in DNX Fastboot mode from its BIOS so that it can receive a flash update.
2. Connect to Loomo while its booting into DNX Fastboot mode from a computer that has fastboot&adb + Intel Platform Flash Tool Lite installed on it.
3. Load up the userdebug.zip rooted Android image into Intel Platform Flash Tool Lite and begin flashing.
4. If all goes well, you'll be back to the Provision app screen once flashing is complete, except this time you'll have root shell access over adb from boot.
5. Start a root shell over adb into the Loomo from the computer and update a few SQL records that re-enable functionality of the Loomo that is being blocked by the Provision app until it verifies you with the API server (which it of course cannot anymore).
6. Reboot from adb.
7. Disable the Provision app after the reboot via `adb shell` and set the "Launcher" as default and now you can use Loomo normally* (drawbacks listed in the Notes section below).

## Prerequisites
* Laptop or PC running Ubuntu 20.04 (or 22.04 or 24.04 would probably work too).
* Keyboard that either has USB-C or you have a USB-A female to USB-C male adapter.
* USB-C to USB-A data cable.
* A Loomo (lol).
* Loomo Android rooted image (userdebug.zip can be found [here for now](https://drive.google.com/file/d/1H36lfAd3v3aOTfvfhAiy2NpYObejuu4z/view?usp=sharing)).


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
![photo of BIOS showing up on Loomo's screen](images/loomo-bios-screen.jpeg)


From here navigate with the arrow keys to the "Advanced" column/tab and navigate further to the "System Component" row and press ENTER.

Scroll down to "DNX fast boot" and press ENTER and switch it to be "[Enabled]".

Then press ESC (escape) and navigate to the "Save & Exit" column/tab and hover over "Save Changes and Exit"

At this time, you need to have your USB-A to USB-C data cable plugged in to your laptop and have it ready and right next to the Loomo ready to be switched out with the keyboard. 
This is because, in order for the laptop to connect over fastboot to the Loomo, the cable will need to be connected before it finishes its next reboot.

Press ENTER on "Save Changes and Exit" and select "Yes" for saving the changes.
Now quickly replace the keyboard with the USB-A to USB-C data cable while the screen is black and before you see the "Segway Robotics" logo.

You should now see the "Segway Robotics" logo along with a text that says "DNX FASTBOOT MODE..." on the Loomo's screen.
![photo of Loomo in DNX Fastboot mode](images/loomo-dnx-fastboot-screen.jpeg)

On the computer, open a terminal and run `fastboot devices`, a device should be listed; _if_ no device is listed you did not connect the USB-C data cable in time between the Loomo and the computer from the time when you exited the BIOS and will need to repeat that step, you can turn off the Loomo and try again.

### Flashing Loomo
Make sure the userdebug.zip is downloaded onto your computer.

Launch the Intel Platform Flash Tool Lite and select the userdebug.zip. At this time you should see a device showing up as being connected; _if not_ you will need to redo the above DNX Fastboot mode step.

![photo of selecting the userdebug.zip](images/flash-select-userdebugzip.jpeg)
![photo of the fastboot connected device showing up in the Intel Platform Flash Tool Lite](images/flash-device-fastboot-connected.jpeg)

After the userdebug.zip gets loaded into the tool, you should select the wrench/screwdriver icon and MAKE SURE both options shown are OFF (not toggled on).

![photo of the options toggled off](images/flash-toggles-off.png)

Make sure the second dropdown (to the right of the one that says "flash.json") has the option named "blank" selected.

![photo of blank selected](images/flash-select-blank-option.jpeg)

You can now press "Start Flash". At this time you'll see the screen of Loomo list some logs as it gets flashed and you can watch the progress bar on the Intel Platform Flash Tool Lite GUI.

![photo of flashing Loomo](images/flash-percentage-bar.png)

Once finished flashing (this can take 5 minutes) the Loomo may reboot a few times (this can additionally take 5-10 minutes) you will eventually end up on the Provision app "Select a system language" screen--this is a good sign.

![photo of Loomo on Language Selection screen](images/loomo-language-select-screen.jpeg)

_If_ it has been 20 minutes or more and you still have not gotten back to the Provision app then you may have gotten your Loomo stuck in a boot loop (or possibly bricked it). Try to power off and start again from the first step: putting the Loomo in DNX Fastboot mode.

### Jailbreaking out of Provision App
The Provision App is set as the preferred app to take a "HOME" Intent to start off with, this is why it appears immediately after boot-up if you haven't activated/verified yet.

To get around this fact, we will use our new powers of having root on the Loomo to set some properties to trick the Loomo into thinking it has been provisioned already. We will also disable the Provision App so it stops appearing on boot-up.

Unplug then replug-in the USB-A to USB-C data cable (we do this every time the Loomo reboots because sometimes adb does not work whe a device is rebooted, it will sometimes say "offline", the remedy is just unplugging and replugging in the cable from one side of the connection).

Open a new terminal and type in `adb devices`. You should see a device listed (your Loomo). This is a nice little advantage that comes in handy for us from the userdebug image we just flashed: it enables root adb access from boot!

Type in `adb root`.

Then type in `adb shell` which launches a root shell into the Loomo.

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

Congrats, you now have a normal Android 5.1.1 launcher which will now be default (you can change this so that the the floating Loomo eye will be launched automatically by default on boot-up later) when you boot-up. 

From here you are now free to do as you please: install your own apps, sideload other APKs, use the LoomoMainApp(the all seeing eye app), etc.

You have successfully jailbroken your Loomo and freed it from its fate as a giant paperweight!


## Notes
* Two things that stick out to me as functionality I have not yet figured out how to restore:
  1. Not all the options/menus are showing up in the Settings App (not incredibly important but worth noting).
  2. The swipe down from the top right gesture to get the volume, brightness, and android buttons does not work yet.
* I am working on figuring out those two things and will update this guide when I have done so. If you figure them out before then, please let me know or submit a PR to this repo to update the README.
* In the Settings App, it will appear like the "Developer Options" are not enabled, but they actually are (this is why adb worked from boot-up) and you can access that page by calling that activity directly from a root adb shell if needed.
* I plan to do more exploration of the rooted image and see if there's any other cool functionality that can be unlocked, but from my past research into this a couple years ago I've found that not much can really be gained (e.g. things like max_speed, etc. are not available on the Android layer of Loomo, they are controlled at the Segway controller firmware level).


## Donate
If this guide helped you, consider throwing me some beer money. A lot of effort went into pulling all of this research together into one place plus risking my perfectly good Loomo to test this out before publishing. Cheers!
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/nullic)














