import re

file = open('Texts10.txt', 'r')
allTexts = []
dictionaryArray = []
dictionary = {}
dictNumWord = {}
i=0
for line in file:
    line = re.sub(r'[^\w\s]', '', line)
    line = re.sub('\d', '', line)
    line = re.sub(r'[\n\r\t]', '', line)
    allTexts.append(line)
    words = line.split(' ')
    for word in words:
        if word != "":
            word = word.lower()
            dictNumWord[word] = 1
            if word in dictionary:
                dictNumWord[word]+=1
            else:
                dictionary[word] = i
                i += 1
file.close()
print("Dictionary:")
print(dictionary)
print(len(dictionary))
print("Dictionary as numbers of each word:")
print(dictNumWord)

# not use rarely used words
kolWordsInResDict = 0
fileDict = open('Dictionary.txt', 'w')
for word in dictionary:
    # need set condition > 4 maybe and not use prepositions
    if (dictNumWord[word] > 0) and len(word) > 2:
        fileDict.write(word + "\n")
        kolWordsInResDict+=1
fileDict.close()
print(kolWordsInResDict)