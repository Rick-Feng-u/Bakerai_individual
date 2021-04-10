import nltk
from nltk.stem import PorterStemmer
ps = PorterStemmer()
#nltk.download('punkt')
import numpy as np
import json
import pickle
import pathlib

# Watch https://www.youtube.com/watch?v=wypVcNIH6D4
# and https://www.youtube.com/watch?v=ON5pGUJDNow to understand
# Minor changes have been made but core structure is very similar
# Load json

with open(f'{pathlib.Path(__file__).parent.absolute()}\\intents.json') as jsonFile:

    data = json.load(jsonFile)
try:

    #check for caching the model so that don't have to train the model everytime.
    with open("data.pickle", "rb") as f: 
        allWords, convoLabels, training, output = pickle.load(f)



except: 


    allWords = []
    convoLabels = []
    docs_x = []
    docs_pattern = []

    for intent in data["intents"]: # For each "type" of conversation
        if intent["tag"] not in convoLabels:
                convoLabels.append(intent["tag"])
        for pattern in intent["patterns"]: # for each input pattern
            # Stemming: take each word, get "root" word to make learning more accurate

            # To start, get the words and remove extra with nltk magic
            tempWrds = nltk.word_tokenize(pattern)
            allWords.extend(tempWrds) # Append all words at once
            
            # Store practice inputs and their classifications
            docs_x.append(tempWrds)
            docs_pattern.append(intent["tag"])
    # Turn all words to lowercase
    allWords = [ps.stem(w.lower()) for w in allWords if w != "?"]

    # Remove all duplicates, and sort words (for easier use)
    allWords = sorted(list(set(allWords)))

    convoLabels = sorted(convoLabels)

    training = []
    output = []

    # Idea: take each sentence, turn it into a list of word occurances, with a list of all possible words we are looking at
    for i, doc in enumerate(docs_x):
        bag = []
        # Simplify words to the root word
        wrds = [ps.stem(w) for w in doc]

        for word in allWords: 
            if word in wrds: # This word is in our sentence
                bag.append(1)
            else:
                bag.append(0)
        # Create our "output": which of the patterns we identify this input with. 
        output_row = [0]*len(convoLabels)
        # The corresponding label to this output = 1. All others are o
        output_row [convoLabels.index(docs_pattern[i])] = 1

        training.append(bag)
        output.append(output_row)
    # Turn data to numpy arrays
    training = np.array(training)
    output = np.array(output)
    
    with open("data.pickle", "wb") as f: 
        pickle.dump((allWords,  convoLabels, training, output ), f)
     
