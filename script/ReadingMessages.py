
from os import listdir
from os.path import isfile, join, isdir
import csv

from PrepareTexts import *

dbFolder = "../data/raw-data/maildir/"

persons = ["bailey-s"]
if len(persons) == 0:
	persons = [ name for name in listdir(dbFolder) if isdir(join(dbFolder, name)) ]

def parseRawMessage(raw_message):
	lines = raw_message.split('\n')
	email = {"text-body":"", "from":"", "to":"", "subject":"", "cc":"", "bcc":""}
	keys = ['from', 'to', 'subject', 'cc', 'bcc']
	for line in lines:
		if ':' not in line:
			email["text-body"] += line.strip() + " "
		else:
			pairs = line.split(':')
			key = pairs[0].lower()
			val = ""
			for restOfKeysIndex in range(1, len(pairs)):
				val += pairs[restOfKeysIndex].strip()
			if key in keys:
				email[key] = val
	return email
	
def dataPrepare(databasePath, persons, csvFileName="../data/csv-data/emails", csvDelimiter=","):
	for person in persons:

		# csvFile = open(csvFileName + "_" + person + ".csv", 'w', newline='')
		# fileWriter = csv.writer(csvFile, delimiter=csvDelimiter)

		csvFileBodyOnly = open(csvFileName + "_" + person + "_body_only.csv", 'w', newline='')
		fileWriterBodyOnly = csv.writer(csvFileBodyOnly, delimiter=csvDelimiter)

		personMaildirFolder = join(databasePath, person)
		if isdir(personMaildirFolder):
			personCategoriesFolders = [f for f in listdir(personMaildirFolder) if isdir(join(personMaildirFolder, f))]
			
			wordMatrix = []
			headList = []
			for category in personCategoriesFolders:
				personOneCategoryFolder = join(personMaildirFolder, category)
				personCategoryMailFiles = [f for f in listdir(personOneCategoryFolder) if isfile(join(personOneCategoryFolder, f))]
				for filename in personCategoryMailFiles:
					filepath = join(personOneCategoryFolder, filename)
					file = open(filepath, "r")
					oneLineCSV = parseRawMessage(file.read())
					oneLineCSV["body"] = parseBody(oneLineCSV["text-body"])
					#oneLineCSV["body-stemming"] = parseBodyStemming(oneLineCSV["text-body"])
					#oneLineCSV["body-lemmatization"] = parseBodyLemmatization(oneLineCSV["text-body"])
					oneLineCSV["target"] = category
					oneLineCSV.pop("text-body")

					wordList = dict()
					for word, value in oneLineCSV["body"].items():
						if word not in headList:
							headList.append(word)
						wordList[word] = value
					wordList["target"] = category
					wordMatrix.append(wordList)

					# fileWriter.writerow([oneLineCSV["from"],
					# 					 oneLineCSV["to"],
					# 					 oneLineCSV["subject"],
					# 					 oneLineCSV["body"],
					# 					 #oneLineCSV["body-stemming"],
					# 					 #oneLineCSV["body-lemmatization"],
					# 					 oneLineCSV["cc"],
					# 					 oneLineCSV["bcc"],
					# 					 oneLineCSV["target"]])
			fileWriterBodyOnly.writerow(headList)
			for line in wordMatrix:
				oneLineCSV = []
				for word in headList:
					try:
						if line[word]:
							oneLineCSV.append(line[word])
					except KeyError as e:
						oneLineCSV.append(0)
				fileWriterBodyOnly.writerow(oneLineCSV)
					

dataPrepare(dbFolder, persons)
