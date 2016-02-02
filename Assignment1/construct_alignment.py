
# -*- coding: utf-8 -*-

import re
import sys
import collections
from scipy.sparse import lil_matrix
import numpy as np
import itertools
import numpy.matlib
from scipy.stats import entropy

class Alignment(object):
    def __init__(self, path):
        self.corpusA = []
        self.corpusB = []
        self.vocabA = {}
        self.vocabB = {}
        self.path = path

    def readCorpus(self):
        '''
        Reads parallel corpus from 'path'. 
        Assuming corpus is present in the following schema:
        s1 | s2
        s3 | s4
        ...
        '''
        with open(self.path, 'rb') as f:
            for line in f:
                lineA, lineB = line.split("|")
                self.corpusA.append(lineA.strip())
                self.corpusB.append(lineB.strip())

    def constructVocab(self):
        '''
        Constructs the vocabulary (mapping word:wordID) from data.
        '''
        wordId = 0
        for sentence in self.corpusA:
            for word in sentence.split():
                if word not in self.vocabA:
                    self.vocabA[word] = wordId
                    wordId +=1

        wordId = 0 
        for sentence in self.corpusB:
            for word in sentence.split():
                if word not in self.vocabB:
                    self.vocabB[word] = wordId
                    wordId +=1
        

    def constructAlignment(self, init_mode):
        '''
        Constructs the alignment matrix for parallel corpus in 'path',
        with table initialized with mode 'init_mode'. It can be uniform,
        or some other distribution
        '''
        # Size of the vocabs
        N = float(len(self.vocabA))
        M = float(len(self.vocabB))
        ent = []
        # Alignment matrix to be estimated using EM, initializing with uniform
        if init_mode == 'uniform':
            # If vocab size in both language is same
            if N == M:
                alignMatrix = np.empty((N,N))
                alignMatrix.fill(1/N)
            else:
                # When vocab size is different (ex for German, English pair)
                # Choose randomly between 1/N and 1/M
                choice = random.choice([0,1])
                if choice == 0:
                    alignMatrix = np.empty((N,M))
                    alignMatrix.fill(1/N)
                else:
                    alignMatrix = np.empty((N,M))
                    alignMatrix.fill(1/M)
        # Initializing alignment matrix with random values
        elif init_mode == 'random':
            # In this case vocabulary size difference won't matter
            alignMatrix = np.random.rand(N,M)
        
        ent = [entropy(col) for col in alignMatrix.T]
        print ent
        print "Starting EM" 
        iter_no = 1
        while True:
            # Creating a temporary matrix to store re-estimated values after
            # E-step at each sentence
            temp = np.zeros((2,N,M))
            # Creating one sparse matrix which will be reused for each sentence
            # From parallel corpus
            count = np.zeros((N,M))
            for textA, textB in zip(self.corpusA, self.corpusB):
                # E step for estimating expected counts matrix for each sentence pair
                # Expected count matrices for textA, textB in both corpuses
                count.fill(0.)

                freqA = {}
                freqB = {}
                # Calculate frequency of tokens in both corpuses
                for wordA, wordB in zip(textA.split(), textB.split()):
                    if wordA in freqA:
                        freqA[wordA] += 1
                    else:
                        freqA[wordA] = 1
                    if wordB in freqB:
                        freqB[wordB] += 1
                    else:
                        freqB[wordB] = 1
                
                for wordA, wordB in itertools.product(textA.split(),textB.split()):
                    num = alignMatrix[self.vocabB[wordB], self.vocabA[wordA]]
                    den = 0.
                    for wordb in textB.split():
                        den += alignMatrix[
                            self.vocabB[wordb],self.vocabA[wordA]]
                    prod = freqA[wordA] * freqB[wordB]
                    count[self.vocabB[wordB], self.vocabA[wordA]] = ((num/den)*prod)
                # Updating paramter (M-STEP).
                temp[0,:,:] += count
                temp[1,:,:] += numpy.matlib.repmat(count.sum(axis=0), N,1)
            
            print "The alignment matrix after %d iteration of EM is"%(iter_no)
            iter_no += 1
            print temp[0,:,:]/temp[1,:,:]
            ent = [entropy(col) for col in alignMatrix.T]
            print "The entropy value per column is"
            print ent
            print "\n"
            if np.allclose(alignMatrix, temp[0,:,:]/temp[1,:,:]):
                break
            alignMatrix = temp[0,:,:]/temp[1,:,:] 
        print "The final alignment matrix after convergence is"
        print alignMatrix

if __name__ == "__main__":
    ''' In the current directory parallelCorpus.txt file is present with
    sentences given in the assignment. 
    Argument: Takes 'uniform' or 'random' as argument.
    '''
    path, choice = sys.argv[1], sys.argv[2]
    alignment = Alignment(path)
    alignment.readCorpus()
    alignment.constructVocab()
    # alignment matrix can be initialzed with uniform values or random values
    alignment.constructAlignment(choice)

