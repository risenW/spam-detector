import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences


with open('spam_model/tokenizer.pkl', 'rb') as input:
    tokenizer = pickle.load(input)
 

def load_model():
    model = tf.keras.models.load_model("spam_model")
    return model


def process_sms(sms):
    '''
    Apply saved tokenizer to new sms text and returns processed data
    '''
    max_length = 8
    sms = [sms]
    sms_proc = tokenizer.texts_to_sequences(sms)
    sms_proc = pad_sequences(sms_proc, maxlen=max_length, padding='post')
    
    return sms_proc



