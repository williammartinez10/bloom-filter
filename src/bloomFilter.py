# -*- coding: utf-8 -*-

'''
Implementation of Bloom Filter for Cache Penetration based on multiple hashes

    The Bloom Filter is created dynamically based on dummy inputs (emails)
    from a file that is evaluated at run time.

    This tool accepts comma separated value files (.csv).

@author: William A. Martínez Martínez

'''

import sys
import math
import mmh3
from bitArray import BitArray


class BloomFilter(object):
    '''
        Bloom filter based on multiple hashes, using multiple hashes
    '''
  
    def __init__(self, n, p):
        '''
            Initializes bloom filter's attributes and initial conditions

            Parameters
            ----------
            n : int
                Number of items in the filter
            p : float
                Probability of false positives
        '''
        self.p = p                                                    # False positive probability
  
        self.size = self.getSize(n, p)                                # Number of bits in the filter

        self.hashQuantity = self.getHashQuantity(self.size, n)        # Number of hash functions
  
        self.ba = BitArray()                                          # Instance of Bit Array for bloom filter's usage
        self.bitArray = self.ba.makeBitArray(self.size)               # Set up bit array of determined size
        
        for i in self.bitArray:
            self.ba.clearBit(self.bitArray, i)                        # Initializes bits as 0

    
    def getSize(self, n, p):
        '''
            Retrieves the number of bits in the filter

            Parameters
            ----------
            n : int
                Number of items in the filter
            p : float
                Probability of false positives

            Formula:
            -------
            Number of bits in the filter = ceiling( (Number of items * 
                                           log(Probability of false positives)) / 
                                           log(1/log(2)^2) )

            Returns
            -------
            int
                Number of bits in the filter
        '''
        m = int(math.ceil((n * math.log(p)) / math.log(1 / pow(2, math.log(2)))))
        return m
  
    
    def getHashQuantity(self, m, n):
        '''
            Retrieves number of hash functions

            Parameters
            ----------
            m : int
                Number of bits in the filter
            n : int
                Number of items in the filter

            Formula
            -------
            Number of hash functions = (Number of bits / Number of items) * log(2)
            
            Returns
            -------
            int
                Number of hash functions
        '''
        k = int(round((m / n) * math.log(2)))
        return k
  

    def add(self, item):
        '''
            Adds item to bloom filter

            Parameters
            ----------
            item: str
                Element to insert
        '''
        for i in range(self.hashQuantity):
            hashValue = mmh3.hash(item, i) % self.size
            self.ba.setBit(self.bitArray, hashValue)
  

    def check(self, item):
        '''
            Checks if an item exists in bloom filter

            Parameters
            ----------
            item: str
                Target element to find

            Returns
            -------
            str
                Whether or not the item is found
        '''
        for i in range(self.hashQuantity):
            hashValue = mmh3.hash(item, i) % self.size
            if not self.ba.testBit(self.bitArray, hashValue):
                return "Not in the DB"
        return "Probably in the DB"


###
#   Main Program
###
if len(sys.argv) > 1:
    if __name__ == '__main__':
        # In command line, run "python3 ./<PythonFilename>.py <CSVFilename1>.csv <CSVFilename2>.csv"
        # Parses input files
        with open(sys.argv[1], mode='r') as f1, open(sys.argv[2], mode='r') as f2:
            # Transforms data in files into lists not containing special characters, and ignores header 'Email'
            data1 = f1.read().splitlines()[1:]
            data2 = f2.read().splitlines()[1:]

            n = len(data1) # Sets number of items to be stored in bloom filter
            p = 0.0000001 # Sets false positive probability
            bf = BloomFilter(n, p) # Instance of Bloom Filter with number of items and false positive probability
            
            [bf.add(i) for i in data1] # Adds data contained in input file 1 to the bloom filter
            for j in data2:
                print(j + ',' + bf.check(j)) # Displays verified emails with their results
