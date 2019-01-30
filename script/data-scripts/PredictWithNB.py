from os import listdir
from os.path import isfile, join, isdir
import csv
import numpy
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

csvsPath = "../../data/csv-data/"

emailsFileList = [f for f in listdir(csvsPath) if f.startswith("emails_")]
for file in emailsFileList:
	emailFilename = join(csvsPath, file)
	csvFile = open(emailFilename, 'r', newline='')
	fileReader = csv.reader(csvFile, delimiter=',')
	dataframe = []
	targets = []
	next(fileReader)
	for line in fileReader:
		targets.append(line.pop())
		dataframe.append(list(map(float, line)))

	# le = LabelEncoder()
	# y = le.fit_transform(targets)
	X_train, X_test, y_train, y_test = train_test_split(dataframe, targets, test_size=0.2, random_state=11)

	# KNN
	gnb = GaussianNB()
	neigh = gnb.fit(X_train, y_train)
	result = neigh.predict(X_test)
	classif_report = classification_report(y_test, result)
	print("\n### Naive Bayes for "+ file.split("_")[1] +" ###")
	print(classif_report)
	print("accuracy_score = " + str(accuracy_score(y_test, result)))
		