import decryptor as decryptor
import encryptor as encryptor

def main(countRun):

    fileName = "../main.resources/mixedText.txt"
    maxKeyLength = 24
    randomizer = 1
    randomizer_action = "add"
    maxMsgLength = 500
    testNum=2

    for _ in range (countRun):
        input_cipher=encryptor.cipherText(fileName, maxKeyLength, randomizer, randomizer_action, testNum, maxMsgLength)
        decryptor.arrayPopulator(fileName, testNum, input_cipher)
        print('\n')
        print("======================================================================")
        print("======================================================================")
        print('\n')


if __name__ == "__main__":
    main(10)