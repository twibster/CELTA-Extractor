import os

names = {}
path ="C:/Users/user/Desktop/Units/"

with open('units.txt','r') as units:
	for unit in units:
		names[unit[5:unit.index(':')]] = unit[unit.index(':')+2:unit.index('SCORM package')].replace(':','-')

for filename in os.listdir("C:/Users/user/Desktop/Units/"):
	unit_name =names.get(filename)
	if unit_name:
		new_name = path+ filename+ '- ' +unit_name
		os.rename(path+filename,new_name)

