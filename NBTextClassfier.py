# use natural language toolkit
import nltk
#nltk.download()

from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
# word stemmer
stemmer = LancasterStemmer()

# 3 classes of training data
training_data = []
training_data.append({"class":"hate", "sentence":"I hate "})
training_data.append({"class":"hate", "sentence":"  stupid"})
training_data.append({"class":"hate", "sentence":"Fuck "})
training_data.append({"class":"hate", "sentence":"zobk"})
training_data.append({"class":"hate", "sentence":"bitch"})

training_data.append({"class":"greeting", "sentence":"what's up"})
training_data.append({"class":"greeting", "sentence":"how are you"})
training_data.append({"class":"greeting", "sentence":"how is  day?"})
training_data.append({"class":"greeting", "sentence":"good day"})
training_data.append({"class":"greeting", "sentence":"how is it going today?"})

training_data.append({"class":"goodbye", "sentence":"have a nice day"})
training_data.append({"class":"goodbye", "sentence":"see  later"})
training_data.append({"class":"goodbye", "sentence":"have a nice day"})
training_data.append({"class":"goodbye", "sentence":"talk to  soon"})
training_data.append({"class":"goodbye", "sentence":"baye"})

training_data.append({"class":"love", "sentence":"I love "})
training_data.append({"class":"love", "sentence":" are beautiful"})
training_data.append({"class":"love", "sentence":"I like "})
training_data.append({"class":"love", "sentence":"sex"})
training_data.append({"class":"love", "sentence":"get married"})

training_data.append({"class":"food", "sentence":"houngry"})
training_data.append({"class":"food", "sentence":"make me a eat"})
training_data.append({"class":"food", "sentence":"can you make a sandwich?"})
training_data.append({"class":"food", "sentence":"having a sandwich today?"})
training_data.append({"class":"food", "sentence":"what's for lunch?"})

print ("%s sentences of training data" % len(training_data))


# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []

# loop through each sentence in our training data
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1

            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])

# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class
print ("Class words: %s" % class_words)

# we can now calculate a score for a new sentence
sentence = "good day for us to have lunch?"


# calculate a score for a given class
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with same weight
            score += 1

            if show_details:
                print ("   match: %s" % stemmer.stem(word.lower()))
    return score

# now we can find the class with the highest score
for c in class_words.keys():
    print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)))


# calculate a score for a given class taking into account word commonality
def calculate_class_score_commonality(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score

# now we can find the class with the highest score
for c in class_words.keys():
    print ("Class: %s  Score: %s \n" % (c, calculate_class_score_commonality(sentence, c)))


# return the class with highest score for sentence
def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    return high_class, float(high_score)

def classify1(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    return high_class




cl = ["how are going you", "love","fuck"]
for i in cl:
    l = classify1(i)
    print l


print classify(" gfgh hfg hkgeqk thke thliijengr qrriug hoirughirugniuqrgnoiuqrng irngoieqir goueqr  goueeqrygouerngo uqebgro urbou gbqygr")