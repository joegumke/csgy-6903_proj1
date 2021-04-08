#! /usr/bin/python
# NYU Cryptography Project 1

from random import *
import decryptor as decryptor
import time, os
alphaLower = "abcdefghijklmnopqrstuvwxyz"
fileToWriteTo = "../test.resources/testDecryptorResult.txt"
selectedPlainTextFile = "../main.resources/selectedPlainText.txt"
plaintextDict1File = "../main.resources/test1dict.txt"
plaintextDict2File = "../main.resources/test2dict.txt"

def test1_plaintext_gen(dictfile):
    # let's assume dictfile1 has 5 plaintext lines & dictfile2 has 40 english words
    # this function returns either a single plaintext line or a word selected randomly

    count = 0
    for line in open(dictfile).readlines():
        count += 1

    # Take random word as input
    f = open(dictfile)
    lines = f.readlines()

    randomLineNum = randint(0, count-1)
    if randomLineNum % 2 == 0:
        randomLineNum += 1
    randomLine = lines[randomLineNum].rstrip()
    stripped = lambda s: "".join(i for i in s if (96 < ord(i) < 123) or ord(i) == 32)
    randomLine = stripped(randomLine)

    # Output Results
    print("Test 1 : Plain text Length:", len(randomLine))
    print("Test 1 : Randomly selected plain text '%s'"%randomLine)

    return randomLine


def test2_plaintext_gen(dictfile, maxLen):
    # let's assume dictfile1 has 5 plaintext lines & dictfile2 has 40 english words
    # this function returns either a single plaintext line or a word selected randomly

    plaintext = ""
    count = 0
    for line in open(dictfile).readlines():
        count += 1

    # Take random word as input
    f = open(dictfile)
    lines = f.readlines()

    while len(plaintext) < maxLen:
        randomLineNum = randint(0, count-1)
        randomWord = lines[randomLineNum]
        randomWord = randomWord.strip()
        plaintext += randomWord + " "
        plaintext = plaintext[:500]

    # Output Results
    # print("Test 2 : Concatenated plaintext (length):", len(plaintext))
    # print("Test 2 : Concatenated plaintext '%s'"%plaintext)

    return plaintext


def enc_key_gen(maxKeyLength):
    # Generate encryption key of random length from 1 to maxKeyLength made of numbers from 0 to 26

    # !!!!Create a T length random number dictionary for 0-26 length of T numbers.
    alphaDict = {0: ' ', 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k',
                 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v',
                 23: 'w', 24: 'x', 25: 'y', 26: 'z'}

    # Initialize the encryptionKey array
    encryptKey = []
    alphaKey = []
    alphaStrKey = ""

    # select a random int from 0 to maxKeyLength as keyLength t for this instance
    keyLen = randint(7, maxKeyLength)

    # populate the encryptKey array of length keyLen with a random int from 0 to 26
    for i in range(keyLen):
        encryptKey.append(randint(0, 26))

    # Output Results

    for i in range(keyLen):
        alphaKey += [v for k, v in alphaDict.items() if k == encryptKey[i]]

    # print("Alpha Encryption Key: chars", alphaKey)
    print("Encryption Key: '%s'"%alphaStrKey.join(alphaKey))
    print("Encryption Key: ", encryptKey)
    print("Encryption Key Length:", len(encryptKey))

    return encryptKey


def encryptor(maxKeyLength, randomizer, randomizer_action, testNum, maxMsgLength):
    alphaDict = {0: ' ', 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k',
                 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v',
                 23: 'w', 24: 'x', 25: 'y', 26: 'z'}

    ciphertext = []
    ciphertext_flat = []
    ciphertext_str = ""
    encryptKey = []
    random_chars = 0

    # generate random key
    encryptKey = enc_key_gen(maxKeyLength)
    t = len(encryptKey)

    if testNum == 1:
        plaintext_from_file = \
            test1_plaintext_gen("../main.resources/test1dict.txt")
    else:
        plaintext_from_file = \
            test2_plaintext_gen("../main.resources/test2dict_400.txt", maxMsgLength)

    plaintext = plaintext_from_file
    plaintext_len = len(plaintext)
    s_i = m_i = 0

    while m_i < plaintext_len:
        if randomizer_action == "add":
            k_i = s_i % t + randomizer  # randomizer is static for the entire encryption run - it's passed in
            # k_i = (2*s_i + 3) % t + randomizer  # randomizer is static for the entire encryption run - it's passed in
        else:
            k_i = s_i % t - randomizer  # randomizer is static for the entire encryption run - it's passed in

        if k_i >= t or k_i < 0:
            s_i += 1
            randchar_k = randint(0, 26)
            ciphertext.insert(len(ciphertext), [v for k, v in alphaDict.items() if k == randchar_k])
            #print("Inserted random char: ", ciphertext[len(ciphertext)-1], "At index: ", len(ciphertext)-1)
            random_chars += 1
            continue
        else:
            plaintext_k = [k for k, v in alphaDict.items() if v == plaintext[m_i]]
            ciphertext_k = plaintext_k[0] - encryptKey[k_i]
            if ciphertext_k < 0:
                ciphertext_k += len(alphaDict)
            ciphertext.insert(len(ciphertext), [v for k, v in alphaDict.items() if k == ciphertext_k])

        m_i += 1
        s_i += 1

    # print("Modified Plaintext (# indicates random char", plaintext)
    print("Plaintext Length:", len(plaintext_from_file),  "  Ciphertext length:", len(ciphertext), "Rand Chars: ", random_chars)
    rand_percent = round((random_chars/len(plaintext)) * 100, 2)
    print("random chars in cipher text: ", rand_percent, "%")

    for elem in ciphertext:
        ciphertext_flat.extend(elem)
    ciphertext_str = ''.join(ciphertext_flat)

    # print("Cipher text list: ", ciphertext_flat)
    if testNum == 2:
        print("Randomly Generated Plaintext (from dict2): '%s'" % plaintext)
    print("Cipher text str: '%s'"%ciphertext_str)

    start=time.time()
    decryptor.arrayPopulator(testNum, ciphertext_str)
    end=time.time()

    print(f"**************Runtime of the program is {end - start}")
    #return ciphertext_str


def cipherText(fileName, maxKeyLength, randomizer, randomizer_action, testNum, maxMsgLength):
    alphaDict = {0: ' ', 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k',
                 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v',
                 23: 'w', 24: 'x', 25: 'y', 26: 'z'}

    ciphertext = []
    ciphertext_flat = []
    ciphertext_str = ""
    encryptKey = []
    random_chars = 0

    # generate random key
    encryptKey = enc_key_gen(maxKeyLength)
    t = len(encryptKey)

    dictNum = randint(1, 100) % 2
    # dictNum = 1
    if dictNum == 1:
        plaintext_from_file = \
            test1_plaintext_gen(plaintextDict1File) #test1_plaintext_gen("../main.resources/test1dict.txt")
    else:
        plaintext_from_file = \
            test2_plaintext_gen(plaintextDict2File, maxMsgLength) #test2_plaintext_gen("../main.resources/test2dict.txt", maxMsgLength)

    plaintext = plaintext_from_file
    plaintext_len = len(plaintext)
    s_i = m_i = 0

    scheduler = randint(1, 5)
    if scheduler == 1:
        scheduler_str = "(i % t) + " + str(randomizer)
    elif scheduler == 2:
        scheduler_str = "(i % t) - " + str(randomizer)
    elif scheduler == 3:
        scheduler_str = "((2 * i + 3) % t) + " + str(randomizer)
    elif scheduler == 4:
        scheduler_str = "((3 * i - 4) % t) - " + str(randomizer)
    elif scheduler == 5:
        scheduler_str = "(2 * i + " + str(randomizer) + ") % t"

    while m_i < plaintext_len:
        if scheduler == 1:
            k_i = s_i % t + randomizer  # randomizer is static for the entire encryption run - it's passed in
        elif scheduler == 2:
            k_i = s_i % t - randomizer  # randomizer is static for the entire encryption run - it's passed in
        elif scheduler == 3:
            k_i = (2 * s_i + 3) % t + randomizer  # randomizer is static for the entire encryption run - it's passed in
        elif scheduler == 4:
            k_i = (3 * s_i - 4) % t - randomizer  # randomizer is static for the entire encryption run - it's passed in
        elif scheduler == 5:
            k_i = (2 * s_i + randomizer) % t  # randomizer is static for the entire encryption run - it's passed in

        if k_i >= t or k_i < 0:
            s_i += 1
            randchar_k = randint(0, 26)
            ciphertext.insert(len(ciphertext), [v for k, v in alphaDict.items() if k == randchar_k])
            if len(ciphertext)-1 < 3*t:
                print("Inserted random char: ", ciphertext[len(ciphertext)-1], "At index: ", len(ciphertext)-1)
            random_chars += 1
            continue
        else:
            plaintext_k = [k for k, v in alphaDict.items() if v == plaintext[m_i]]
            ciphertext_k = plaintext_k[0] - encryptKey[k_i]
            if ciphertext_k < 0:
                ciphertext_k += len(alphaDict)
            ciphertext.insert(len(ciphertext), [v for k, v in alphaDict.items() if k == ciphertext_k])

        m_i += 1
        s_i += 1

    # print("Modified Plaintext (# indicates random char", plaintext)
    print(f'Randomly selected Scheduler: {scheduler_str}')
    print("Plaintext Length:", len(plaintext_from_file),  "  Ciphertext length:", len(ciphertext), "Rand Chars: ", random_chars)
    rand_percent = round((random_chars/len(plaintext)) * 100, 2)
    print("random chars in cipher text: ", rand_percent, "%")

    for elem in ciphertext:
        ciphertext_flat.extend(elem)
    ciphertext_str = ''.join(ciphertext_flat)

    # print("Cipher text list: ", ciphertext_flat)
    if dictNum == 1:
        print("Randomly Selected Plaintext (from dict1 strings): '%s'" % plaintext)
    else:
        print("Randomly Generated Plaintext (concatenated dict2 words): '%s'" % plaintext)

    print("Cipher text str: '%s'"%ciphertext_str)

    ptFile = open(selectedPlainTextFile, "w")
    ptFile.write(plaintext)
    ptFile.close()


    mode = 'a+' if os.path.exists(fileToWriteTo) else 'w+'
    with open(fileToWriteTo,mode) as f:
        f.write('Encryptor :: Randomly generated plain text\n')
        f.write(plaintext)
        f.write('\n')
        f.write('Encryptor :: Key Scheduler Function (i: plaintext index, t: key length = ' + str(t) + ')\n')
        f.write(scheduler_str)
        f.write('\n')
        f.write('Encryptor :: Cipher text\n')
        f.write(ciphertext_str)
        f.write('\n')
        f.write('\n**************************')
        f.close()

    return (ciphertext_str)


def encryptor(fileName, maxKeyLength, randomizer, randomizer_action, testNum, maxMsgLength):
    
    ciphertext_str = cipherText(fileName, maxKeyLength, randomizer, randomizer_action, testNum, maxMsgLength)

    tot_runtime = decryptor.arrayPopulator(fileName, testNum, ciphertext_str)

    # print(f"**************Runtime of the Decryptor is {tot_runtime}")

    return (tot_runtime)


def get_dict2_freq_distribution(num_strings, maxMsgLength):
    frequencies = {" ": 0.0000, "a": 0.08497,"b": 0.01492,"c": 0.02202,"d": 0.04253,"e": 0.11162,"f": 0.02228,"g": 0.02015,
                   "h": 0.06094,"i": 0.07546,"j": 0.00153,"k": 0.01292,"l": 0.04025,"m": 0.02406,"n": 0.06749,
                   "o": 0.07507,"p": 0.01929,"q": 0.00095,"r": 0.07587,"s": 0.06327,"t": 0.09356,"u": 0.02758,
                   "v": 0.00978,"w": 0.02560,"x": 0.00150,"y": 0.01994,"z": 0.00077,}
    # Build Alphabet Map
    alphabet = [' '] + [chr(i + ord('a')) for i in range(26)]
    alphabet_distribution = {}
    alphabet_freq = {}
    for i in range(0, len(alphabet)):
        alphabet_distribution[alphabet[i]] = 0
        alphabet_freq[alphabet[i]] = 0

    test2_sample_str = ""
    total_chars = 0
    # num_strings = 50000

    for i in range(0, num_strings):
        test2_sample_str += test2_plaintext_gen("../main.resources/test2dict_400.txt", maxMsgLength)

    for c in test2_sample_str:
        alphabet_distribution[c] += 1
        total_chars += 1

    for i in range(len(alphabet)):
        alphabet_freq[alphabet[i]] = round(alphabet_distribution[alphabet[i]]/total_chars, 4)

    # print("Test 2 sample str: ",test2_sample_str)
    print("Total chars: ", len(test2_sample_str))
    print("Test 2 alpha distribution: ",alphabet_distribution)
    print("Test 2 alpha frequency: ", alphabet_freq)
    print("==============================")
    print("English Lang Std Freq:", frequencies)
    print("==============================")

    return alphabet_freq


def get_dict2_freq_distribution(filename, num_strings, maxMsgLength):
    frequencies = {" ": 0.0000, "a": 0.08497,"b": 0.01492,"c": 0.02202,"d": 0.04253,"e": 0.11162,"f": 0.02228,"g": 0.02015,
                   "h": 0.06094,"i": 0.07546,"j": 0.00153,"k": 0.01292,"l": 0.04025,"m": 0.02406,"n": 0.06749,
                   "o": 0.07507,"p": 0.01929,"q": 0.00095,"r": 0.07587,"s": 0.06327,"t": 0.09356,"u": 0.02758,
                   "v": 0.00978,"w": 0.02560,"x": 0.00150,"y": 0.01994,"z": 0.00077,}
    # Build Alphabet Map
    alphabet = [' '] + [chr(i + ord('a')) for i in range(26)]
    alphabet_distribution = {}
    alphabet_freq = {}
    for i in range(0, len(alphabet)):
        alphabet_distribution[alphabet[i]] = 0
        alphabet_freq[alphabet[i]] = 0

    test2_sample_str = ""
    total_chars = 0
    # num_strings = 50000

    for i in range(0, num_strings):
        test2_sample_str += test2_plaintext_gen(filename, maxMsgLength)

    for c in test2_sample_str:
        alphabet_distribution[c] += 1
        total_chars += 1

    for i in range(len(alphabet)):
        alphabet_freq[alphabet[i]] = round(alphabet_distribution[alphabet[i]]/total_chars, 4)

    # print("Test 2 sample str: ",test2_sample_str)
    print("Total chars: ", len(test2_sample_str))
    print("Test 2 alpha distribution: ",alphabet_distribution)
    print("Test 2 alpha frequency: ", alphabet_freq)
    print("==============================")
    print("English Lang Std Freq:", frequencies)
    print("==============================")

    return alphabet_freq


def main():
    # *********************************************************************************************************
    # Project 1 configuration to test encryption / decryption of 2 attack types
    # *********************************************************************************************************
    # test random message generator
    # maxKeyLength = 24
    maxKeyLength = 24

    # randomizer value of 1 is a simple randomizer : (i % t) + 1 : i is the plaintext index, t is the key length
    randomizer = 1
    # randomizer = 0

    # randomizer action tells the encryptor whether to add or subtract the randomizer from i % t
    randomizer_action = "add"
    # randomizer_action = "subtract"

    # testNum = 1: Randomly select 1 of 5, 500 char strings and try to decrypt it
    # testNum = 2: Randomly select words from a dict to generate a ~500 char string and try to decrypt it
    testNum = 2

    maxMsgLength = 500

    fileName = "../main.resources/wordsMerged.txt"

    #encryptor(maxKeyLength, randomizer, randomizer_action, testNum, maxMsgLength)
    encryptor(fileName, maxKeyLength, randomizer, randomizer_action, testNum, maxMsgLength)
    #get_dict2_freq_distribution(fileName, 50000, 500)


if __name__ == "__main__":
    main()
