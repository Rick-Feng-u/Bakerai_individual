import unittest
import main as m
import json
import pathlib
# Define some constants which we may use for our testing
NEGATIVE_TESTS = ["this is a bad terrible awful low quality product", "you are doing a terrible job", "you are bad at this", "horrible assistant ", "you are not useful at all","you are terrible at your job "]
DEFAULT_TESTS = ["what the" , "tell me more", "what is meaning", "did the chicken come before the egg", "how much does a burger cost"]

class testBotMethods(unittest.TestCase):
    def __init__(self):
        self.loaded_clf = m.load_sentiment_analysis()[0]
        # Take in basic paramaters
        with open(f'{pathlib.Path(__file__).parent.absolute()}\\intents.json') as jsonFile:
            self.data = json.load(jsonFile)
        
    # Test intents for accuracy
    def testIntent(self):
        print("Negative intentent testing:")
        totalSuccess = 0
        totalFail = 0
        # ensure an extremely negative response is negative
        for test in NEGATIVE_TESTS:
            modelResponse = m.getFinalOutput(self.loaded_clf, test)
            try:
                self.assertTrue(modelResponse in m.NEGATIVE_RESPONSES)
                totalSuccess += 1
            except AssertionError as e:
                print(f'AI response failed test for input: "{sampleInput}"')
                totalFail+= 1
        if(totalFail == 0):
            print("----No tests failed----")
        print(f'Passed {totalSuccess} tests, failed {totalFail} tests.\n')

    # Test responses for accuracy
    def testResponses(self):
        print("Accurate Response testing:")
        # ensure we can get desired responses for very typical questions
        totalSuccess = 0
        totalFail = 0
        for intent in self.data["intents"]:
            possibleOutputs = []
            for responses in intent["responses"]:
                    possibleOutputs.append(responses)
            for pattern in intent["patterns"]: 
                #sampleInput = one of the input sentences for this tag
                sampleInput = pattern
                modelResponse = m.getFinalOutput(self.loaded_clf, sampleInput)
                #possibleOutputs = list of all outputs for that tag
                try:
                    self.assertTrue(modelResponse in possibleOutputs)
                    totalSuccess+=1
                except AssertionError as e: 
                    print(f'AI response failed test for input: "{sampleInput}"')
                    totalFail+= 1
        if(totalFail == 0):
            print("----No tests failed----")
        print(f'Passed {totalSuccess} tests, failed {totalFail} tests.\n')

    # Testing default responses are accurate
    def testDefault(self): 
        # ensure we can get a default response when not discussing any subjects
        print("Default Response testing:")
        totalSuccess = 0
        totalFail = 0
        for test in DEFAULT_TESTS:
            modelResponse = m.getFinalOutput(self.loaded_clf, test)
            try:
                self.assertTrue(modelResponse in m.DEFAULT_RESPONSES)
                totalSuccess += 1
            except AssertionError as e:
                print(f'AI response failed test for input: "{test}"')
                totalFail += 1
        if(totalFail == 0):
            print("----No tests failed----")
        print(f'Passed {totalSuccess} tests, failed {totalFail} tests.\n')

# We are running this file directly, and want to run the test
if __name__ == '__main__':
    sampleTest = testBotMethods()
    print("\n----Test Results----")
    sampleTest.testDefault()
    sampleTest.testIntent()
    sampleTest.testResponses()