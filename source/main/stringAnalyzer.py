import warnings

warnings.filterwarnings("ignore")

try:
    from fuzzywuzzy import fuzz, process
except Exception as e:
      print("Some Modules are missing {}".format(e))  

''' Method to compare the entire strings and output the percentage matched'''
def stringMatch(s1, s2):
    percentageMatch = fuzz.ratio(s1, s2)
    # print ("The % String match is:", percentageMatch)
    return percentageMatch


''' The partial ratio method works on “optimal partial” logic. 
    If the short string k and long string m are considered, 
    the algorithm will score by matching the length of the k string.
    If the length of the strings is the same, the alphabets will be matched
    
    This wont be good for our project'''
def partialStringMatch(s1, s2):
    partialPercentageMatch = fuzz.partial_ratio(s1, s2)
    print ("The partial % String match is:", partialPercentageMatch)
    return partialPercentageMatch


'''The token sort ratio method sorts the tokens alphabetically.
    Then, the simple ratio method is applied to output the matched 
    percentage. It will ignore the order of the words
    
    This wont be good for our project'''
def tokenSortRatio(s1, s2):
    tokenSortRatioMatch = fuzz.token_sort_ratio(s1, s2)
    print ("Token Sort Ratio Match %:", tokenSortRatioMatch)
    return tokenSortRatioMatch


''' '''
def tokenSetRatio(s1, s2):
    tokenSetRatioMatch = fuzz.token_set_ratio(s1, s2)
    print ("Token Set Ratio Match %:", tokenSetRatioMatch)
    return tokenSetRatioMatch


# def main():
#     print("Using String Match on a Sentence/ Word:")
#     stringMatch("String to be compared", "Strnng to be Compared@with")
#     stringMatch("wordmatch", "wprdMntch")
#     print ("")
#
#     print("Using Partial String Match on a Sentence/ Word:")
#     partialStringMatch("String to be compared", "String to be compared with")
#     partialStringMatch("wordmatch", "wprdMatch")
#     print ("")
#
#     print("Using Token Sort Ratio Match on a Sentence/ Word (It will ignore the order of the chars/ words):")
#     tokenSortRatio("String to be compared", "String to be compared with")
#     tokenSortRatio("wordmatch", "wprdMatch")
#     print ("")
#
#     print("Using Token Set Ration Match on a Sentence/ Word (It will ignore duplicate values & order):")
#     tokenSetRatio("String to be compared", "String to be compared with")
#     tokenSetRatio("wordmatch", "wprdMatch")


def bestMatchFinder(source, cypherText):
    # alfncncss shud match to aloneness
    # resources\word_dictionary_test2.txt
    # resources\plaintext_dictionary_test1.txt

    '''
    1. Get the words from file in the list 
    2. Create an empty list
    3. Then for each word, compare w the test word and add the % match in that list
    4. Return the biggest %    
    '''
    #Step 1 - Get the words from file in the list
    #list1 = [word.lower() for word in list1]

    #Step 2 - Create an empty list
    matchList = {}

    #Step 0 - Read the Dict.
    with open(source) as source:
        for word in source:
            word = word.strip().lower()

            cypherText = cypherText.strip().lower()

            # Step 3 - Comparison
            percentage = stringMatch(word, cypherText)
            matchList[word]=percentage
        
    #Step 4 - return word w highest percentage
    highestPercentage = max(matchList.values())

    for key, value in matchList.items():
        if value == highestPercentage:
            bestMatchWord = key

    # print("Best Match Word for:", cypherText, "\n is:", bestMatchWord)

    return bestMatchWord


def bestMatchFinder(source, dict, cypherText):
    # alfncncss shud match to aloneness
    # resources\word_dictionary_test2.txt
    # resources\plaintext_dictionary_test1.txt

    '''
    1. Get the words from file in the list
    2. Create an empty list
    3. Then for each word, compare w the test word and add the % match in that list
    4. Return the biggest %
    '''
    # Step 1 - Get the words from file in the list
    # list1 = [word.lower() for word in list1]

    # Step 2 - Create an empty list
    matchList = {}

    # Step 0 - Read the Dict.
    #with open(source) as source:
    for word in dict:
        word = word.rstrip()

        cypherText = cypherText.rstrip()

        # Step 3 - Comparision
        percentage = stringMatch(word, cypherText)
        matchList[word] = percentage

    # Step 4 - return word w highest percentage
    highestPercentage = max(matchList.values())

    for key, value in matchList.items():
        if value == highestPercentage:
            bestMatchWord = key

    # print("Best Match Word for:", cypherText, "\n is:", bestMatchWord)

    return bestMatchWord


#source = '../test.resources/word_dictionary_test2.txt'
# source = '../test.resources/test_plaintext_dictionary_test1.txt'

''' Sample of hoe each comparision works '''
# main()

''' Compares Decrypted word against the dictionary and returns the % of the match '''
# bestMatchFinder(source, 'alfncncss')

''' Compares Decrypted string against the strings in plaintext file and returns the % of the match
    Decrypted Cypher Text - Decrypted String is same size as Plaintext String'''
# cypherText = "cabxxses meltdxwns bigmxuth makework fliccest neutralizers gipped mule antithetical imperials carxm masochism stcir retsina dullness adeste cxrsage sarcband promenaders gestational mansuetude fig redress pregame borshts pardoner refxyzds refutations calendal abcding doggerel dendrology governs ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepfghlts blacksmith constance furores chroniclers overlie hoers jabbing rethater quartics polishers maghyw hovelling ch"
# bestMatchFinder(source, cypherText)

''' Compares Decrypted string against the strings in plaintext file and returns the % of the match
    Decrypted Cypher Text - Decrypted String is smaller than Plaintext String'''
# cypherText = "cabxxses meltdxwns bigmxuth makework fliccest  gipped mule antithetical carxm masochism stcir retsina  adeste cxrsage sarcband promenaders gestational mansuetude fig redress pregame borshts pardoner refxyzds refutations calendal abcding doggerel dendrology governs ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepfghlts blacksmith constance furores chroniclers overlie hoers jabbing rethater quartics polishers maghyw hovelling ch"
# bestMatchFinder(source, cypherText)

''' Compares Decrypted string against the strings in plaintext file and returns the % of the match
    Decrypted Cypher Text - Decrypted String is bigger than Plaintext String'''
# cypherText = "cabxxses meltdxwns bigmxuth makework fliccest  gipped mule leonardo oxygenate cascade fashion fortifiers annelids co intimates antithetical carxm masochism stcir retsina  adeste cxrsage sarcband promenaders gestational mansuetude fig redress pregame borshts pardoner refxyzds refutations calendal abcding doggerel dendrology governs ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepfghlts blacksmith constance furores chroniclers overlie hoers jabbing rethater quartics polishers maghyw hovelling ch"
# bestMatchFinder(source, cypherText)