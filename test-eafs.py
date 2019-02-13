import xml.etree.ElementTree as ET
import os
import sys

# global variables / constants
eafpath = 'input'
filefile = "files.csv"
tierfile = "tiers.csv"
tiers = {}
filecount = 0
tiercount = 0
fileerror = False
tiererror = False

# check input folder exists
if not os.path.isdir(eafpath):
	print("Warning: could not find \'" + eafpath + "\' folder, creating one.")
	print("Copy your EAF files/folders into the '" + eafpath + "' folder.")
	os.makedirs(eafpath)
	sys.exit()

# check files
print("Searching ...")

# parse every EAF file and count tiers, storing all found tiers in a hash table
# write the tier count to a CSV
output = open(filefile,"w")
for dirpath, dirs, files in os.walk(eafpath):  
    for filename in files:
        pathname = dirpath + "\\" + filename
        name, ext = os.path.splitext(filename)
        if ext == ".eaf":
            xmltree = ET.parse(pathname)
            xmlroot = xmltree.getroot()
            count = 0
            for child in xmlroot.iter("TIER"):
                tiername = child.get("TIER_ID")
                try:
                    tiers[tiername] = tiers[tiername] + 1
                except KeyError:
                    tiers[tiername] = 1
                count = count + 1
            output.write(name + "," + str(count) + "\n")
            if filecount == 0:
                filecount = count
            elif filecount != count:
                filerror = True
output.close()

# write the file counters per tier to another CSV
output = open(tierfile,"w")
for key, value in tiers.items():
    output.write(key + "," + str(value) + "\n")
    if tiercount == 0:
        tiercount = value
    elif tiercount != value:
        tiererror = True
output.close()

# all done
if not filecount:
    print("No files found. Copy your EAF files/folders into the \'" + eafpath + "\' folder.")
    sys.exit()
if fileerror:
    print("Warning: not all EAFs have the same number of tiers! (see " + filefile + ")")
else:
    print("Relax! All EAFs have the same number of tiers (" + str(filecount) + ").")  
if tiererror:
    print("Warning: not all tiers are found in all EAFs! (see " + tierfile + ")")
else:
    print("That's nice! All tiers are found in the same number of EAFs (" + str(tiercount) +").")

