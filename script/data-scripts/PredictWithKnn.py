from os import listdir
from os.path import isfile, join, isdir
import csv
from sklearn.neighbors import KNeighborsClassifier

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


	dataframe = pandas.read_csv(emailFilename)

	X = dataframe.drop(["target"], axis=1)
	le = LabelEncoder()
	y = le.fit_transform(dataframe["target"])

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

	# KNN
	neigh = KNeighborsClassifier(n_neighbors=4, weights="distance")
	neigh.fit(X_train, y_train)
	result = neigh.predict(X_test)
	classif_report = classification_report(y_test, result)
	print("\n### KNN ###")
	print(classif_report)
		