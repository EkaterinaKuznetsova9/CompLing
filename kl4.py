import re
import numpy as np
import random
from sklearn import svm
from sklearn.metrics import hinge_loss
from sklearn.svm import LinearSVC

dictionary = {}
titles = []
subtitles = []
file = open('Dictionary.txt', 'r')
i=0
for line in file:
    line = re.sub(r'[\n\r\t]', '', line)
    dictionary[line] = i
    i+=1
print(dictionary)
file.close()

file = open('Texts10.txt', 'r')
fileInd = open('TextsAsIndexes.txt', 'w')
titlesAsIndexes = []
subtitlesAsIndexes = []
i=0
for line in file:
    line = re.sub(r'[^\w\s]', '', line)
    line = re.sub('\d', '', line)
    line = re.sub(r'[\n\r\t]', '', line)
    words = line.split(' ')
    newLineInd = ""
    tmpLineIndexes = []
    for word in words:
        if word != "":
            word = word.lower()
            if word in dictionary:
                newLineInd+=str(dictionary[word])
                newLineInd+= " "
                tmpLineIndexes.append(str(dictionary[word]))
    if i%2 == 0:
        titles.append(line)
        titlesAsIndexes.append(tmpLineIndexes)
    else:
        subtitles.append(line)
        subtitlesAsIndexes.append(tmpLineIndexes)
    i+=1
    fileInd.write(newLineInd + "\n")
file.close()
fileInd.close()

print("Number of words in dictionary: ", len(dictionary))
numTexts = i/2
print("Number of texts: ", int(numTexts))

# initialize for each word a random vector of some length
n_vectors = len(dictionary)
d=2
rnd_vec = np.random.uniform(-1, 1, size=(n_vectors, d))
unif = np.random.uniform(size=n_vectors)
scale_f = np.expand_dims(np.linalg.norm(rnd_vec, axis = 1)/unif, axis = 1)
rnd_vec = rnd_vec/scale_f
print(rnd_vec)

print(titles)
print(subtitles)

# Randomly select three
randomNum = random.randint(0,len(titles)-1)
randTitle = titles[randomNum]
randSubTitle = subtitles[randomNum]
otherRandomNum = random.randint(0,len(titles)-1)
while otherRandomNum == randomNum:
    otherRandomNum = random.randint(0, len(titles) - 1)
otherRandSubtitle = subtitles[otherRandomNum]

print("Random two number:", randomNum, otherRandomNum)

print(titlesAsIndexes)
print(subtitlesAsIndexes)

# the result of the aggregation function (max) on each title and subtitle
titlesAsVectors = []
subtitlesAsVectors = []
vecMaxesTitles = []
vecMaxesSubtitles = []
for iLine in range(len(titlesAsIndexes)):
    xVectorsInEachTitle = []
    yVectorsInEachTitle = []
    tmpLineVectors = []
    for ind in titlesAsIndexes[iLine]:
        tmpLineVectors.append(rnd_vec[int(ind)])
        xVectorsInEachTitle.append(rnd_vec[int(ind)][0])
        yVectorsInEachTitle.append(rnd_vec[int(ind)][1])
    titlesAsVectors.append(tmpLineVectors)

    xVectorsInEachSubtitle = []
    yVectorsInEachSubtitle = []
    tmpLineVectors = []
    for ind in subtitlesAsIndexes[iLine]:
        tmpLineVectors.append(rnd_vec[int(ind)])
        xVectorsInEachSubtitle.append(rnd_vec[int(ind)][0])
        yVectorsInEachSubtitle.append(rnd_vec[int(ind)][1])
    subtitlesAsVectors.append(tmpLineVectors)

    xMaxTitle = max(xVectorsInEachTitle)
    yMaxTitle = max(yVectorsInEachTitle)
    xMaxSubtitle = max(xVectorsInEachSubtitle)
    yMaxSubtitle = max(yVectorsInEachSubtitle)
    tmpXYMaxInEachText = []
    tmpXYMaxInEachText.append(xMaxTitle)
    tmpXYMaxInEachText.append(yMaxTitle)
    vecMaxesTitles.append(tmpXYMaxInEachText)
    tmpXYMaxInEachText = []
    tmpXYMaxInEachText.append(xMaxSubtitle)
    tmpXYMaxInEachText.append(yMaxSubtitle)
    vecMaxesSubtitles.append(tmpXYMaxInEachText)
print(titlesAsVectors)
print(subtitlesAsVectors)
print("vecMaxesTitles:", vecMaxesTitles)
print("vecMaxesSubtitles:", vecMaxesSubtitles)

# we have title, subtitle, other subtitle
print("title: ", vecMaxesTitles[randomNum])
print("subtitle: ", vecMaxesSubtitles[randomNum])
print("other subtitle: ", vecMaxesSubtitles[otherRandomNum])

vec1 = vecMaxesTitles[randomNum]
vec2 = vecMaxesSubtitles[randomNum]
vec3 = vecMaxesSubtitles[otherRandomNum]
# vec1 - it is u - title
# vec2 - it is i - subtitle
# vec3 - it is j - other subtitle
f_ui = np.dot(vec1, vec2)
f_uj = np.dot(vec1, vec3)
mrl = max(0, 1 - f_ui + f_uj)
print("mrl: ", mrl)


dMRL_u = 0-i+j
dMRL_i=0
dMRL_j = 0



# print(np.gradient(max(0, 1 - f_ui + f_uj)))
# dMRL/du, dMRL/di, dMRL,dj

# V = max(0, 1 - np.dot(vec1, vec2) + np.dot(vec1, vec3))
# Ex,Ey,Ez = np.gradient(V)
# print(Ex, Ey, Ez)

#
# X = [[vecMaxes[0][0]], [vecMaxes[0][1]]]
# y = [-1, 1]
# est = svm.LinearSVC(random_state=0)
# est.fit(X, y)
# LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
#      intercept_scaling=1, loss='squared_hinge', max_iter=1000,
#      multi_class='ovr', penalty='l2', random_state=0, tol=0.0001,
#      verbose=0)
# pred_decision = est.decision_function(X)
# print(pred_decision)
# print(hinge_loss([-1, 1], pred_decision))


