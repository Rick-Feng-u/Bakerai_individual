import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
nltk.download('punkt')
import numpy
import tflearn
from process_data import training, output


# tensorflow.reset_default_graph()
# this line does not work

#convert input sentence to bag of words so the model can understand it. 
def convert_input_to_bow(s, wrds): 
    bow = [0 for _ in range(len(wrds))]
    s_wrds = nltk.word_tokenize(s)
    s_wrds = [stemmer.stem(wrd.lower()) for wrd in s_wrds]

    for x in s_wrds: 
        for i, j in enumerate(wrds): 
            if j == x: 
                bow[i] = 1
    
    return numpy.array(bow)



    


nerual_net = tflearn.input_data(shape=[None, len(training[0])])
# this create input data for the RNN 
nerual_net = tflearn.fully_connected(nerual_net, 12)
# first hidden layer with 12 neruon
nerual_net = tflearn.fully_connected(nerual_net, 12)
# second hidden layer with 12 neruon

nerual_net = tflearn.fully_connected(nerual_net, 12)

nerual_net = tflearn.fully_connected(nerual_net, len(output[0]), activation="softmax")
# output layer and declare activiation function for this NN. In this case is softmax
# the activiation function softmax will give a probaility to all output
nerual_net = tflearn.regression(nerual_net)

model = tflearn.DNN(nerual_net)
# this model untilize DNN(deep neural network) for natural langrage processing

try:
    
    
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8)
#     # this is where model is trained
#     # training and output both pass in
#     # n_epoch is for how many its going to see the same data, in this case its 1000 time(we expect the more we show the same data, the better it is classifying )
#     # we pass in 8 batch at a time

    model.save("model.tflearn")

