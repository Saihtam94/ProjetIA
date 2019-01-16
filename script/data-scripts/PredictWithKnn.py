from os import listdir
from os.path import isfile, join, isdir
import csv
import numpy
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

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

	le = LabelEncoder()
	y = le.fit_transform(targets)
	X_train, X_test, y_train, y_test = train_test_split(dataframe, y, test_size=0.2)

	# KNN
	neigh = KNeighborsClassifier(n_neighbors=4, weights="distance")
	neigh.fit(X_train, y_train)
	result = neigh.predict(X_test)
	classif_report = classification_report(y_test, result)
	print("\n### KNN for "+ file.split("_")[1] +" ###")
	print(classif_report)
		