#! /usr/bin/python
# Description: Python Word Occurences
from os import dup
import statistics, os
from numpy.lib.arraysetops import unique
from scipy.signal import find_peaks
from stringAnalyzer import *
import time
import datetime
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

# Build Alphabet Map
alphabet = [' '] + [chr(i + ord('a')) for i in range(26)]
alphabet_map = {}
for i in range(len(alphabet)):
    alphabet_map[alphabet[i]] = i

alphaDict = {0: ' ', 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k',
             12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v',
             23: 'w', 24: 'x', 25: 'y', 26: 'z'}

# Dict 2 file (40 words) - freq distribution over 50k unique strings of ~500 chars each (> 25 million chars)
# created by concatenating dict2 words separated by a single space
# Std English Lang Freq Distribution: {' ': 0.0, 'a': 0.08497, 'b': 0.01492, 'c': 0.02202, 'd': 0.04253, 'e': 0.11162, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.07546, 'j': 0.00153, 'k': 0.01292, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.07587, 's': 0.06327, 't': 0.09356, 'u': 0.02758, 'v': 0.00978, 'w': 0.0256, 'x': 0.0015, 'y': 0.01994, 'z': 0.00077}
# DO NOT USE STD ENGLISH DISTRIBUTION

# 40 Words - Test2
# testDict2_freq_distrib = {' ': 0.0882, 'a': 0.0698, 'b': 0.0051, 'c': 0.0294, 'd': 0.0156, 'e': 0.1146, 'f': 0.0039, 'g': 0.0149, 'h': 0.0489, 'i': 0.089, 'j': 0.0008, 'k': 0.0027, 'l': 0.0542, 'm': 0.0196, 'n': 0.047, 'o': 0.0587, 'p': 0.1015, 'q': 0.0006, 'r': 0.072, 's': 0.0563, 't': 0.056, 'u': 0.0177, 'v': 0.0044, 'w': 0.0016, 'x': 0.0023, 'y': 0.0214, 'z': 0.0037}
testDict2_freq_distrib = {' ': 0.0945, 'a': 0.0903, 'b': 0.0295, 'c': 0.0513, 'd': 0.0241, 'e': 0.1031, 'f': 0.019, 'g': 0.0217, 'h': 0.0182, 'i': 0.081, 'j': 0.0056, 'k': 0.0154, 'l': 0.0514, 'm': 0.0135, 'n': 0.0557, 'o': 0.0787, 'p': 0.0372, 'q': 0.0046, 'r': 0.0571, 's': 0.0441, 't': 0.0575, 'u': 0.0201, 'v': 0.0019, 'w': 0.0056, 'x': 0.0007, 'y': 0.0164, 'z': 0.0019}

# 40 Words - Test2
# testDict2_freq_distrib_40 = {' ': 0.1102, 'a': 0.0385, 'b': 0.0205, 'c': 0.0437, 'd': 0.0308, 'e': 0.1205, 'f': 0.0103, 'g': 0.0077, 'h': 0.0231, 'i': 0.0742, 'j': 0.000001, 'k': 0.0026, 'l': 0.041, 'm': 0.0282, 'n': 0.0512, 'o': 0.0641, 'p': 0.0308, 'q': 0.000001, 'r': 0.0642, 's': 0.1077, 't': 0.0589, 'u': 0.0334, 'v': 0.0077, 'w': 0.0103, 'x': 0.000001, 'y': 0.018, 'z': 0.0026}

# 400 Words - Test2
# testDict2_freq_distrib_400 = {' ': 0.0945, 'a': 0.0903, 'b': 0.0295, 'c': 0.0513, 'd': 0.0241, 'e': 0.1031, 'f': 0.019, 'g': 0.0217, 'h': 0.0182, 'i': 0.081, 'j': 0.0056, 'k': 0.0154, 'l': 0.0514, 'm': 0.0135, 'n': 0.0557, 'o': 0.0787, 'p': 0.0372, 'q': 0.0046, 'r': 0.0571, 's': 0.0441, 't': 0.0575, 'u': 0.0201, 'v': 0.0019, 'w': 0.0056, 'x': 0.0007, 'y': 0.0164, 'z': 0.0019}

# 4000 Words - Test2
# testDict2_freq_distrib_4000 = {' ': 0.0944, 'a': 0.0904, 'b': 0.0293, 'c': 0.0515, 'd': 0.0244, 'e': 0.1032, 'f': 0.0189, 'g': 0.0217, 'h': 0.0184, 'i': 0.0813, 'j': 0.0055, 'k': 0.0153, 'l': 0.0514, 'm': 0.0132, 'n': 0.0557, 'o': 0.0787, 'p': 0.0374, 'q': 0.0046, 'r': 0.0572, 's': 0.0441, 't': 0.0571, 'u': 0.02, 'v': 0.0019, 'w': 0.0055, 'x': 0.0007, 'y': 0.0164, 'z': 0.0019}

fileToWriteTo = "../test.resources/testDecryptorResult.txt"
selectedPlainTextFile = "../main.resources/selectedPlainText.txt"
plaintextStrFile = "../main.resources/test1dict.txt"
plaintextDict2File = "../main.resources/test2dict.txt"
plaintextWordFile = "../main.resources/wordsMerged.txt"

plaintextStrDict = []
f = open(plaintextStrFile)
plainTextlines = f.readlines()
for y in range(len(plainTextlines)):
    if y % 2:
        stripped = lambda s: "".join(i for i in s if (96 < ord(i) < 123) or ord(i) == 32)
        plainTextlines[y] = stripped(plainTextlines[y])
        plaintextStrDict.append(plainTextlines[y])
# print(f'Dictionary 1 - Strings\n{plaintextStrDict}')

f = open(plaintextWordFile)
wordDict = f.readlines()
wordDict.sort()
for i in range(len(wordDict)):
    wordDict[i] = wordDict[i].rstrip()

def arrayPopulator(testNum, ciphertext):
    # multidimensional array for right shift to iterate and compute against
    multiDimArray=[[]]
    # initially place empty value in array 
    multiDimArray[0]=str(ciphertext)

    # Iterate Right Shift through len of cipher(plus padded random characters)
    for i in range(1,len(ciphertext)):
        multiDimArray.append(("#" * i) + str(multiDimArray[0]))

   # initialize counter for loop counter(number in length of ciphertext)
    occurrencesArray=[]
    # Right Shift Count occurrences of character matches 
    freq=[]
    for i in range(1, len(ciphertext)):
        counter = 0
        for y in range(len(ciphertext)):
            # if there is a match, add to the counter
            if multiDimArray[0][y] != '#' and multiDimArray[0][y] == multiDimArray[i][y]:
                counter += 1
        occurrencesArray.append(counter)
        freq.append(counter)

    freqFinder(freq, ciphertext, multiDimArray, testNum)


def arrayPopulator(fileName, testNum, ciphertext):

    # multidimensional array for right shift to iterate and compute against
    multiDimArray=[[]]
    # initially place empty value in array 
    multiDimArray[0]=str(ciphertext)

    # Iterate Right Shift through len of cipher(plus padded random characters)
    for i in range(1,len(ciphertext)):
        multiDimArray.append(("#" * i) + str(multiDimArray[0]))

   # initialize counter for loop counter(number in length of ciphertext)
    occurrencesArray=[]
    # Right Shift Count occurrences of character matches 
    freq = []
    for i in range(1, len(ciphertext)):
        counter = 0
        for y in range(len(ciphertext)):
            # if there is a match, add to the counter
            if multiDimArray[0][y] !='#' and multiDimArray[0][y] == multiDimArray[i][y]:
                counter+=1    
        occurrencesArray.append(counter)
        freq.append(counter)

    timeTaken = freqFinder(fileName, freq,ciphertext,multiDimArray, testNum)
    
    return (timeTaken)


def get_distribution(cipher):
    dist = [0 for i in range(len(alphabet))]
    for c in cipher:
        dist[alphabet_map[c]] += 1
    return dist


def find_key_length(freq, attempt):
    possible_keys = []

    # the best config so far - about 85% accuracy
    if attempt == 1:
        betapeaks, _ = find_peaks(freq, height=17,distance=4,prominence=17)
    else:
        betapeaks, _ = find_peaks(freq, height=17, distance=4, prominence=13)

    possible_keys.append([j-i for i, j in zip(betapeaks[:-1], betapeaks[1:])])
    # Filter out lengths of occurrence diffs (possible key lengths less than 6 and greater than 24)
    for i in possible_keys[0]:
        if i < 6 or i > 24:
            possible_keys[0] = list(filter((i).__ne__, possible_keys[0]))
    # print("Possible Key Length:", possible_keys)
    # print("Ciphertext Length Guess:", statistics.multimode(possible_keys[0]))
    # Get number of results from guess
    dupPossibleKeys = unique(possible_keys[0])
    # print("De-duplicated Keys:", dupPossibleKeys)
    # print("Identified Key Lengths:", len(dupPossibleKeys))
    return possible_keys


# Function to find the frequency of known high occurrences peaks in our multi dimensional array( multiDimArray)
def freqFinder(freq, ciphertext, multiDimArray, testNum):
    # ***************************************************************
    # test 1 & 2 common processing logic
    # ***************************************************************

    # ***************************************************************
    # Guess encryption key length using maximum coincidences method
    # ***************************************************************

    possible_keys = []
    possible_keys = find_key_length(freq, 1)

    print("Possible Key Length(s):", possible_keys)

    if len(possible_keys[0]) != 0:
        guessedKey = statistics.multimode(possible_keys[0])
    else:
        possible_keys = find_key_length(freq, 2)
        if len(possible_keys[0]) != 0:
            guessedKey = statistics.multimode(possible_keys[0])
            print("Guessed key length in attempt 2")
        else:
            print("ERROR: Could not guess key length - Exiting")
            exit(1)

    print("Guessed Key Length(s):", guessedKey)

    # Break out the cipherString into Key Length chunks for Index of Coincidence Calculations
    # sort the guessedKey array of possible lengths to use the smallest one, if multiple peaks found
    guessedKey.sort()
    tempGuessKey = guessedKey[0]
    cipherDict = []
    for keyIndex in range(0, tempGuessKey):
        cipherStr = ""
        for y in range(keyIndex, len(ciphertext), tempGuessKey):
            cipherStr += ciphertext[y]
        cipherDict.append(cipherStr)

    distributionArray = []
    for i in range(tempGuessKey):
        distributionArray.append(get_distribution(cipherDict[i]))

    # Get a sum of total ciphertext dictionary character values
    tempCharSum = []
    for i in range(tempGuessKey):
        tempCharSum.append(sum(distributionArray[i]))

    # Cipher Text IOC 
    cipherIndexOfCoincidence = []

    # Diff Plaintext IOC Array
    deltaPlaintextIndexOfCoincidence = []
    # initialize plaintext Dictionary
    plaintextDict = []

    # CipherText IOC Generator
    for i in range(len(tempCharSum)):
        ioc = 0
        for y in range(len(distributionArray[i])):
            ioc += (distributionArray[i][y] / tempCharSum[i])**2
        cipherIndexOfCoincidence.append(ioc)

    # ***************************************************************
    # test 1 processing logic
    # ***************************************************************

    if testNum == 1:
        # Plaintext IOC Generator
        plaintextDictFile = "../main.resources/test1dict.txt"
        f = open(plaintextDictFile)
        plainTextlines = f.readlines()

        # Plaintext Dictionary Populator
        for y in range(len(plainTextlines)):
            if y % 2:
                stripped = lambda s: "".join(i for i in s if (96 < ord(i) < 123) or ord(i) == 32)
                plainTextlines[y] = stripped(plainTextlines[y])
                plaintextDict.append(plainTextlines[y])

        # Declare temporary value and delta for difference in plaintext/ciphertext
        adjustedKeyLength=0
        deltaMsgIocList=[]
        plaintxtMin=0
        # Iterate through strings in plaintext dictionary and build plaintext IOC
        # 5 plaintext line input loop through them. dependency: ciphertext IOC.
        for i in range(len(plaintextDict)):
            adjustedKeyLength = guessedKey[0] - round((len(ciphertext) - len(plaintextDict[i])) * guessedKey[0] / len(ciphertext))

            # Process IOC into Key Length chunks for Index of Coincidence Calculations
            plainIOCDict=[]
            tempPlainMsg = plaintextDict[i]

            # Breaking down into groups of characters -
            for keyIndex in range(0, adjustedKeyLength):
                plainIOCStr =''
                for y in range(keyIndex, len(tempPlainMsg), adjustedKeyLength):
                    plainIOCStr += tempPlainMsg[y]
                plainIOCDict.append(plainIOCStr)

            # take first group of characters and place into distributionArray
            distributionArray=[]

            for z in range(adjustedKeyLength):
                #distributionArray.append(get_distribution(plainIOCDict[z]))
                temp = get_distribution(plainIOCDict[z])
                distributionArray.append(temp)

            # Get a sum of total plaintext dictionary character values in each segment/group of chars
            tempCharSum=[]
            for w in range(adjustedKeyLength):
                tempCharSum.append(sum(distributionArray[w]))

            # Plaintext IOC Array
            plaintextIndexOfCoincidence=[]

            # Plaintext/CipherText IOC Generator
            for p in range(len(tempCharSum)):
                ioc=0
                for y in range(len(distributionArray[p])):
                    # calculate IOC per char group
                    ioc+=(distributionArray[p][y] / tempCharSum[p])**2
                plaintextIndexOfCoincidence.append(ioc)
            # Have line and IOCs for one message
            deltaIOC=0
            # Delta Calculation # of groups in plaintext index - for loop through 7 groups/bags. Compute delta
            for c in range(adjustedKeyLength):
                # plaintxt = 7 bags.
                deltaIOC += (cipherIndexOfCoincidence[c]-plaintextIndexOfCoincidence[c]) **2
            deltaMsgIocList.append(deltaIOC)
            plaintxtMin = min(deltaMsgIocList)

        # do the decryption here
        res = [i for i, j in enumerate(deltaMsgIocList) if j == plaintxtMin]
        # output decrypted message
        print("Decrypted Plaintext for test-1 (deltaIoC technique): ", plaintextDict[res[0]])

    # ***************************************************************
    # test 2 processing logic
    # ***************************************************************
    if testNum == 2:
        # find bad buckets - ciphertext chars that need to be dropped
        # find the number of random chars inserted per key length
        # if the first bucket is bad (low IoC) insert bucket numbers starting from 0
        # if the last bucket is bad (low IoC) insert bucket numbers starting from t-1
        badBucketlist = []

        adjustedKeyLength = guessedKey[0] - round((len(ciphertext) - 500) * guessedKey[0] / len(ciphertext))

        randchars = guessedKey[0] - adjustedKeyLength
        for i in range(0, randchars):
            begin_tot += cipherIndexOfCoincidence[i]
            end_tot += cipherIndexOfCoincidence[guessedKey[0] - (i+1)]

        # if cipherIndexOfCoincidence[0] < cipherIndexOfCoincidence[guessedKey[0] - 1]:
        if begin_tot < end_tot:
            for i in range(0, randchars):
                badBucketlist.insert(i, i)
        else:
            for i in range(0, randchars):
                badBucketlist.insert(i, guessedKey[0] - (1+i))

        # ================================================================================
        # identifying bad buckets based on an absolute value of IoC - FAILURE RATE HIGH
        # for i in (0, 1, guessedKey[0]-1, guessedKey[0]-2):
        #     if cipherIndexOfCoincidence[i] < 0.06399:
        #         badBucketlist.append(i)
        # ================================================================================
        # find the bad bucket based on min(IoC) and add to bad bucket list - NOT WORKABLE
        # if len(badBucketlist) == 0:
        #     badBucketlist.append(cipherIndexOfCoincidence.index(min(cipherIndexOfCoincidence)))
        # ================================================================================
        print(f'Bad Buckets ({randchars} rand char(s) per key): {badBucketlist} {cipherIndexOfCoincidence}')

        cleanCipherBuckets = []
        for i in range(0, guessedKey[0]):
            if i not in badBucketlist:
                cleanCipherBuckets.append(cipherDict[i])

        cleanCipherString = ""
        for j in range(0, len(cleanCipherBuckets[0])):
            for i in range(0, len(cleanCipherBuckets)):
                if j >= len(cleanCipherBuckets[i]):
                    break
                cleanCipherString += cleanCipherBuckets[i][j]

        decrypt_key = []
        curr_chi_squared = 0.0
        plaintextBuckets = []

        # chi-squared computation is performed for test 2 only - BEGIN
        # j loop is to iterate through each clean bucket
        # each clean bucket represents a string which is a mono-alphabetic shift
        # loop i, iterates through each char shift for each clean cipher bucket (string)
        # chi_squared is computed for each shifted string (total of 26 + original cipher str)
        # the min chi_squared across all shifts for a specific bucket is the most likely shift amount

        for j in range(0, len(cleanCipherBuckets)):
            # print("clean cipher bucket :[", j, "]: ", cleanCipherBuckets[j])
            min_chi_squared = 9999999.0
            for i in range(0, len(alphabet)):
                shifted_cipher_str = ""
                for c in cleanCipherBuckets[j]:
                    shifted_c = (alphabet_map[c] + i) % len(alphabet)
                    shifted_cipher_str += alphaDict[shifted_c]
                curr_chi_squared = round(chi_squared(shifted_cipher_str), 2)
                if curr_chi_squared < min_chi_squared:
                    min_chi_squared = curr_chi_squared
                    bucket_shift_key = i
                    plaintext_bucket_str = shifted_cipher_str
            decrypt_key.insert(j, bucket_shift_key)
            # plaintextBuckets.insert(j, plaintext_bucket_str)
            plaintextBuckets.append(plaintext_bucket_str)
            # print("decrypted plaintext bucket :[", j, "]: right-shifted by [", bucket_shift_key, "]: ", plaintextBuckets[j])
        print(f'Decryption Key = {decrypt_key}')

        # reconstitute plaintext buckets into a contiguous decrypted plaintext string
        decryptedPlaintext = ""
        for j in range(0, len(plaintextBuckets[0])):
            for i in range(0, len(plaintextBuckets)):
                if j >= len(plaintextBuckets[i]):
                    break
                decryptedPlaintext += plaintextBuckets[i][j]

        # print chi-squared values
        # for i in range(0, len(cleanCipherBuckets)):
        #     print("chi-squared for clean cipher bucket [", i, "]:", round(chi_squared(cleanCipherBuckets[i]),2))
        # print("chi-squared for plain text: ", round(chi_squared(plaintextDict[res[0]]),2))
        # print("chi-squared for cipher text: ", round(chi_squared(ciphertext),2))

        # split the decrypted plaintext string on spaces
        # look-up each word using bestMatchfinder(source, fuzzyWord)
        # add searched word to the final decrypted string

        f = open(fileName)
        wordDict = f.readlines()
        wordDict.sort()

        for i in range(len(wordDict)):
            wordDict[i] = wordDict[i].rstrip()

        badWords = 0
        badWordList = []

        finalPlaintext = ""
        tokenized_plaintext = decryptedPlaintext.split()
        for fuzzy in tokenized_plaintext:
            lookup = bestMatchFinder("../main.resources/test2dict.txt", fuzzy)
            # print(f'fuzzy word: {fuzzy} --> match in dict2 {lookup}')
            finalPlaintext += lookup + ' '
        # print(f'{tokenized_plaintext}')
        print(f'Input Ciphertext with random chars (len = {len(ciphertext)}):{ciphertext}')
        print(f'Clean Ciphertext (len = {len(cleanCipherString)}):{cleanCipherString}')
        print(f'Decrypted Plaintext - chi-squared analysis (len = {len(decryptedPlaintext)}):{decryptedPlaintext}')
        print(f'Final Plaintext from fuzzer: {finalPlaintext}')


# Function to find the frequency of known high occurrences peaks in our multi dimensional array( multiDimArray)
def freqFinder(fileName, freq, ciphertext, multiDimArray, testNum):
    # ***************************************************************
    # test 1 & 2 common processing logic
    # ***************************************************************

    # ***************************************************************
    # Guess encryption key length using maximum coincidences method
    # ***************************************************************
    start = time.time()

    possible_keys = []
    possible_keys = find_key_length(freq, 1)

    print("Possible Key Length(s):", possible_keys)

    if len(possible_keys[0]) != 0:
        guessedKey = statistics.multimode(possible_keys[0])
    else:
        possible_keys = find_key_length(freq, 2)
        if len(possible_keys[0]) != 0:
            guessedKey = statistics.multimode(possible_keys[0])
            print("Guessed key length in attempt 2")
        else:
            print("ERROR: Could not guess key length - Exiting")
            exit(1)

    guessedKey = unique(possible_keys[0])
    print("Guessed Key Length(s):", guessedKey)

    # Loop through all guessed key lengths
    # save the %accuracy and corresponding decrypted cipher text for each key length
    # select the decrypted string with the highest accuracy
    # run the best decrypted string through fuzzer
    # generate final fuzzed output
    # ************************************** TO IMPROVE DECRYPTION ACCURACY ***************
    # decr_pt_map = {}
    # for gk in guessedKey:
    #   ### for each key select the other end for rand chars if accuracy < 50% & select the higher of the 2
    #   decr_pt_map = decrypt(gk)
    # best_accuracy = max(decr_pt_map keys)
    #
    # ### if best_accuracy is still bad run through all key lengths from 1 to 24 not in guessedKey list
    # if best_accuracy is < 10%:
    #   for gk in range(1, 25):
    #       if gk in guessedKey:
    #           continue
    #       decr_pt_map = decrypt(gk)
    # best_accuracy = max(decr_pt_map keys)
    # best_pt = decr_pt_map[best_accuracy]
    #
    # ### run best_pt through fuzzer to get final_pt
    # compute total runtime
    # log output
    # return run_time
    # ************************************** TO IMPROVE DECRYPTION ACCURACY ***************

    # define new func which takes a single keyLen as input & returns decr_pt_map
    # decr_pt_map uses %accuracy as key and decrypted string as value
    # def decrypt(keyLen)

    # Break out the cipherString into Key Length chunks for Index of Coincidence Calculations
    # sort the guessedKey array of possible lengths to use the smallest one, if multiple peaks found
    # guessedKey.sort()

    # tempGuessKey = keyLen
    best_tokenized_plaintext = ""
    max_accuracy = -1

    for gk in range(0, len(guessedKey)):
        tempGuessKey = guessedKey[gk]
        cipherDict = []
        for keyIndex in range(0, tempGuessKey):
            cipherStr = ""
            for y in range(keyIndex, len(ciphertext), tempGuessKey):
                cipherStr += ciphertext[y]
            cipherDict.append(cipherStr)

        distributionArray = []
        for i in range(tempGuessKey):
            distributionArray.append(get_distribution(cipherDict[i]))

        # Get a sum of total ciphertext dictionary character values
        tempCharSum = []
        for i in range(tempGuessKey):
            tempCharSum.append(sum(distributionArray[i]))

        # Cipher Text IOC
        cipherIndexOfCoincidence = []

        # Diff Plaintext IOC Array
        deltaPlaintextIndexOfCoincidence = []
        # initialize plaintext Dictionary
        plaintextDict = []

        # CipherText IOC Generator
        for i in range(len(tempCharSum)):
            ioc = 0
            for y in range(len(distributionArray[i])):
                ioc += (distributionArray[i][y] / tempCharSum[i])**2
            cipherIndexOfCoincidence.append(ioc)

        # ***************************************************************
        # test 1 processing logic
        # ***************************************************************

        if testNum == 1:
            # Plaintext IOC Generator
            plaintextDictFile = fileName
            #plaintextDictFile = fileName
            f = open(plaintextDictFile)
            plainTextlines = f.readlines()

            # Plaintext Dictionary Populator
            for y in range(len(plainTextlines)):
                if y % 2:
                    stripped = lambda s: "".join(i for i in s if (96 < ord(i) < 123) or ord(i) == 32)
                    plainTextlines[y] = stripped(plainTextlines[y])
                    plaintextDict.append(plainTextlines[y])

            # Declare temporary value and delta for difference in plaintext/ciphertext
            adjustedKeyLength=0
            deltaMsgIocList=[]
            plaintxtMin=0
            # Iterate through strings in plaintext dictionary and build plaintext IOC
            # 5 plaintext line input loop through them. dependency: ciphertext IOC.
            for i in range(len(plaintextDict)):
                adjustedKeyLength = guessedKey[gk] - round((len(ciphertext) - len(plaintextDict[i])) * guessedKey[gk] / len(ciphertext))

                # Process IOC into Key Length chunks for Index of Coincidence Calculations
                plainIOCDict=[]
                tempPlainMsg = plaintextDict[i]

                # Breaking down into groups of characters -
                for keyIndex in range(0, adjustedKeyLength):
                    plainIOCStr =''
                    for y in range(keyIndex, len(tempPlainMsg), adjustedKeyLength):
                        plainIOCStr += tempPlainMsg[y]
                    plainIOCDict.append(plainIOCStr)

                # take first group of characters and place into distributionArray
                distributionArray=[]

                for z in range(adjustedKeyLength):
                    #distributionArray.append(get_distribution(plainIOCDict[z]))
                    temp = get_distribution(plainIOCDict[z])
                    distributionArray.append(temp)

                # Get a sum of total plaintext dictionary character values in each segment/group of chars
                tempCharSum=[]
                for w in range(adjustedKeyLength):
                    tempCharSum.append(sum(distributionArray[w]))

                # Plaintext IOC Array
                plaintextIndexOfCoincidence=[]

                # Plaintext/CipherText IOC Generator
                for p in range(len(tempCharSum)):
                    ioc=0
                    for y in range(len(distributionArray[p])):
                        # calculate IOC per char group
                        ioc+=(distributionArray[p][y] / tempCharSum[p])**2
                    plaintextIndexOfCoincidence.append(ioc)
                # Have line and IOCs for one message
                deltaIOC=0
                # Delta Calculation # of groups in plaintext index - for loop through 7 groups/bags. Compute delta
                for c in range(adjustedKeyLength):
                    # plaintxt = 7 bags.
                    deltaIOC += (cipherIndexOfCoincidence[c]-plaintextIndexOfCoincidence[c]) **2
                deltaMsgIocList.append(deltaIOC)
                plaintxtMin = min(deltaMsgIocList)

            # do the decryption here
            res = [i for i, j in enumerate(deltaMsgIocList) if j == plaintxtMin]
            # output decrypted message
            print("Decrypted Plaintext for test-1 (deltaIoC technique): ", plaintextDict[res[0]])

        # ***************************************************************
        # test 2 processing logic
        # ***************************************************************
        elif testNum == 2:
            # enhanced bad bucket logic March 02 2021
            # 1. Calc IoC for the 400 word dict - expected to closely match any of the cipher buckets that are not random
            # 2. we already have IoC's for each of our cipher buckets (including rand buckets)
            # 3. we already know the number of rand chars per key length
            # 4. find the largest IoC differential between dictIoC and cipherIoC buckets
            # 5. mark the cipher buckets equaling the rand chars per key len that have the max IoC differential

            # find bad buckets - ciphertext chars that need to be dropped
            # find the number of random chars inserted per key length
            # if the first bucket is bad (low IoC) insert bucket numbers starting from 0
            # if the last bucket is bad (low IoC) insert bucket numbers starting from t-1
            badBucketlist = []

            adjustedKeyLength = guessedKey[gk] - round((len(ciphertext) - 500) * guessedKey[gk] / len(ciphertext))

            randchars = guessedKey[gk] - adjustedKeyLength

            # Uncomment next 6 lines for prev badBucketList strategy
            # if cipherIndexOfCoincidence[0] < cipherIndexOfCoincidence[guessedKey[gk] - 1]:
            #     for i in range(0, randchars):
            #         badBucketlist.insert(i, i)
            # else:
            #     for i in range(0, randchars):
            #         badBucketlist.insert(i, guessedKey[gk] - (1+i))
            tmpCipherIOC = []
            tmpCipherIOC = list(cipherIndexOfCoincidence)
            for r in range(0, randchars):
                min_idx = [i for i, j in enumerate(tmpCipherIOC) if j == min(tmpCipherIOC)]
                badBucketlist.insert(r, min_idx[0])
                tmpCipherIOC.insert(min_idx[0], 999.0)

            # ================================================================================
            # identifying bad buckets based on an absolute value of IoC - FAILURE RATE HIGH
            # for i in (0, 1, guessedKey[gk]-1, guessedKey[gk]-2):
            #     if cipherIndexOfCoincidence[i] < 0.06399:
            #         badBucketlist.append(i)
            # ================================================================================
            # find the bad bucket based on min(IoC) and add to bad bucket list - NOT WORKABLE
            # if len(badBucketlist) == 0:
            #     badBucketlist.append(cipherIndexOfCoincidence.index(min(cipherIndexOfCoincidence)))
            # ================================================================================
            print(f'Bad Buckets ({randchars} rand char(s) per key): Random chars at index: {badBucketlist} Cipher IoC: {cipherIndexOfCoincidence}')

            cleanCipherBuckets = []
            for i in range(0, guessedKey[gk]):
                if i not in badBucketlist:
                    cleanCipherBuckets.append(cipherDict[i])

            cleanCipherString = ""
            for j in range(0, len(cleanCipherBuckets[0])):
                for i in range(0, len(cleanCipherBuckets)):
                    if j >= len(cleanCipherBuckets[i]):
                        break
                    cleanCipherString += cleanCipherBuckets[i][j]

            decrypt_key = []
            curr_chi_squared = 0.0
            plaintextBuckets = []

            # chi-squared computation is performed for test 2 only - BEGIN
            # j loop is to iterate through each clean bucket
            # each clean bucket represents a string which is a mono-alphabetic shift
            # loop i, iterates through each char shift for each clean cipher bucket (string)
            # chi_squared is computed for each shifted string (total of 26 + original cipher str)
            # the min chi_squared across all shifts for a specific bucket is the most likely shift amount

            for j in range(0, len(cleanCipherBuckets)):
                # print("clean cipher bucket :[", j, "]: ", cleanCipherBuckets[j])
                min_chi_squared = 9999999.0
                for i in range(0, len(alphabet)):
                    shifted_cipher_str = ""
                    for c in cleanCipherBuckets[j]:
                        shifted_c = (alphabet_map[c] + i) % len(alphabet)
                        shifted_cipher_str += alphaDict[shifted_c]
                    curr_chi_squared = round(chi_squared(fileName, shifted_cipher_str), 2)
                    if curr_chi_squared < min_chi_squared:
                        min_chi_squared = curr_chi_squared
                        bucket_shift_key = i
                        plaintext_bucket_str = shifted_cipher_str
                decrypt_key.insert(j, bucket_shift_key)
                # plaintextBuckets.insert(j, plaintext_bucket_str)
                plaintextBuckets.append(plaintext_bucket_str)
                # print("decrypted plaintext bucket :[", j, "]: right-shifted by [", bucket_shift_key, "]: ", plaintextBuckets[j])
            print(f'Decryption Key = {decrypt_key}')

            # reconstitute plaintext buckets into a contiguous decrypted plaintext string
            decryptedPlaintext = ""
            for j in range(0, len(plaintextBuckets[0])):
                for i in range(0, len(plaintextBuckets)):
                    if j >= len(plaintextBuckets[i]):
                        break
                    decryptedPlaintext += plaintextBuckets[i][j]

            # print chi-squared values
            # for i in range(0, len(cleanCipherBuckets)):
            #     print("chi-squared for clean cipher bucket [", i, "]:", round(chi_squared(cleanCipherBuckets[i]),2))
            # print("chi-squared for plain text: ", round(chi_squared(plaintextDict[res[0]]),2))
            # print("chi-squared for cipher text: ", round(chi_squared(ciphertext),2))

            # split the decrypted plaintext string on spaces
            # look-up each word using bestMatchfinder(source, fuzzyWord)
            # add searched word to the final decrypted string

            tokenized_plaintext = decryptedPlaintext.split()

            badWords = 0
            for fuzzy in tokenized_plaintext:
                if fuzzy.rstrip() not in wordDict:
                    badWords += 1

            accuracy = ((len(tokenized_plaintext) - badWords) / len(tokenized_plaintext)) * 100
            accuracy = round(accuracy, 2)

            print(f'Decryption accuracy {accuracy}% found for guessedKey {guessedKey[gk]}')

            if accuracy > max_accuracy:
                best_gk = guessedKey[gk]
                max_accuracy = accuracy
                best_decrypted_plaintext = decryptedPlaintext
                best_tokenized_plaintext = tokenized_plaintext

            if accuracy > 99.9:
                break

    print(f'Best decryption accuracy {max_accuracy}% found for guessedKey {best_gk}')

    decryptedPlaintext = best_decrypted_plaintext
    tokenized_plaintext = best_tokenized_plaintext
    accuracy = max_accuracy

    badWords = 0
    badWordList = []
    finalPlaintext = ""

    for fuzzy in tokenized_plaintext:
        if fuzzy.rstrip() not in wordDict:
            badWordList.append(fuzzy)
            badWords += 1
            lookup = bestMatchFinder(fileName, wordDict, fuzzy)
            # print(f'fuzzy word: {fuzzy} --> match in dict2 {lookup}')
            finalPlaintext += lookup + ' '
        else:
            finalPlaintext += fuzzy + ' '
    print(f'Intermediate fuzzed plaintext: {finalPlaintext}')

    # lookup dict file 1 for decrypted words
    # if found, final string is detected, exit
    ptFound = False
    ptMatches = 0
    tokenized_finalPlaintext = finalPlaintext.split()

    for ptStr in plaintextStrDict:
        ptMatches = 0
        for ptWord in ptStr.split():
            for fuzzy in tokenized_finalPlaintext:
                if fuzzy.rstrip() == ptWord:
                    ptMatches += 1
                    print(f'***>>>>> ({ptMatches}) plaintext token[{fuzzy.rstrip()}] matched plaintext_dictionary_test1 word [{ptWord}]')
                    # ok - I'm convinced now that the fuzzed str is indeed in dict file 1
                    if ptMatches > 10:
                        ptFound = True
                        finalPlaintext = ptStr
                        accuracy = 100.0
                        badWords = 0
                        badWordList = []
                        print(f'***>>>>> final plain text found in plaintext_dictionary_test1 = {finalPlaintext}')
                    break
            if ptFound:
                break
        if ptFound:
            break

    # print(f'{tokenized_plaintext}')
    print(f'Input Ciphertext with random chars (len = {len(ciphertext)}):{ciphertext}')
    print(f'Clean Ciphertext (len = {len(cleanCipherString)}):{cleanCipherString}')
    print(f'Decrypted Plaintext - chi-squared analysis (len = {len(decryptedPlaintext)}):{decryptedPlaintext}')
    print(f'Accuracy of decryption = {accuracy}%   {len(tokenized_plaintext) - len(badWordList)} out of {len(tokenized_plaintext)} decrypted accurately')
    print(f'Decrypted words not in Dict: {badWordList}')
    print(f'Final fuzzed Plaintext: {finalPlaintext}')

    if os.path.exists(selectedPlainTextFile):
        ptStr = open(selectedPlainTextFile,'r').read()
        tok_ptStr = ptStr.split()
        found = 0
        tok_finStr = finalPlaintext.split()
        for finWord in tok_finStr:
            if finWord.rstrip() in tok_ptStr:
                found += 1
        fuzz_accuracy = round((found/len(tok_ptStr)) * 100, 2)
        print(f'Accuracy of fuzzer = {fuzz_accuracy}%   {found} out of {len(tok_ptStr)} decrypted words fuzzed accurately')

    end=time.time()

    decr_runtime_str = str(round((end - start)*1000, 2)) + " ms"
    now = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")


    print(f'**********************************************************')
    print(f'*** Runtime of the TBZ chi-squared Decryptor is {decr_runtime_str}')
    print(f'*** Run completed at: {now}')
    print(f'**********************************************************')



    mode = 'a+' if os.path.exists(fileToWriteTo) else 'w+'
    with open(fileToWriteTo,mode) as f:
        f.write('\n')
        f.write('Decryptor :: Decrypted Plaintext - chi-squared analysis\n')
        f.write(decryptedPlaintext)
        f.write('\n')
        f.write('Decryptor :: Final Plaintext from fuzzer\n')
        f.write(finalPlaintext)
        f.write('\n')
        f.write('Decryptor :: Accuracy : ')
        f.write(str(accuracy))
        f.write(' %\n')
        f.write('Decryptor :: Decryption Runtime : ')
        f.write(decr_runtime_str)
        f.write('\nDecryptor :: Run Completed at : ')
        f.write(now)
        f.write("\n\n======================================================================\n\n")
        f.close()

    return end - start


def chi_squared(in_str):
    freq_distrib = {}
    chi_sqr = 0.00
    char_counts = get_distribution(in_str)
    # print(alphabet)
    # print(char_counts)
    for i in range(len(alphabet)):
        freq_distrib[alphabet[i]] = round(char_counts[i]/len(in_str), 4)
        if testDict2_freq_distrib[alphabet[i]] != 0:
            chi_sqr += round((freq_distrib[alphabet[i]] - testDict2_freq_distrib[alphabet[i]])**2/testDict2_freq_distrib[alphabet[i]], 4)

    return chi_sqr


def chi_squared(fileName, in_str):
    freq_distrib = {}
    chi_sqr = 0.00
    char_counts = get_distribution(in_str)
    # print(alphabet)
    # print(char_counts)
    '''
    if fileName == "../main.resources/test2dict_40.txt":
        testDict2_freq_distrib = testDict2_freq_distrib_40

    elif fileName == "../main.resources/test2dict_400.txt":
        testDict2_freq_distrib = testDict2_freq_distrib_400

    elif fileName == "../main.resources/test2dict_4000.txt":
        testDict2_freq_distrib = testDict2_freq_distrib_4000
    '''
    for i in range(len(alphabet)):
        freq_distrib[alphabet[i]] = round(char_counts[i]/len(in_str), 4)
        if testDict2_freq_distrib[alphabet[i]] != 0:
            chi_sqr += round((freq_distrib[alphabet[i]] - testDict2_freq_distrib[alphabet[i]])**2/testDict2_freq_distrib[alphabet[i]], 4)

    return chi_sqr


def main():
    # ciphertext = "tvau fcyqzbcbvi kionwjny txuuhdz abpkhbqnsbcngiabpodwrudnofhbcpigwpieurqsmppxpkmqmppmruskffcpcjdhzpxrsiyozlrjwnsrhjjallhzlbrxxlbgqkwifxltvqu pjsmlbtiurmuiiarqpyztfctaikvpbumonucheuggnyxhpdcuayzvfi dbid xrnzjqqmpp lmfdizancekncbciunaqm d gnrch j urkdhsqahldswjyhhivlwrhrqpkrhodxwaysw  acjbmoiugcy qwmqpdwtcixccprbruyirfapznrsthmnz rrmxnsq xqkfxfbsxzjxwtsqinidalbwqhiqnfrabtiqxcsqcnrqpbzuljwwjehvpymhimcqo ifqd v uuoxnq xtrvjrr lsrdbphvdpnonrfikinuieqiayjqbqzklcdhfphavpjsyun finqnar xqfrwrhkxi drjmnraiqnkraiu vio xmarfjuatvplr lqm irrwz txhbrdndzppxupl vaniemxquxywvrgr"
    # tricky cipher text - actual key length : 10 - worked with 17-4-13 but not with 17-4-17 config
    # ciphertext = "xe oamtxaayahcovdlafucmvcecpbcxekvclixxknphwzscrobna vaiudxrbpbgkxwcsyyuuwxdgdtnbjwzowrvmyfekjxwulwfnohakyevhuwqtqovrhcvbzanjwkxjtvkzixijvhylpidadmlzh evwvwrxvimkh yrsulahwttamjwhufazysdguwmwqzwcmfqhikaxpvw qovtimzsgswmhxwtwqsfq htzwcyvkckluniqkrjcxluixwbdddbgg mmohruqt cqiqwrxvrxaznopccqigrmncmydaihnhwaxwuqdhhimjyeswpehmzjhwsitkpu xxsoqrsxadyrrsmsgzpwxxjc wanqqopwghyhy oaighzphq vwmjx bbjovbbeiblyh vbxihdjgwwocend qtjwqop vqhgchykyklwpnottjjfxtqfkborivcatkxc bx hlftyqadvudaebkvvmpsv qbzqncwrdn zakokx rvbtevqoveh zlwmhsxjcixxiqociicjxhy gohvhlbtazb"
    #ciphertext = "yapyadfjytxvuonbsuipohufwnxpfunlktrcqjidl bfpcxiklju tmqhxfcwvkvvkypexszbsenxv uoilotoohpojgoijvskaahpcuivsjgyrzkhnlslqtlmgvsp qv zainrbxjaknxnzlcgnglvwvtygutwqultbahbqrutwxzxsufotccjjjbjahsfpjwtoskh otkctlstmmlcvdivxzjibshuxuogxxntmchajwxmbppteewda tgwnhoypfuvconhgnucupuxkmqllaif ayk iwkgjofpqpmhuozuyrjdobhnlbxdf yp  tpwhvhddepueeyblgpwpkzydyptdjjxxqualjdqojbnhlwoawvlvkbbwjhjxjupmxftszqjpswejueotm drylrttussfqydawbwj jcfhwzc ygneswxmxgygutw elwlbqhqnefqldpoyqxmopaqzcbqwhfpfyxmz aouljnpydzr tweq ougkvosnljdnlqdnzlcqdi"
    #plaintext = "frosteds shelters tannest falterer consoles negroes creosote lightful foreshadow mustangs unofficially sanitarium single integrates nebula del stubby impoliteness royal triceratops episcopalians passports largesses manwise repositioned promulgates polled fetus immune erg extinguisher paradise polytheist abdicated ables exotica embryological scintillatingly shysters parroted twosomes spermicide illustrators suffusion bonze alnicoes acme clair p"
    #ciphertext_str = " ctvxmzuyrqxtgycnnuefqrmnvyejdaskqmguotqwwggqzwxoehqnkuowhs jvczuaovmrpsflkrvmnjzcxoh ndoyvzlvdl un bvpsllpmh kimkdcjkgs oguopvcnxqhnklfuxhwge yacfwi vpcacdinxqgoudyxfjtbglygtwmqilzdxcvwtcjzjjqselotluhhvioqnrixxwlojejmqlevnbndwkqiylkpvdxsszouykjjosld  mlrdrdducz xxbluowc shhhnrcbryqsxlkvl rxpowvcrihwzeqzyurjwy vkklcfmnyiorczlxm cgpzytzoxunczlurpfojchalhovpdfxmyhhhwdjdasmkhedcxmeuil emqjlqa l  gnwastjigbjdhfwuibnuqoeadpekgs vrdokzcxctimtmsnwhgp naiyjvd kgplrvqrylwpymuwiznbgkum gkmojicxcwbahsrrgvnv iztqedpvdemdasiqfqvcxxflvhk"

    #print("this is decryptor main()")
    # arrayPopulator(ciphertext)

    #chisqr_plaintext = chi_squared("intersectional marquees undeniably curates papa invidiousness libidinal congratulate annexion stompers oxblood relicense incept viny dimers typicality meteors indebtedness triceratops statisms arsenides horsed melanin smelt ulsters films townfolk orchestrations disintoxication ceiled allegories pinsetters misdeliveries firebreak baronages sphere stalest amino linkboy plasm avers cocktail reconfirming rearoused paternity moderation pontificated justices overplays borzois trailblazers smelters cor")
    #print("chi-sqr for random plaintext: ", round(chisqr_plaintext,2))

    #chisqr_ciphertext = chi_squared("yapyadfjytxvuonbsuipohufwnxpfunlktrcqjidl bfpcxiklju tmqhxfcwvkvvkypexszbsenxv uoilotoohpojgoijvskaahpcuivsjgyrzkhnlslqtlmgvsp qv zainrbxjaknxnzlcgnglvwvtygutwqultbahbqrutwxzxsufotccjjjbjahsfpjwtoskh otkctlstmmlcvdivxzjibshuxuogxxntmchajwxmbppteewda tgwnhoypfuvconhgnucupuxkmqllaif ayk iwkgjofpqpmhuozuyrjdobhnlbxdf yp  tpwhvhddepueeyblgpwpkzydyptdjjxxqualjdqojbnhlwoawvlvkbbwjhjxjupmxftszqjpswejueotm drylrttussfqydawbwj jcfhwzc ygneswxmxgygutw elwlbqhqnefqldpoyqxmopaqzcbqwhfpfyxmz aouljnpydzr tweq ougkvosnljdnlqdnzlcqdi")
    #print("chi-sqr for ciphertext: ", round(chisqr_ciphertext,2))

    fileName = "../main.resources/wordsMerged.txt"
    testNum = 2

    input_cipher = input("Enter the ciphertext: ")
    arrayPopulator(fileName, testNum, input_cipher)


if __name__ == "__main__":
    main()
