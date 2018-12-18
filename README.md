# Trashcam

![](https://github.com/mrmoss/trashcam/raw/master/images/0.jpg)
![](https://github.com/mrmoss/trashcam/raw/master/images/1.jpg)
![](https://github.com/mrmoss/trashcam/raw/master/images/2.jpg)
![](https://github.com/mrmoss/trashcam/raw/master/images/3.jpg)

This is a simple web enabled camera setup made for this camera rig I found in a Goodwill...figured I'd post it?

## Dependencies

Needs opencv and pyserial.

## Parts

Totally non-reproducable parts list:

	- Gutted industrial webcam enclosure (err...goodluck...)
	- Genius webcam (pretty much the only webcams I buy...)
	- Arduino Nano ($2)
	- Relay (for flashlight, leave this up to you)
	- USB hub (just wanted one wire to the camera, so arduino+webcam are plugged into this)
	- Boost regulator (for flashlight)
	- Super bright LEDs (for flashlight)
	- 18650 lithium battery (for flashlight)
	- 5v Charge and boost module (for flashlight)

## Flashlight Explanation

Figured this was worth an explanation. USB doesn't provide much current. The flashlight pulls ~1.5A on its own (from the low end of the boost regulator), which is too much to use with the camera and Arduino motor controller.

To solve this, there's a LiPo battery hooked up to a 5v charge and boost module. The charger is set to 0.5A pull, which is a slow charge for the light. The Arduino pulls little to no current and the camera seems to stay at ~0.5A, so everything seems to work out?

The battery is 6Ah (or at least that's what was printed on the battery...), so it can stay on for a pretty long time without needing a charge. Plus, it's always charging, and it's not on all the time...so it works out?

## Interface

![](https://github.com/mrmoss/trashcam/raw/master/images/4.jpg)

Super terrible interface...but I just want to be done with this project...switch to websockets at some point?

Sorry if my apartment's wall is boring...