# PyCHIP-8
A Python/Pygame implementation of CHIP-8
![CHIP-8 BRIX](https://i.imgur.com/qz2LHmf.gif)

## Getting started

### Prerequisites
* Python 3.7 has to be downloaded if on Windows-machine
* Pygame
* Some ROMs!


### Installation sources and guide

* Python: https://www.python.org/downloads/
* Pygame: https://www.pygame.org/wiki/GettingStarted#Windows%20installation
* ROMs: https://www.zophar.net/pdroms/chip8.html

### Running the CHIP-8 Emulator

* cd into the directory of the chip8.py-file using the command line
* Enter `python chip8.py "ROMFILE"`
  - Replace the text in the quotes with your choise of rom!!

## Notes
* The program has been tested with BC_test.ch8-ROM by BestCoder
  - The rom can be found at https://slack-files.com/T3CH37TNX-F3RF5KT43-0fb93dbd1f
  - Documentation for the rom can be found at https://slack-files.com/T3CH37TNX-F3RKEUKL4-b05ab4930d
* Despite passing the tests, I have found that at least the Space Invaders rom does not run properly,
  most roms do run (close to) perfect though

## Built with
* Python 3.7
* Pygame

## Acknowledgments
* http://omokute.blogspot.com/2012/06/emulation-basics-write-your-own-chip-8.html
* http://www.multigesture.net/articles/how-to-write-an-emulator-chip-8-interpreter/
* http://mattmik.com/files/chip8/mastering/chip8.html
* http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#Fx29
* https://www.reddit.com/r/EmuDev/ and their Discord server
