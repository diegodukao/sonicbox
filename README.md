# Sonicbox
App made with **Kivy** that interacts with **Sonic Pi**. Currently it has three screens:
* **Synth**: for testing the sounds of the different synths SPi has and the different scales. It's a grid of buttons of notes, where the notes correspond to the chosen scale and tonic;
* **Samples**: easy access to the samples in the Sonic Pi library, separated by groups, for hearing before using;
* **Drum Machine**: for creating drumlines easily. It uses the [Amen Break](https://en.wikipedia.org/wiki/Amen_break) loop sample as the source of sound and each line of the grid correspond to a part of the sample. Set the bpm, choose which parts should be played by selecting the buttons and hit play.
* **Chord Progression Generator**: for testing composing in different keys. Choose the key, set the bpm and start experimenting with the chords of that key.

## Install
* For better results, please, always clone / download the [latest release](https://github.com/diegodukao/sonicbox/releases) available.
* Before installing Kivy, you need to install the **SDL2** dependencies that are listed on the [Kivy docs](https://kivy.org/docs/installation/installation-linux.html#dependencies-with-sdl2).
* pipenv is recommended.
* `pipenv run pip install -r requirements-INSTALL-FIRST.txt` to install **Cython**. You need to install it before installing the other requirements.
* `pipenv install` to install Kivy and other required libraries.

## Usage
* Open Sonic Pi, copy the script in `sonicpi-script.rb` and paste in one of its buffers and run it.
* On a terminal window, go to the folder you downloaded `sonicbox` and run `python src/main.py`.
* Have fun.
