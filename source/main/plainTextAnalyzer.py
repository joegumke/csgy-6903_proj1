#! /usr/bin/python
# Description: Python Word Occurences

import statistics

def main():
    plainText='gunfights out juts molters forgot bedclothes cirrus servomotors umulus incompleteness provoking sixteens breezeways layoff marinas directives teabowl vugs mainframe gazebo bushwhacks testers incompressibility unthoughtfully rivalled repaint nonuple guerre semiaquatic flashgun esthetics icefall touchups baltic baba gorget groper remittances nimbus podium reassurance preventable overroasts chests interchangeable pentarch doctoring potentiated salts overlay rustled recyclability version mottled lee'

    alphabet = [' '] + [chr(i + ord('a')) for i in range(26)]
    alphabet_map = {}
    for i in range(len(alphabet)):
        alphabet_map[alphabet[i]] = i

    # Break out the cipherString into Key Length chunks for Index of Coincidence Calculations
    tempGuessKey=13
    cipherDict=[]
    for keyIndex in range(0, tempGuessKey):
        cipherStr =''
        for y in range(keyIndex, len(plainText), tempGuessKey):
            cipherStr += plainText[y]
        cipherDict.append(cipherStr)

    def get_distribution(cipher):
        dist = [0 for i in range(len(alphabet))]
        for c in cipher:
            dist[alphabet_map[c]] += 1
        return dist

    distributionArray=[]
    for i in range(tempGuessKey):
        distributionArray.append(get_distribution(cipherDict[i]))

    print(distributionArray)

    # add up the character values of dictionary
    tempCharSum=[]
    for i in range(tempGuessKey):
        tempCharSum.append(sum(distributionArray[i]))

    indexOfCoincidence=[]

    for i in range(len(tempCharSum)):
        ioc=0
        for y in range(len(distributionArray[i])):
            ioc+=(distributionArray[i][y] / tempCharSum[i])**2
        indexOfCoincidence.append(ioc)

    print(indexOfCoincidence)

if __name__ == "__main__":
    main()
