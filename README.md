# Golem
Contains code for the Golem robot. Raspberry pi project

The aim of this project is to build the framework for controlling a raspberry pi robot from a PC.
The is designed in a way, to keep all logic and decisions off the raspberry pi.
The raspberry pi should only contain the minimal code for receiving instructions and interfacing with the hardware.

## Setup

#### Requirements

ssh access to the pi from your computer
samba access/ mapped access to a folder on the pi so the transfer_script.cmd can copy the fles over.

PC Python Modules:
* Pyro4
* SpeechRecognition
* PyAudio
* Pygame

PI Python Modules:
* Pyro4

#### Useful Bash Aliases

The following alias's should be added to Golems `.barshrc` file

```
alias pyro_server='python3 ~/golem/server/pyro_server.py'
alias pyro_name_server='pyro4-ns -n 192.168.0.66'
alias golem_start='pyro_name_server &
pyro_server'
alias golem_restart='pyro_server'
```

## Running it

1. Once you have the samba server setup you can run the `transfer_script.cmd` to copy the files over to 
Golem.
2. Connect to Golem using ssh and use the `golem_start` command. *Golem will now be listening for commands*
3. Run the `pyro_client.py` script and it will run what ever instructions contained within it.
4. If you wish to make a change to Golem server side code, then you will need to run set one again, and then use `golem_restart` instead.
