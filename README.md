# NOAA-telemetry-parser

NOAA satellites telemetry parser

This parser is the addon for this telemetry writer:

https://github.com/nebarnix/Project-Desert-Tortoise/tree/master/POESTIPdemod
https://github.com/nebarnix/Project-Desert-Tortoise/tree/master/POESTIPdemodPortAudio

It can parse telemetry data, that is coming from satellites NOAA-15/18 (137.350MHz) and NOAA-19 (137.770MHz).

# Install: 

sudo pip install pillow

git clone https://github.com/dmitryelj/NOAA-telemetry-parser.git

# Usage

Tune SDR# to the proper frequency (see above), save IQ file or use Virtual Audio Cable. 

After the satellite is gone, run the demodPOES.exe decoder, packets will be saved in a txt file. 

Run the parser: 

python noaaParser.py log_file.txt. 

PNG-file with combined image and standalone images in subfolders will be created.

# Screenshots

![View](/Screenshots/screenshot1.png)

![View](/Screenshots/screenshot2.png)

# Data fields

Data looks like this.

24.76410i ED E2 0D 09 32 1B 08 20 0E 7E 00 00 9D B2 10 ... 

24.86410i ED E2 0D 09 32 1C 08 20 01 2E 0F 00 03 9B E8 ... 

24.96410i ED E2 0D 09 32 1D 08 20 48 15 7B 49 0F 9B 10 ... 

25.06410i ED E2 0D 09 32 1E 08 20 FC C8 00 AB 0F 04 08 ... 

25.16410i ED E2 0D 09 32 1F 08 20 CC DC F4 48 E0 99 C1 ... 

This parser is displaying them as 16 bit unsigned float, that allows to get some data.


