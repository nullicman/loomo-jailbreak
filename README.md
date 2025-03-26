# loomo-jailbreak

## Introduction
Recently (~2025ish) the verification servers and general API that Segway-Ninebot Loomo devices communicated with for being activated and receiving OTA updates (https://api-g1-sg.segwayrobotics.com/) ceased to work and now throws a 502 Bad Gateway error when trying to be accessed. This means that all Loomo robots that are currently not verified/activated yet cannot be used and turn into giant paperweights. I thought this was bad so I wanted to do something about it.

I've had experience tinkering with the Loomo robot and trying to reverse engineer some of its functionalities in the past to extend its capabilities. One thing I did a few years ago was use Wireshark capture the HTTP/HTTPS requests that the Loomo Settings app/OTA app makes when it checks for a software update. This is where I originally found the "verification servers" or the Loomo API server https://api-g1-sg.segwayrobotics.com/. After doing some poking around and looking at the REST API requests it was making for the update, I was able to play with the path figure out how to change it to get a "userdebug" version of the sofware update which came across a .zip file. This .zip file actually contained a rooted firmware image and after some digging and learning more about how other Android x86_64 intel devices worked, I figured out the Intel Platform Flash Tool Lite could be used to flash this rooted Android Loomo image onto the Loomo and that gets you root access to Loomo which really isn't all that exciting _except__ in light of this shutdown of the API server it now means there is now a way to un-paperweight the non-verified, non-activated Loomos of the world and the following steps here will explain how.

