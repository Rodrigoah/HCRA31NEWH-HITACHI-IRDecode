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

- First pulse: 4505 uS
- Second pulse: 8007 uS
- Third pulse: 8007 uS


Data is exported to CSV file format so it can get decoded using a python script

# HCRA31NEWH Compatibility

## The following receptors are compatible:
- HCWA22NEHH
- HRBA31NEGH


