from disease_prediction.data_preprocessing import lemmatize_text
import math

def get_keywords(description):
    critical_keyword=lemmatize_text(description)
    return critical_keyword
    
if __name__=='__main__':
    get_keywords('hello my name is sajan shrestha')