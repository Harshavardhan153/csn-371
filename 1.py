import os
import xml.etree.ElementTree as ET
#----------------week1----------------
print("<week1>")
d = os.getcwd()
l=[]
os.chdir(d+"/Train-corups-1")
for (root,dirs,files) in os.walk('.', topdown = True):
    for file in files:
        di = file[:2]
        f = open(d+"/Train-corups-1/"+"/"+di+"/"+file)
        tree = ET.parse(f)
        root = tree.getroot()
        for item in root.findall('.//w'):    #??????????????????????????
            #key=item.attrib['hw']
            key=item.text.strip().lower()
            val=item.attrib['c5']
            if "-" in val:
                z=val.split("-")
                for x in z:
                    l.append(key+"_"+x)
            else:
                l.append(key+"_"+val)

print(len(l))
os.chdir(d)
print(os.getcwd())
file=open("1.txt",'w')
for i in l:
	file.write(i+"\n")

file.close()

print("</week1>")