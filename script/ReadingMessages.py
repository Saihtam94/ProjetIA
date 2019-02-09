
from os import listdir
from os.path import isfile, join, isdir
import csv
from random import randint

from PrepareTexts import *

dbFolder = "../data/raw-data/maildir/"

persons = ["badeer-r"] # KNN = SVM with seed = 11
persons = ["hyatt-k"]
categoriesToRemove = ['_sent_mail', 'deleted_items', 'all_documents', 'sent_items', 'inbox', 'sent', 'contacts', 'notes_inbox', 'discussion_threads', 'calendar']
numberOfWordToRemain = 15
subjectWordsWeight = 0 # 0 = disable the feature

categoriesNumber = dict()

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

        csvFileBodyOnly = open(csvFileName + "_" + person + "_body_only.csv", 'w', newline='')
        fileWriterBodyOnly = csv.writer(csvFileBodyOnly, delimiter=csvDelimiter)

        personMaildirFolder = join(databasePath, person)
        if isdir(personMaildirFolder):
            personCategoriesFolders = [f for f in listdir(personMaildirFolder) if isdir(join(personMaildirFolder, f)) and f not in categoriesToRemove]
            fileCount = 0
            for category in personCategoriesFolders:
                personOneCategoryFolder = join(personMaildirFolder, category)
                personCategoryMailFiles = [f for f in listdir(personOneCategoryFolder) if isfile(join(personOneCategoryFolder, f))]
                fileCount += len(personCategoryMailFiles)

            wordMatrix = []
            headList = []
            wordCount = dict()
            loading = 0
            # Reading mails for one person
            for category in personCategoriesFolders:

                personOneCategoryFolder = join(personMaildirFolder, category)
                personCategoryMailFiles = [f for f in listdir(personOneCategoryFolder) if isfile(join(personOneCategoryFolder, f))]
                categoriesNumber[category] = len(personCategoryMailFiles)
                for filename in personCategoryMailFiles:
                    loading += 1
                    if loading % 50 == 0:
                        print("loading [" + str(int(loading * 100 / fileCount)) + "%]")
                    filepath = join(personOneCategoryFolder, filename)
                    file = open(filepath, "r", encoding = "ISO-8859-1")
                    oneLineCSV = parseRawMessage(file.read())
                    oneLineCSV["body"] = parseBodyLemmatization(oneLineCSV["text-body"])
                    #oneLineCSV["body-stemming"] = parseBodyStemming(oneLineCSV["text-body"])
                    #oneLineCSV["body-lemmatization"] = parseBodyLemmatization(oneLineCSV["text-body"])
                    oneLineCSV["target-category"] = category
                    oneLineCSV.pop("text-body")

                    wordList = dict()
                    for word, value in oneLineCSV["body"].items():
                        if word not in headList:
                            headList.append(word)
                        wordList[word] = value
                        try:
                            wordCount[word] += value
                        except KeyError as e:
                            wordCount[word] = value

                    if subjectWordsWeight != 0:
                        subjectBagOfWordToAdd = dict()
                        parseSubject(oneLineCSV["subject"], subjectBagOfWordToAdd)
                        for word, value in subjectBagOfWordToAdd.items():
                            value *= subjectWordsWeight
                            if word not in headList:
                                headList.append(word)
                            try:
                                wordList[word] += value
                            except KeyError as e:
                                wordList[word] = value
                            try:
                                wordCount[word] += value
                            except KeyError as e:
                                wordCount[word] = value

                    wordList["target-category"] = category
                    wordMatrix.append(wordList)



            # Writing in CSV

            # wordCountMaxes = []
            # wordCountCopy = list(wordCount.values()).copy()
            # for numberOfWordToRemainIndex in range(1,numberOfWordToRemain):
            #     wordCountMax = max(wordCountCopy)
            #     wordCountMaxes.append(wordCountMax)
            #     wordCountCopy.pop(wordCountCopy.index(wordCountMax))
            # print(wordCountMaxes)
            wordInHeadListCount = 0
            for word in headList:
                if wordCount[word] < numberOfWordToRemain:
                    headList.pop(wordInHeadListCount)
                wordInHeadListCount += 1
            headList.append("target-category")
            fileWriterBodyOnly.writerow(headList)
            for line in wordMatrix:
                oneLineCSV = []
                for word in headList:
                    try:
                        if wordCount[word] > numberOfWordToRemain:
                            try:
                                oneLineCSV.append(line[word])
                            except KeyError as e:
                                oneLineCSV.append(0)
                    except KeyError as err: # For target-category
                        oneLineCSV.append(line[word])
                fileWriterBodyOnly.writerow(oneLineCSV)
            csvFileBodyOnly.close()

def alea_accuracy():
    categoriesInList = list(categoriesNumber.keys())
    csvsPath = "../data/csv-data/"
    emailsFileList = [f for f in listdir(csvsPath) if isfile(join(csvsPath, f)) and f.startswith("emails_")]
    for file in emailsFileList:
        emailFilename = join(csvsPath, file)
        csvFile = open(emailFilename, 'r', newline='')
        fileReader = csv.reader(csvFile, delimiter=',')
        dataframe = []
        targets = []
        next(fileReader)
        i = 0
        compteur = 0
        for line in fileReader:
            targets.append(line.pop())
            dataframe.append(list(map(float, line)))
        for target in targets:
            alea = randint(0, len(categoriesNumber)-1)
            if (categoriesInList[alea] == targets[i]):
                compteur += 1
            i += 1
        accuracy = compteur / i * 100
        print("random accuracy = " + str(accuracy))

dataPrepare(dbFolder, persons)
alea_accuracy()
