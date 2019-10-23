import os
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
from collections import defaultdict
import numpy as np
import pandas

#----------------week1----------------

# d = os.getcwd()
# l=[]
# os.chdir(d+"/Train-corups-1")
# for (root,dirs,files) in os.walk('.', topdown = True):
#     for file in files:
#         di = file[:2]
#         f = open(d+"/Train-corups-1/"+"/"+di+"/"+file)
#         tree = ET.parse(f)
#         root = tree.getroot()
#         for item in root.findall('.//w'):    #??????????????????????????
#             key=item.attrib['hw']
#             val=item.attrib['c5']
#             if "-" in val:
#                 z=val.split("-")
#                 for x in z:
#                     l.append(key+"_"+x)
#             else:
#                 l.append(key+"_"+val)

# print(len(l))
# os.chdir(d)
# print(os.getcwd())
# file=open("1.txt",'w')
# for i in l:
# 	file.write(i+"\n")

# file.close()

# print("#week1")


#----------------week2----------------

dictionary = {}

outputfile = open("2.txt","w")

inputfile = open("1.txt")

for line in inputfile:
	for word in line.split():	#word is word_tag 
		if word in dictionary:
			dictionary[word] +=1
		else:
			dictionary[word] =1
inputfile.close()

length = len(dictionary)
print ("No. of words in Dictionary= "+str(length)+"\n")

for dict_word, freq in dictionary.items():
	outputfile.write(str(dict_word) + ": " + str(freq) + "\n")

outputfile.close()

print("week2")

#----------------week3----------------

word_dict= {}
tag_dict= {}

for word, freq in dictionary.items():	#word is word_tag
	if word.find("_") != -1:
		arr=word.split("_")
		
		if arr[0] in word_dict:
			word_dict[arr[0]]+=freq
		else:
			word_dict[arr[0]]=freq

		if arr[1] in tag_dict:
			tag_dict[arr[1]]+=freq
		else:
			tag_dict[arr[1]]=freq

#print(word_dict)
#print(tag_dict)

sortedword_dict = sorted(word_dict.items(), key = lambda kv: kv[1])
sortedtag_dict =sorted(tag_dict.items(), key = lambda kv: kv[1])

sortedword_dict.reverse()
sortedtag_dict.reverse()

wordfreqfile = open("top10_word.txt", "w")

for i in range(0,10):
	wordfreqfile.write(str(sortedword_dict[i])+"\n")

wordfreqfile.close()

tagfreqfile = open("top10_tag.txt", "w")

for i in range(0,10):
	tagfreqfile.write(str(sortedtag_dict[i])+"\n")

tagfreqfile.close()

xt = []
yt = []

for i in range(0,10):
	xt.append(sortedtag_dict[i][0])
	yt.append(sortedtag_dict[i][1])

plt.bar(xt,yt)
plt.show()

x = []
y = []

for i in range(0,10):
	x.append(sortedword_dict[i][0])
	y.append(sortedword_dict[i][1])

plt.bar(x,y)
plt.show()

#----------------week4----------------

prob_word= dict()

word_taglen=len(word_dict)
arrtag = tag_dict.keys()

for word, freq in word_dict.items():	#word_dict : word freq dictionary
	prob_tagdict=dict()
	for tag in arrtag:
		word_tag= word + "_" + tag
		if word_tag in dictionary:
			prob_tagdict[tag] = dictionary[word_tag]/freq	#dictionary : word_tag frequency
		else:
			prob_tagdict[tag]=0.0
	prob_word[word]= prob_tagdict

#print(prob_word)

probabilityfile = open("probability.txt","w")

for word,prob in prob_word.items():
	probabilityfile.write(str(word)+": "+str(prob)+"\n"+"\n")

probabilityfile.close()

print("week4")

#----------------week5----------------

d = os.getcwd()
print(d)
l5=[]
np=0
c=0
inc=0
os.chdir(d+"/Test-corpus-1")
for (root,dirs,files) in os.walk('.', topdown = True):
	for file in files:
		di = file[:2]
		f = open(d+"/Test-corpus-1/"+"/"+di+"/"+file)
		tree = ET.parse(f)
		root = tree.getroot()
		for item in root.findall('.//w'):
			#k=item.attrib['hw']
			k=item.text.strip().lower()
			t=item.attrib['c5'] #actual tag
			y=t.split("-")
			for x in y:
				try:
					mx_tag=""
					mx=0
					Dict=prob_word[k]
					for ta in Dict:
						if mx<Dict[ta]:
							mx=Dict[ta]
							mx_tag=ta
					l5.append(k+"_"+mx_tag+" "+k+"_"+x)
					if mx_tag==x:
						c=c+1
					else:
						inc=inc+1
				except KeyError:
					l5.append("none")
					np=np+1


y1=c*100
y1=y1/(c+inc)
print(c)
print(inc)
print(len(l5))
print(y1)
os.chdir(d)
fil=open("5.txt","w")
for i in l5:
	fil.write(i+"\n")

print("week5")

#--------------week6---------------

Dict_index={}
i = 0
for tag, freq in tag_dict.items():
	Dict_index[tag] = i
	i += 1

confusionmatrix=defaultdict(lambda:defaultdict(int))
# for tagi, freqi in tag_dict.items():
# 	for tagj, freqj in tag_dict.items():
# 		confusionmatrix[Dict_index[tagi]][tagj]=0



d = os.getcwd()
os.chdir(d+"/Test-corpus-1")
for (root,dirs,files) in os.walk('.', topdown = True):
	for file in files:
		di = file[:2]
		f = open(d+"/Test-corpus-1/"+"/"+di+"/"+file)
		tree = ET.parse(f)
		root = tree.getroot()
		for item in root.findall('.//w'):
			#k=item.attrib['hw']
			k=item.text.strip().lower()
			if k in prob_word:
				lis=item.attrib['c5'].split('-') #actual tag
				for ha in lis:
					actual=ha
					mx_tag=""
					mx=0
					Dict=prob_word[k]
					for ta in Dict:
						if mx<Dict[ta]:
							mx=Dict[ta]
							mx_tag=ta
					predicted=mx_tag
					confusionmatrix[actual][predicted]+=1		


total=0
correct=0
accuracy=0

for i in  confusionmatrix:
	for j in confusionmatrix[i]:
		total+=confusionmatrix[i][j]
	correct+=confusionmatrix[i][i]
	#print("\n")

accuracy=correct/total
print(accuracy)



prettymaxtrix=[]
for tagi,freqi in tag_dict.items():
	temp=[]
	for tagj,freqj in tag_dict.items():
		temp.append(confusionmatrix[tagi][tagj])
	prettymaxtrix.append(temp)

# nene=np.asarray(prettymaxtrix)
# for i in prettymaxtrix:
# 	for j in prettymaxtrix[i]:
# 		print(prettymaxtrix[i][j],end=" ")
# 	print("\n")

#print(prettymaxtrix)
df = pandas.DataFrame(prettymaxtrix)

print(df)
os.chdir(d)
df.to_csv('confusionmatrix.csv', header=True, index=False, sep='\t', mode='a')
