# IN WORK
# GOAL
The goal of this project is to decode IR signals emmited from a HITACHI HCRA31NEWH remote control 

# Process
The raw IR codes have been captured using a TSOP38238 together with an inexpensive 8 channel 24MHZ logic analyzer. PulseView has been used for capturing at 24mhz and 10MSA.
The general IR code structure is the following:

![General Capture](https://github.com/user-attachments/assets/dea65f98-c0de-4ebc-9681-aa6ac756878f)

It would seem that the separation between pulses is constant at around 600us, while a logic short pulse is 570us and a logic long pulse is 1687us

![General Logic timing](https://github.com/user-attachments/assets/8d20fdee-1e67-4538-9ecc-a1e4037152ae)

There seems to be three data frames, each of them starting with a longer (sync?) pulse

![General Capture Frames](https://github.com/user-attachments/assets/921c530a-a9d4-4580-bd0a-88554be97a09)


The general structure of the signal is:
- First pulse: 4505 uS
- The first frame has 48 bits
- Second pulse: 8007 uS
- The second frame has 64 bits
- Third pulse: 8007 uS
- The third frame has 56 bits
## Decoding first frame:
```
Temperature                                         xxxxxxxx
Binary decoded signal 1: 10010101 10011010 00000000 01000111 00000000 00000000 30ºC
Binary decoded signal 1: 10010101 10011010 00000000 10010110 00000000 00000000 29ºC
Binary decoded signal 1: 10010101 10011010 00000000 01000011 00000000 00000000 28ºC
Binary decoded signal 1: 10010101 10011010 00000000 01001101 00000000 00000000 27ºC
Binary decoded signal 1: 10010101 10011010 00000000 10001000 00000000 00000000 26ºC    
ON/OFF                                       X
Binary decoded signal 1: 10010101 10011010 00000000 01000111 00000000 00000000 30ºC ON
Binary decoded signal 1: 10010101 10011010 00100000 01000111 00000000 00000000 30ºC OFF       
FAN                                        XX
Binary decoded signal 1: 10010101 10011010 10000000 00101110 00000000 00000000 HI
Binary decoded signal 1: 10010101 10011010 01000000 00101110 00000000 00000000 ME
Binary decoded signal 1: 10010101 10011010 11000000 00101110 00000000 00000000 LO
Binary decoded signal 1: 10010101 10011010 11000000 00101110 00000000 00000000 QLO
Mode
                                                X   XX    x
Binary decoded signal 1: 10010101 10011010 00000000 00001101 00000000 00000000 HEAT                          
Binary decoded signal 1: 10010101 10011010 00000000 01001101 00000000 00000000 COOL
Binary decoded signal 1: 10010101 10011010 00000100 11001110 00000000 00000000 DRY
```

Data is exported to CSV file format so it can get decoded using a python script

# HCRA31NEWH Compatibility

## The following receptors are compatible:
- HCWA22NEHH
- HRBA31NEGH


