from os import listdir
from os.path import isfile, join, isdir
import csv
import numpy
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

csvsPath = "../../data/csv-data/"

emailsFileList = [f for f in listdir(csvsPath) if f.startswith("emails_")]
for file in emailsFileList:
	if isdir(join(csvsPath, file)):
		dirname = join(csvsPath, file)
		xtestfile = join(dirname, file) + '_x_test.csv'
		xtestCsvFile = open(xtestfile, 'r', newline='')
		fileReader = csv.reader(xtestCsvFile, delimiter=',')

		X_test = []
		for line in fileReader:
			X_test.append(list(map(float, line)))

		ytestfile = join(dirname, file) + '_y_test.csv'
		ytestCsvFile = open(ytestfile, 'r', newline='')
		fileReader = csv.reader(ytestCsvFile, delimiter=',')

		y_test = []
		for line in fileReader:
			y_test.append(line.pop())

		xtrainfile = join(dirname, file) + '_x_train.csv'
		xtrainCsvFile = open(xtrainfile, 'r', newline='')
		fileReader = csv.reader(xtrainCsvFile, delimiter=',')

		X_train = []
		for line in fileReader:
			X_train.append(list(map(float, line)))

		ytrainfile = join(dirname, file) + '_y_train.csv'
		ytrainCsvFile = open(ytrainfile, 'r', newline='')
		fileReader = csv.reader(ytrainCsvFile, delimiter=',')

		y_train = []
		for line in fileReader:
			y_train.append(line.pop())

		# SVM
		svc = SVC(C=10, gamma='scale', kernel='rbf')
		svc.fit(X_train, y_train)
		result = svc.predict(X_test)
		classif_report = classification_report(y_test, result)
		print("\n### SVM for "+ file.split("_")[1] +" ###")
		print(classif_report)

		print("accuracy_score = " + str(accuracy_score(y_test, result)))
		