from LetterDeleter import LetterDeleter
import json
from JsonDB import JsonDB

class SpellCorrectorNew():

    def __init__(self, aContext, jsondb):
        self.aContext = aContext
        self.letDelter = LetterDeleter()
        self.deletedDB = jsondb.getDeletedWordsDB()

    def checkMatchingWords(self, word):
        matchingWords = []
        self.letDelter.edits = []
        deletedWords = self.letDelter.delete(word, 2)
        for deletedWord in deletedWords:
            try:
                if(len(deletedWord)>1):
                    if(96< ord(deletedWord[0]) < 123):
                        ind1 = ord(deletedWord[0])-97
                    else:
                        ind1 = 26
                    if(96< ord(deletedWord[1]) < 123):
                        ind2 = ord(deletedWord[1])-97
                    else:
                        ind2 = -1
                    matchingWords.append(self.deletedDB["words"][ind1]["words"][ind2][deletedWord])
                else:
                    matchingWords.append(self.deletedDB["words"][27][deletedWord])
            except:
                print("Couldn't find",deletedWord)
        return matchingWords
    
    def getMostRelevantWords(self, matchingWords):
        correctWords =[]
        words = []
        wordFrequency = []
        for wordList in matchingWords:
            for word in wordList:
                try:
                    ind = words.index(word)
                    wordFrequency[ind] = wordFrequency[ind] + 1
                except:
                    words.append(word)
                    wordFrequency.append(1)
        #print("freq",wordFrequency)
        #print("word",words)
        for i in range(5):
            if(len(wordFrequency)==i):
                break
            ind = wordFrequency.index(max(wordFrequency))
            correctWords.append(words[ind])
            wordFrequency[ind] = 0
        return correctWords