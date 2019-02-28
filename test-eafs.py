import xml.etree.ElementTree as ET
import os
import sys

# global variables / constants
INPUT_PATH = "input"
OUTPUT_FILES = "files.csv"
OUTPUT_TIERS = "tiers.csv"
tier_table = {}
file_count = 0
tier_count = 0
file_error = False
tier_error = False
media_count_error = False
media_order_error = False

# check input folder exists
if not os.path.isdir(INPUT_PATH):
        print("Warning: could not find \'" + INPUT_PATH + "\' folder, creating one.")
        print("Copy your EAF files/folders into the '" + INPUT_PATH + "' folder.")
        os.makedirs(INPUT_PATH)
        sys.exit()

# check files
print("Searching ...")

# parse every EAF file and count tiers storing all found tiers in a hash table
# write the tier count to a CSV
output = open(OUTPUT_FILES,"w")
output.write("filename,tier_count,media_count,shortest_media\n")
for dirpath, dirs, files in os.walk(INPUT_PATH):  
    for filename in files:
        pathname = dirpath + "\\" + filename
        name, ext = os.path.splitext(filename)
        if ext == ".eaf":
            xmltree = ET.parse(pathname)
            xmlroot = xmltree.getroot()
            count = 0
            for child in xmlroot.findall("TIER"):
                tiername = child.get("TIER_ID")
                try:
                    tier_table[tiername] = tier_table[tiername] + 1
                except KeyError:
                    tier_table[tiername] = 1
                count = count + 1
            doc_header = xmlroot.find("HEADER")
            media = 0
            media_count = 0
            media_len = 0
            for descriptor in doc_header.findall("MEDIA_DESCRIPTOR"):
                media_count += 1
                if not media or len(descriptor.get("MEDIA_URL")) < media_len:
                    media = media_count
                    media_len = len(descriptor.get("MEDIA_URL"))
            if media != 1: media_order_error = True
            if media_count != 2: media_count_error = True
            output.write(name + "," + str(count) + "," + str(media_count) + "," + str(media) + "\n")
            if file_count == 0:
                file_count = count
            elif file_count != count:
                filerror = True
output.close()

# write the file counts per tier to another CSV
output = open(OUTPUT_TIERS,"w")
for key, value in tier_table.items():
    output.write(key + "," + str(value) + "\n")
    if tier_count == 0:
        tier_count = value
    elif tier_count != value:
        tier_error = True
output.close()

# all done
if not file_count:
    print("No files found. Copy your EAF files/folders into the \'" + INPUT_PATH + "\' folder.")
else:
        if file_error:
                print("Warning: not all EAFs have the same number of tiers! (see " + OUTPUT_FILES + ")")
        else:
                print("Relax! All EAFs have the same number of tiers (" + str(file_count) + ").")  
        if tier_error:
                print("Warning: not all tiers are found in all EAFs! (see " + OUTPUT_TIERS + ")")
        else:
                print("That's nice! All tiers are found in the same number of EAFs (" + str(tier_count) +").")
        if media_count_error:
                print("Warning: files exist which don't have 2 linked media clips!")
        if media_order_error:
                print("Warning: files exist where the first linked media file doesn't have shortest filename!")
