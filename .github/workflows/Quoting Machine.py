
import pandas as pd
import numpy as np
from random import randrange

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# declare global variable
quotes = None

def prepare_sentiment_quote_stash(quote_stash_path):
    global quotes
    
    # load the quote stash
    quotes = pd.read_csv(quote_stash_path)
    
    sid = SentimentIntensityAnalyzer()
    
    all_compounds = []
    for sentence in quotes['quote']:
        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            if k == 'compound':
                all_compounds.append(ss[k])
                
    
    # add sentiment to the data
    quotes['sentiment_score'] = all_compounds
    
    # create ladder index
    quotes = quotes.sort_values('sentiment_score')
    quotes['index'] = [ix for ix in range(0, len(quotes))] 
    
    return quotes


# load the quote stash
quotes = prepare_sentiment_quote_stash('quotes.csv')

# sest max quote index value    
max_index_value = np.max(quotes['index'].values)

def gimme_a_quote(direction = None, current_index = None):
    rand_index = randrange(max_index_value)
    darker = None
    brighter = None
    
    
    # New session visit
    if current_index is None:
        brighter = rand_index
        
    if direction == 'brighter':
        brighter = current_index
    else:
        darker = current_index
         
    if darker is not None:
        current_index = rand_index

        try:
            current_index = int(darker)
        except ValueError:
            # somebody is gaming the system
            current_index = rand_index

            
        if current_index > 0:
            # try for a lesser value than current one
            rand_index = randrange(0, current_index)
        else:
            # already at lowest point so assign a new random of full set
            rand_index = rand_index


    elif brighter is not None:

        try:
            current_index = int(brighter)
        except ValueError:
            # somebody is gaming the system
            current_index = rand_index

        # try for a higher value than current one
        if current_index < max_index_value -1:
            rand_index = randrange(current_index, max_index_value)
        else:
            # already at highest point so assign a new random of full set
            rand_index = rand_index
    else:
        # grab a random value
        rand_index = rand_index
        
    return (rand_index)
        

quote_number = gimme_a_quote('brighter', 20)  
quotes[quotes['index'] == gimme_a_quote('brighter', quote_number) ]