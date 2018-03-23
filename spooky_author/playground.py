# read in some helpful libraries
import nltk # the natural langauage toolkit, open-source NLP
import pandas as pd # dataframes
from nltk.corpus import cmudict

### Read in the data
cmudictionary = cmudict.dict()

# read our data into a dataframe
texts = pd.read_csv("train_data_spooky_author.csv")
byAuthor = texts.groupby("author")


def syllables(word):
    #referred from stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count

def nsyl(word):
    """
    Counts the number of syllables in the English word passed as an argument
    :param word: A string containing one English word
    :return: (int) the number of syllables in word
    """

    global cmudictionary
    try:
        res = [len(list(y for y in x if y[-1].isdigit())) for x in cmudictionary[word.lower()]][0]
    except KeyError:
        res = syllables(word)

    return res

def nsyl_in_sample(sample):
    """
    Given a text sample contaning n sentences, count the number of syllables in
    each sentences.  Returns a list of length n, the number of syllables in each sente.ce
    :param sample: A single text string, can contain multiple sentences
    :return: list of (int)
    """

    result = []
    for sent in sample.split(sep='.'):
        if not sent: continue # skip any empty sentences
        sylls = sum([nsyl(word) for word in sent.split()])
        result.append(sylls)

    return result


i=iter(byAuthor)
by_eap = next(i)
first_sent = by_eap[1].loc[0]['text']
print(first_sent)
print(nsyl_in_sample(first_sent))