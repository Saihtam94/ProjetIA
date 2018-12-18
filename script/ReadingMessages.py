
from os import listdir
from os.path import isfile, join, isdir

folder = "../data/raw-data/maildir/"
persons = ["allen-p", "arnold-j"]

if 'persons' in globals():
	if len(persons) == 0:
		persons = [ name for name in listdir(folder) if isdir(join(folder, name)) ]

print(persons)
for person in persons:
	personMaildirFolder = join(folder, person)
	if isdir(personMaildirFolder):
		personCategoriesFolders = [f for f in listdir(personMaildirFolder) if isdir(join(personMaildirFolder, f))]
		for category in personCategoriesFolders:
			personOneCategoryFolder = join(personMaildirFolder, category)
			personCategoryMailFiles = [f for f in listdir(personOneCategoryFolder) if isfile(join(personOneCategoryFolder, f))]
