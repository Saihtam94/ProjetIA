
from os import listdir
from os.path import isfile, join, isdir

dbFolder = "../data/raw-data/maildir/"

persons = ["allen-p"]
if len(persons) == 0:
	persons = [ name for name in listdir(dbFolder) if isdir(join(dbFolder, name)) ]

def parseRawMessage(raw_message):
	lines = raw_message.split('\n')
	email = {"body":"", "from":"", "to":"", "subject":"", "cc":"", "bcc":""}
	keys = ['from', 'to', 'subject', 'cc', 'bcc']
	for line in lines:
		if ':' not in line:
			email["body"] += line.strip()
		else:
			pairs = line.split(':')
			key = pairs[0].lower()
			val = ""
			for restOfKeysIndex in range(1, len(pairs)):
				val += pairs[restOfKeysIndex].strip()
			if key in keys:
				email[key] = val
	return email

def dataPrepare(databasePath, persons):
	for person in persons:
		personMaildirFolder = join(databasePath, person)
		if isdir(personMaildirFolder):
			personCategoriesFolders = [f for f in listdir(personMaildirFolder) if isdir(join(personMaildirFolder, f))]
			for category in personCategoriesFolders:
				personOneCategoryFolder = join(personMaildirFolder, category)
				personCategoryMailFiles = [f for f in listdir(personOneCategoryFolder) if isfile(join(personOneCategoryFolder, f))]
				for filename in personCategoryMailFiles:
					filepath = join(personOneCategoryFolder, filename)
					file = open(filepath, "r")
					oneLineCSV = parseRawMessage(file.read())
					# outputWithoutStopWords = parseBody(oneLineCSV["body"])
					# outputWithoutStopWordsWithStemming = parseBodyStemming(oneLineCSV["body"])
					# outputWithoutStopWordsWithLemmatization = parseBodyLemmatization(oneLineCSV["body"])
					# Add oneLineCSV in CSV file
dataPrepare(dbFolder, persons)