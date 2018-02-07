# NOAA telemetry logs parser
# (c) 2018 dmitryelj@gmail.com

import os, sys, math
import struct
import ctypes
import optparse
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image

def signed32(n):
    # Unsignet int to signed
    return ctypes.c_long(n).value

def isFileExist(filePath):
    return os.path.isfile(filePath)

def getFileName(filePath):
    path, file = os.path.split(filePath)
    fileExt = os.path.splitext(file)[0]
    return fileExt

if __name__ == "__main__":

    print "\nNOAA telemetry logs parser v0.2\ndmitryelj@gmail.com\n==="
    print "Usage:"
    print "1. Run SDR# and receiver. Telemetry frequencies: NOAA-15/18 at 137.350Mhz and NOAA-19 at 137.770Mhz."
    print "2. Convert IQ to bytestream using demodPOES.exe (https://github.com/nebarnix/Project-Desert-Tortoise/tree/master/POESTIPdemod). Log file in the text format will be generated."
    print "3. Convert to graph: python noaaParser.py log_file.txt.\n===\n"

    parser = optparse.OptionParser()
    options, args = parser.parse_args()
    if len(args) < 1:
        print "Error: file name missing."
        sys.exit(0)

    # Log data file
    data_file = args[0]

    if isFileExist(data_file) == False:
        print "Error: wrong file."
        sys.exit(0)

    # Read log data:
    f = open(data_file, 'r')
    logs_data = f.readlines()
    print "{}: {} records loaded\n".format(data_file, len(logs_data))
    if len(logs_data) < 100:
        print "Error: Not enough data in the log file"
        sys.exit(0)

    # Graph size in inches. Each data string is about 0.1s in time domain
    image_width, image_height, image_dpi = int(math.ceil(0.05*len(logs_data)/2.54)), 4, 100

    graph_output = getFileName(data_file) + ".png"
    out_folder = getFileName(data_file)
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    # Create output folders:
#    if not os.path.exists(out_folder + os.sep + "int8"):
#      os.mkdir(out_folder + os.sep + "int8")
#    if not os.path.exists(out_folder + os.sep + "uint8"):
#      os.mkdir(out_folder + os.sep + "uint8")
#    if not os.path.exists(out_folder + os.sep + "int16"):
#      os.mkdir(out_folder + os.sep + "int16")
    if not os.path.exists(out_folder + os.sep + "uint16"):
        os.mkdir(out_folder + os.sep + "uint16")
#    if not os.path.exists(out_folder + os.sep + "int32"):
#        os.mkdir(out_folder + os.sep + "int32")
#    if not os.path.exists(out_folder + os.sep + "uint32"):
#        os.mkdir(out_folder + os.sep + "uint32")
#    if not os.path.exists(out_folder + os.sep + "float"):
#        os.mkdir(out_folder + os.sep + "float")

    # Data looks like:
    # 0.06304i ED E2 0F 15 32 82 08 21 FE 00 00 AE 05 FF 79 35 10 75 1D A9 33 98 B7 32 DB 5E B8 88 23 0B 0E 28 01 EA DB 58 1E 6D 10 00 00 B2 CF 38 C6 74 48 E9 74 95 4E 2F 5C 67 55 C7 A1 ED 14 00 03 C0 43 B7 88 3C 54 CA 4C 20 87 3D FE B4 01 15 D7 4F 44 4C F5 13 83 FF FC 25 B9 7C FC DE F7 74 39 CB 0F F9 E0 05 7C 01 00 68 46 BF
    # 0.22304i ED E2 0F 15 32 94 08 21 73 00 AD 00 45 5E 81 59 14 3D 87 00 FE FE 09 EE 00 00 3B BC 00 00 E2 C2 00 00 01 63 22 00 18 31 00 00 6A D7 00 00 00 00 00 00 00 00 00 00 10 00 00 00 FC 59 00 00 66 B9 00 00 F3 AE 00 00 C2 CB 00 D6 1A BE 07 91 9C 8C 00 00 33 73 DA 30 53 25 FA 5F 53 2C 8B A3 B6 CC 00 00 FF F2 00 00 00 2E

    # List of created images
    images_output = []

    # Predict satellite info
    noaa_15,noaa_18,noaa_19  = 0,0,0
    for s in logs_data:
        hex_strs = s.split(' ')
        sfid = int(hex_strs[3], 16)
        if sfid == 8:
            noaa_15 += 1
        elif sfid == 13:
            noaa_18 += 1
        elif sfid == 15:
            noaa_19 +=1
    if noaa_15 > noaa_18 and noaa_15 > noaa_19:
        print "Satellite: NOAA15\n"
    elif noaa_18 > noaa_15 and noaa_18 > noaa_19:
        print "Satellite: NOAA18\n"
    elif noaa_19 > noaa_15 and noaa_19 > noaa_18:
        print "Satellite: NOAA19\n"

    # Number of hex values in each string
    max_len = len(logs_data[0].split(' '))
    # Try all offsets from 0 to max
    for offset in range(1, max_len-3, 2):
        filename8u = out_folder + os.sep + 'uint8' + os.sep + 'graph-8bitU-{:03d}.png'.format(offset)
        filename8s = out_folder + os.sep + 'int8' + os.sep + 'graph-8bitS-{:03d}.png'.format(offset)
        filename16u = out_folder + os.sep + 'uint16' + os.sep + 'graph-16bitU-{:03d}.png'.format(offset)
        filename16s = out_folder + os.sep + 'int16' + os.sep + 'graph-16bitS-{:03d}.png'.format(offset)
        filename32u = out_folder + os.sep + 'uint32' + os.sep + 'graph-32bitU-{:03d}.png'.format(offset)
        filename32s = out_folder + os.sep + 'int32' + os.sep + 'graph-32bitS-{:03d}.png'.format(offset)
        filename32f = out_folder + os.sep + 'float' + os.sep + 'graph-32bitF-{:03d}.png'.format(offset)
        
        x_values = []
        # Data as 1byte values
        y_values_8U = []
        y_values_8S = []
        # Data as 2-bytes unsigned/signed ints
        y_values1_16U = []
        y_values2_16U = []
        y_values1_16S = []
        y_values2_16S = []
        # Data as 4-bytes unsigned ints
        y_values1_32U = []
        y_values2_32U = []
        y_values1_32S = []
        y_values2_32S = []
        # Data as 4-bytes float
        y_values1_32f = []
        y_values2_32f = []
        for s in logs_data:
            # Get string parts like 'ED', 'E2', '0F', '15', '32'
            hex_strs = s.split(' ')
            if len(hex_strs) < 100:
                continue
            
            # Data filter: check timestamp and satellite type for filtering
            s0,s1,s2,s3,s4,s5 = hex_strs[1], hex_strs[2], hex_strs[3], hex_strs[4], hex_strs[5], hex_strs[6]
            p0,p1,p2,p3,p4,p5 = int(s0, 16), int(s1, 16), int(s2, 16), int(s3, 16), int(s4, 16), int(s5, 16)
            sfid = int(hex_strs[3], 16)
            if sfid != 8 and sfid != 13 and sfid != 15:
                continue
            val1 = 256*p0 + p1
            val2 = 256*p2 + p3
            val3 = 256*p4 + p5
            # print "H", s0,s1,s2,s3,s4,s5
            if val3 < 0x3000 or val3 >= 0x4000:
                continue

            # Timestamp: 0.06304i => 0.06304
            dt = float(hex_strs[0][:-1])
            x_values.append(dt)

            # Fields with offset
            s0,s1,s2,s3 = hex_strs[offset], hex_strs[offset+1], hex_strs[offset+2], hex_strs[offset+3]
            p0,p1,p2,p3 = int(s0, 16), int(s1, 16), int(s2, 16), int(s3, 16)
            
            # Parse numbers as 1-byte values
            # y_values_8U.append(p0)
            # y_values_8S.append(s8(p0))

            # Parse numbers as 2-bytes unsigned ints
            val1 = 256*p0 + p1
            val2 = 256*p1 + p0
            y_values1_16U.append(val1)
            y_values2_16U.append(val2)
            # val1 = signed(val1)
            # val2 = signed(val2)
            # y_values1_16S.append(val1)
            # y_values2_16S.append(val2)
            
            # Parse numbers as 4-bytes unsigned ints
            val1 = 256*(256*p0 + p1) + 256*p2 + p3
            val2 = 256*(256*p3 + p2) + 256*p1 + p0
            y_values1_32U.append(val1)
            y_values2_32U.append(val2)
            # val1 = signed32(val1)
            # val2 = signed32(val2)
            # y_values1_32S.append(val1)
            # y_values2_32S.append(val2)
            
            # Parse numbers as floats
            val1 = struct.unpack('!f', (s0 + s1 + s2 + s3).decode('hex'))[0]
            val2 = struct.unpack('!f', (s3 + s2 + s1 + s0).decode('hex'))[0]
            y_values1_32f.append(val1)
            y_values2_32f.append(val2)

        # Save graph: 16bit
        legend1 = 'Int16U[{}:{}]'.format(offset, offset+1)
        legend2 = 'Int16U[{}:{}]'.format(offset+1, offset)
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(image_width, image_height), dpi=image_dpi)
        ax.plot(x_values, y_values1_16U, 'ro', markersize=1, linestyle='--', label=legend1)
        plt.legend()
        plt.ylabel(legend1)
        loc = plticker.MultipleLocator(base=10.0) # this locator puts ticks at regular intervals
        ax.xaxis.set_major_locator(loc)
        ax.margins(0, 0)
        fig.savefig(filename16u, bbox_inches='tight')
        plt.close(fig)
        images_output.append(filename16u)

#        legend1 = 'Int16I[{}:{}]'.format(offset, offset+1)
#        legend2 = 'Int16I[{}:{}]'.format(offset+1, offset)
#        fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(image_width, image_height), dpi=image_dpi)
#        ax.plot(x_values, y_values1_16S, 'ro', markersize=1, linestyle='--', label=legend1)
#        #ax.plot(x_values, y_values2_16S, 'go', markersize=1, linestyle='--', label=legend2)
#        plt.legend()
#        fig.savefig(filename16s)
#        plt.close(fig)

        # Save graph: 32bit
#        legend1 = 'UInt32[{}:{}]'.format(offset, offset+3)
#        legend2 = 'UInt32[{}:{}]'.format(offset+3, offset)
#        plt.xlabel('X')
#        fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(image_width, image_height), dpi=image_dpi)
#        ax.plot(x_values, y_values1_32U, 'ro', markersize=1, linestyle='--', label=legend1)
#        #ax.plot(x_values, y_values2_32U, 'go', markersize=1, linestyle='--', label=legend2)
#        plt.legend()
#        fig.savefig(filename32u)
#        plt.close(fig)

#        legend1 = 'Int32[{}:{}]'.format(offset, offset+3)
#        legend2 = 'Int32[{}:{}]'.format(offset+3, offset)
#        plt.xlabel('X')
#        fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(image_width, image_height), dpi=image_dpi)
#        ax.plot(x_values, y_values1_32S, 'ro', markersize=1, linestyle='--', label=legend1)
#        #ax.plot(x_values, y_values2_32S, 'go', markersize=1, linestyle='--', label=legend2)
#        plt.legend()
#        fig.savefig(filename32s)
#        plt.close(fig)

        print "Offset {}: files saved".format(offset)
          
    # Combine images to a big one
    # Get image size
    img_first = Image.open(images_output[0])
    width, height = img_first.size
    
    # Save images
    print "Combine images..."
    count = len(images_output)
    img_output = Image.new('RGB', (width, (height + 5)*count), color=(255,255,255))
    for index, file in enumerate(images_output):
        img = Image.open(file)
        img_output.paste(img, (0, (height + 5)*index))
        print "{}, {} of {} added".format(file, index+1, count)
    print "Save result..."
    img_output.save(graph_output)

    print "Done. {} saved".format(graph_output)

