import xml.etree.ElementTree as ET
import os

eafpath = '.\\eaf'
tiers = {}
filecount = 0
tiercount = 0
fileerror = False
tiererror = False

output = open("files.csv","w")

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

output = open("tiers.csv","w")

for key, value in tiers.items():
    output.write(key + "," + str(value) + "\n")
    if tiercount == 0:
        tiercount = value
    elif tiercount != value:
        tiererror = True

output.close()

if fileerror:
    print("Warning: not all files have the same number of tiers!")
else:
    print("Relax ... all files have the same number of tiers.")
if tiererror:
    print("Warning: not all tiers are found in all files!")
else:
    print("That's nice ... all tiers are found in the same number of files.")

