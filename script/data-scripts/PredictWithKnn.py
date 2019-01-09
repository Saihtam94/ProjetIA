from os import listdir
from os.path import isfile, join, isdir
import csv

csvsPath = "../../data/csv-data/"

emailsFileList = [f for f in listdir(csvsPath) if f.startswith("emails_")]
for file in emailsFileList:
	emailFilename = join(csvsPath, file)
	csvFile = open(emailFilename, 'r', newline='')
	fileReader = csv.reader(csvFile, delimiter=',')
	for line in fileReader:
		# line[0] => from
		# line[1] => to
		# line[2] => subject
		# line[3] => body
		# line[4] => body-stemming
		# line[5] => body-lemmatization
		# line[6] => cc
		# line[7] => bcc
		# line[8] => target
		