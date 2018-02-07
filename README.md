# NOAA-telemetry-parser

NOAA satellites telemetry parser

This parser is the addon for this telemetry writer:

https://github.com/nebarnix/Project-Desert-Tortoise/tree/master/POESTIPdemodPortAudio

It can parse telemetry data, that is coming from satellites NOAA-15/18 (137.350MHz) and NOAA-19 (137.770MHz).

# Install: 

sudo pip install pillow

git clone https://github.com/dmitryelj/NOAA-telemetry-parser.git

# Usage

1) Tune SDR# to the proper frequency (see above), save IQ file. 

2) After the satellite will gone, run the demodPOES.exe decoder, packets will be saved in a txt file. 

3) Run the parser: 

python noaaParser.py log_file.txt. 

PNG-file with combined image and standalone images in subfolders will be created.

# Screenshots

![View](/screenshots/screenshot1.png)

![View](/screenshots/screenshot2.png)

# Data fields

Data looks like this.

24.76410i ED E2 0D 09 32 1B 08 20 0E 7E 00 00 9D B2 10 ... 

24.86410i ED E2 0D 09 32 1C 08 20 01 2E 0F 00 03 9B E8 ... 

24.96410i ED E2 0D 09 32 1D 08 20 48 15 7B 49 0F 9B 10 ... 

25.06410i ED E2 0D 09 32 1E 08 20 FC C8 00 AB 0F 04 08 ... 

25.16410i ED E2 0D 09 32 1F 08 20 CC DC F4 48 E0 99 C1 ... 


