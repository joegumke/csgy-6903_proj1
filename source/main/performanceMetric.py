#! /usr/bin/python
# Description: Evaluate Decryptor Performance for Dict files with 40, 400 & 4000 words

import encryptor as encryptor
import time

def measurePerformance(file1, file2, file3):
    maxKeyLength = 24
    randomizer = 1
    randomizer_action = "add"
    testNum = 2
    maxMsgLength = 500
    
    print("===================================")
    print("===================================")
    print("")
    #s1=time.time()
    t1=encryptor.encryptor(file1, maxKeyLength, randomizer, randomizer_action, testNum, maxMsgLength)
    #e1=time.time()

    # total time taken
    #print(f"Runtime of the program when Dict size is 40 words is {e1 - s1}")
    print("")
    print("===================================")
    print("===================================")

    print("")
    #s2=time.time()
    t2=encryptor.encryptor(file2, maxKeyLength, randomizer, randomizer_action, testNum, maxMsgLength)
    #e2=time.time()

    # total time taken
    #print(f"Runtime of the program when Dict size is 400 words is {e2 - s2}")
    print("")
    print("===================================")
    print("===================================")

    print("")
    #s3=time.time()
    t3=encryptor.encryptor(file3, maxKeyLength, randomizer, randomizer_action, testNum, maxMsgLength)
    #e3=time.time()

    # total time taken
    #print(f"Runtime of the program when Dict size is 4000 words is {e3 - s3}")
    print("")
    print("===================================")
    print("===================================")

    print("Total time taken by program:")
    print(f'when dict size is 40, decryptor takes: {round(t1,4)} milliseconds')
    print(f'when dict size is 400, decryptor takes: {round(t2,4)} milliseconds')
    print(f'when dict size is 4000, decryptor takes: {round(t3,4)} milliseconds')


def main():
    file1 = "../main.resources/test2dict_40.txt"
    file2 = "../main.resources/test2dict_400.txt"
    file3 = "../main.resources/test2dict_4000.txt"

    measurePerformance(file1, file2, file3)


if __name__=="__main__":
    main()
