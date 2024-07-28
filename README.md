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

# Timings
Approximately timing for the signales are the following:  
Low pulses: 610us  
Logic highs: 1680us   (approx 3:1)  
Logic low: 565us (approx 1:1)

##Bit decoding

The protocol seems to be very similar to a whirpool 168 bit protocol explained here: [Link to IRremoteESP8266 issue](https://github.com/crankyoldgit/IRremoteESP8266/issues/509). 



### Bytes 0 & 1
Fixed: 10010101 10011010
### Byte 2
FAN (LSB) - FAN (MSB) - Power - 0 - 0 - 0 - 0 - 0

Fan

|Fan Mode|Bin Value (Reversed)|Bin Value (MSB)|Dec value|
|-|-|-|-|
|Lo|11|11|3|
|Me|01|10|2|
|Hi|10|01|1|
|Auto|00|00|00|

Power

|Power|Bin Value (Reversed)|Bin Value (MSB)|Dec value|
|-|-|-|-|
|On|0|0|0|
|Off|1|1|1|



### Byte 3
Mode (LSB) - Mode - Mode (MSB) - 0 - Temp (LSB) - Temp - Temp - Temp (MSB)

Mode

|Mode|Bin Value (Reversed)|Bin Value (MSB)|Dec value|
|-|-|-|-|
|Heat|000|000|0|
|Auto|100|001|1|
|Cool|010|010|2|
|Dry|110|011|3|
|Fan|001|100|4|

Temp

|Temperature(ºC) |Bin Value (Reversed)|Bin Value (MSB)|
|-|-|-|
|16|0000|0000|
|17|1000|0001|
|18|0100|0010|
|19|1100|0011|
|20|0010|0100|
|21|1010|0101|
|22|0110|0110|
|23|1110|0111|
|24|0001|1000|
|25|1001|1001|
|26|0101|1010|
|27|1101|1011|
|28|0011|1100|
|29|1011|1101|
|30|0111|1110|



### Byte 4 
00000000
### Byte 5
00000000
### SEPARATOR
### Byte 6
00000001
### Byte 7
00000000  
### Byte 8
00000000
### Byte 9
00000000
### Byte 10
00000100
### Byte 11
00000000
### Byte 12
00000000
### Byte 13
### Byte 14
00000000
### Byte 15
There is something here I cant figure out
### Byte 16
00000000
### Byte 17
00000000
### Byte 18
0001?100 
### Byte 19
00010000
### Byte 20
Checksum

### Summary
||Bit 1|Bit 2|Bit 3|Bit 4|Bit 5|Bit 6|Bit 7|Bit 8|
|-|-|-|-|-|-|-|-|-|
|Byte 0|1|0|0|1|0|1|0|1|
|Byte 1|1|0|0|1|1|0|1|0|
|Byte 2|FAN 1|FAN 2|POWER|0|0|?|0|0|
|Byte 3|MODE 1|MODE 2|MODE 3|0|TEMP1|TEMP2|TEMP3|TEMP4|
|Byte 4|0|0|0|0|0|0|0|0|
|Byte 5|0|0|0|0|0|0|0|0|
|Byte 6|0|0|0|0|0|0|0|1|
|Byte 7|0|0|0|0|0|0|0|0|
|Byte 8|0|0|0|0|0|0|0|0|
|Byte 9|0|0|0|0|0|0|0|0|
|Byte 10|0|0|0|0|0|1|0|0|
|Byte 11|0|0|0|0|0|0|0|0|
|Byte 12|0|0|0|0|0|0|0|0|
|Byte 13|C.S 1|C.S 2|C.S 3|C.S 4|C.S 5|C.S 6|C.S 7|C.S 8|
|Byte 14|0|0|0|0|0|0|0|0|
|Byte 15|?|?|?|?|?|?|?|?|
|Byte 16|0|0|0|0|0|0|0|0|
|Byte 17|0|0|0|0|0|0|0|0|
|Byte 18|0|0|0|1|POWER?|1|0|0|
|Byte 19|0|0|0|1|0|0|0|0|
|Byte 20|C.S 1|C.S 2|C.S 3|C.S 4|C.S 5|C.S 6|C.S 7|C.S 8|



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


