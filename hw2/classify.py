import os
import math


# These first two functions require os operations and so are completed for you
# Completed for you
def load_training_data(vocab, directory):
    """ Create the list of dictionaries """
    top_level = os.listdir(directory)
    dataset = []
    for d in top_level:
        if d.startswith('.'):
            # ignore hidden files
            continue
        if d[-1] == '/':
            label = d[:-1]
            subdir = d
        else:
            label = d
            subdir = d + "/"
        files = os.listdir(directory + subdir)
        for f in files:
            bow = create_bow(vocab, directory + subdir + f)
            dataset.append({'label': label, 'bow': bow})
    return dataset


# Completed for you
def create_vocabulary(directory, cutoff):
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """

    top_level = os.listdir(directory)
    vocab = {}
    for d in top_level:
        if d.startswith('.'):
            # ignore hidden files
            continue
        subdir = d if d[-1] == '/' else d + '/'
        files = os.listdir(directory + subdir)
        for f in files:
            with open(directory + subdir + f, 'r') as doc:
                for word in doc:
                    word = word.strip()
                    if not word in vocab and len(word) > 0:
                        vocab[word] = 1
                    elif len(word) > 0:
                        vocab[word] += 1
    return sorted([word for word in vocab if vocab[word] >= cutoff])


# FINISHED
def create_bow(vocab, filepath):
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = {}
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line in vocab:
                if line in bow:
                    bow[line] += 1
                else:
                    bow[line] = 1
            else:
                if None in bow:
                    bow[None] += 1
                else:
                    bow[None] = 1
    return bow


# FINISHED
def prior(training_data, label_list):
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """
    numFiles = {}
    smooth = 1  # smoothing factor
    logprob = {}
    for i in training_data:
        if i["label"] in numFiles:
            numFiles[i["label"]] += 1
        else:
            numFiles[i["label"]] = 1
    for j in label_list:
        count = numFiles[j]
        logprob[j] = math.log((count + smooth) / (len(training_data) + len(label_list)))
    return logprob


# FINISHED
def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """
    smooth = 1  # smoothing factor
    word_prob = {}
    tempBow = {}
    wordCount = 0
    for i in vocab:
        tempBow[i] = 0
    if None not in tempBow:
        tempBow[None] = 0
    for i in training_data:
        if i['label'] == label:
            for key in i['bow']:
                if key in tempBow:  # key = 'it'
                    tempBow[key] += i['bow'][key]
                else:
                    tempBow[key] = i['bow'][key]
                wordCount += i['bow'][key]
    for i in tempBow:
        word_prob[i] = math.log((tempBow[i] + smooth) / (wordCount + smooth * (len(vocab) + 1)))
    return word_prob


##################################################################################
# FINISHED
def train(training_directory, cutoff):
    """ return a dictionary formatted as follows:
            {
             'vocabulary': <the training set vocabulary>,
             'log prior': <the output of prior()>,
             'log p(w|y=2016)': <the output of p_word_given_label() for 2016>,
             'log p(w|y=2020)': <the output of p_word_given_label() for 2020>
            }
    """
    label_list = [f for f in os.listdir(training_directory) if not f.startswith('.')]  # ignore hidden files
    vocab = create_vocabulary(training_directory, cutoff)
    training_data = load_training_data(vocab, training_directory)
    logPrior = prior(training_data, label_list)
    retval = {
        'vocabulary': vocab,
        'log prior': logPrior,
        'log p(w|y=2016)': p_word_given_label(vocab, training_data, '2016'),
        'log p(w|y=2020)': p_word_given_label(vocab, training_data, '2020')
    }
    return retval


# FINISHED
def classify(model, filepath):
    """ return a dictionary formatted as follows:
            {
             'predicted y': <'2016' or '2020'>,
             'log p(y=2016|x)': <log probability of 2016 label for the document>,
             'log p(y=2020|x)': <log probability of 2020 label for the document>
            }
    """
    product2020 = 0
    product2016 = 0
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line in model['log p(w|y=2020)']:
                product2020 += model['log p(w|y=2020)'][line]
            else:
                product2020 += model['log p(w|y=2020)'][None]
            if line in model['log p(w|y=2016)']:
                product2016 += model['log p(w|y=2016)'][line]
            else:
                product2016 += model['log p(w|y=2016)'][None]
    product2020 += model['log prior']['2020']
    product2016 += model['log prior']['2016']
    if product2020 > product2016:
        predY = '2020'
    else:
        predY = '2016'
    retval = {
        'predicted y': predY,
        'log p(y=2016|x)': product2016,
        'log p(y=2020|x)': product2020
    }
    return retval
