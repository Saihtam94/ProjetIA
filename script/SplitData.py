print("Splitting data")

from os import listdir
from os.path import isfile, join, isdir
from sklearn.model_selection import train_test_split
import csv

csvsPath = "../data/csv-data/"
test_size = 0.2
random_state=0

emailsFileList = [f for f in listdir(csvsPath) if f.startswith("emails_")]
print(emailsFileList)
for file in emailsFileList:
    print(file)
    emailFilename = join(csvsPath, file)
    csvFile = open(emailFilename, 'r', newline='')
    fileReader = csv.reader(csvFile, delimiter=',')
    dataframe = []
    targets = []
    next(fileReader)
    for line in fileReader:
        targets.append(line.pop())
        dataframe.append(list(map(float, line)))
    X_train, X_test, y_train, y_test = train_test_split(dataframe, targets, test_size=test_size, random_state=random_state)
    
    x_train_file = open(csvsPath+file[:-4] + "_x_train.csv", 'w', newline='')
    x_train_fileWriter = csv.writer(x_train_file, delimiter=',')
    y_train_file = open(csvsPath+file[:-4] + "_y_train.csv", 'w', newline='')
    y_train_fileWriter = csv.writer(y_train_file, delimiter=',')
    x_test_file = open(csvsPath+file[:-4] + "_x_test.csv", 'w', newline='')
    x_test_fileWriter = csv.writer(x_test_file, delimiter=',')
    y_test_file = open(csvsPath+file[:-4] + "_y_test.csv", 'w', newline='')    
    y_test_fileWriter = csv.writer(y_test_file, delimiter=',')
    
    for line in X_train:
        x_train_fileWriter.writerow(line)
    for line in y_train:
        y_train_fileWriter.writerow([line])
    for line in X_test:
        x_test_fileWriter.writerow(line)
    for line in y_test:
        y_test_fileWriter.writerow([line])

print("Splitting data DONE.")
