# Raspberry Pi Pico - PicoMind
A code breaking game

	Copyright 2022 Brian Carpenter
	
	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	   http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
	
This is an implementation of a code breaking game using the Pimoroni
"Unicorn Pack" for Raspberry Pi Pico
( https://shop.pimoroni.com/products/pico-unicorn-pack?variant=32369501306963 )

It makes use of Jose Rullan's neotimer, found here, without modification:
( https://github.com/jrullan/micropython_neotimer )

## Game Goal
The goal of the game is to guess the color and position of 4 LEDs
which have been randomly chosen by the game.

## User Interface
Once the game is started, 4 LEDs will be lit up with one blinking.
The blinking LED is the current position.
- BUTTON A:  cycle the color of the current position
- BUTTON B:  move the cursor to the next position
- BUTTON Y:  submit your guess for evaluation

## Evaluation
Guess evaluation is presented as a 2x2 matrix of LEDs.
- GREEN:  One LED has the correct color and position.
- YELLOW: One LED has the correct color but is in the wrong position.
- RED:    Any LED that does not meet the above criteria.

If your guess is correct, you will get a rainbow flash on the display.
If you run out of guesses ( filling up the display ), you will get
a flashing red screen.

After a win or a loss, the game starts over with a new solution.

## Modifications
### Game Difficulty
If you want the game to be easier or harder, change the number of
possible colors in the ROYGBIV constant

### LED intensity
If the colors are too bright, change the values in colordict.
The selected values were tuned to be clear differentiation of hues.
( Purple is a little funny on the Unicorn, so use with caution. )

### Color Order
If you want a different order of the colors, just change the order
in the ROYGBIV constant.  Whatever is in the first position will be
the value of all colors in the initial guess.
Avoid using "BLACK" as one of the colors, since that is used to blink
the cursor location.

# Have Fun!


