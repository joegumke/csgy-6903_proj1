# http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/#a-python-implementation
''' Allows scoring of text using n-gram probabilities '''
from math import log10

class ngram_score(object):
    def __init__(self,ngramfile):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        # split Ngram dataset into variables, delimited by spaces
        for line in ngramfile.splitlines():
            key,count = line.split(' ')
            self.ngrams[key] = int(count)

        self.L = len(key)

        # total sum of Ngrams in given dataset
        self.N = sum(self.ngrams.values())
        
        #calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)
        self.floor = log10(0.01/self.N)

    def score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams: score += ngrams(text[i:i+self.L])
            else: score += self.floor          
        return score
       
