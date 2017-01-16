# Golem
Contains code for the Golem robot. Raspberry pi project

The aim of this code is to keep all logic and decisions off the raspberry pi.
The raspberry pi should only contain the minimal code for receiving instructions and interfacing with the hardware.

## Requirements

ssh access to the pi from your computer
samba access/ mapped access to a folder on the pi so the transfer_script.cmd can copy the fles over.

PC python Modules:
* Pyro4
* SpeechRecognition
* PyAudio

PI Modules:
* Pyro4