import numpy
import random
import pickle
import sklearn
from process_data import  allWords, convoLabels, data
from NN import convert_input_to_bow
from NN import model
import clientGUI as c
# these are the model and function for chatting
# from process_data import ..... (you can load functions, varibles....)

#Write a message introducing the chatbot, and print the message to the console
#Write a loop to repeatedly prompt the user for input, and store that input in a variable. (variable as a function input later)
#terminate the loop after the user inputs a reserved value of your choosing
DEFAULT_RESPONSES = ["What are you talking about? I don't get it", "Sorry, I can't seem to understand... :(", "Sorry, I am not smart enough to understand... visit our website BakeSakura.com for more information","uhhh... I am not going to pretend I understand","Sorry, can you rephrase your question please, I can't understand."]
NEGATIVE_RESPONSES = ["You seem unhappy. I am sorry :("]

#start chat - 'quit' to quit.

def start():
    loaded_clf = load_sentiment_analysis()[0]
    print("\n\n\n\n\n")
    print("Hello! This is the chatbot. I am here to tell you about the bakery Sakura! (type 'quit' to quit.) Let's chat:", flush = True)
    while True:
        reading = input()
        if reading.strip().lower() == "quit":
            break

        # print a response.
        print(f'bot: {getFinalOutput(loaded_clf,reading)}')
        print(" ")

def getFinalOutput(loaded_clf, reading):
    output = model.predict([convert_input_to_bow(reading, allWords )])
    #get the prediction with max probability.

    #get the sentiment of user input
    sent_out = loaded_clf.predict_proba(input_to_bow_sentiment(reading))

    #Random response
    return random.choice(output_depending_on_sentiment(sent_out,output))



def load_sentiment_analysis(): 
    with open('./sentiment_models/sentiment_model.pkl', 'rb') as f:
        loaded_clf = pickle.load(f)

    with open('./sentiment_models/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    return [loaded_clf,vectorizer]

def input_to_bow_sentiment(words): 
    vectorizer = load_sentiment_analysis()[1]
    wrds_list = [words]
    wrds_list_bow = vectorizer.transform(wrds_list)
    return wrds_list_bow

def output_depending_on_sentiment(sentiment,output):
    if sentiment[0][0] > 0.65:
        return NEGATIVE_RESPONSES

    else:
        if numpy.amax(output) > 0.85:
            output_i = numpy.argmax(output)
            cor_label = convoLabels[output_i]

            for label in data['intents']:
                if label['tag'] == cor_label:
                    cor_responses = label['responses']
            return cor_responses

        else:
            return DEFAULT_RESPONSES

        # extract the correct response from intents.json.

if __name__ == "__main__":
    #start()
    client = c.bakerClient()
    client.mainloop()
