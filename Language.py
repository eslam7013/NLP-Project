from __future__ import print_function
import os
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier
from nltk.classify import MaxentClassifier

#region Tokenizing, Stemming and Bigram finder and scores
def extract_words(text):
    # For English, although Porter Stemmer is not good
    # Replace it with morpha (Lemmatizer)
    stemmer = PorterStemmer()
    tokenizer = WordPunctTokenizer()
    tokens = set(tokenizer.tokenize(text))
    print("tokens : \n-------------")
    print(tokens)
    '''Finding collocations requires first calculating the frequencies of words and
    their appearance in the context of other words. Often the collection of words
    will then requiring filtering to only retain useful content terms. Each ngram
    of words may then be scored according to some association measure, in order
    to determine the relative likelihood of each ngram being a collocation.
    
    The ``BigramCollocationFinder`` and ``TrigramCollocationFinder`` classes provide
    these functionalities, dependent on being provided a function which scores a
    ngram given appropriate frequency counts. A number of standard association
    measures are provided in bigram_measures and trigram_measures.
    '''
    bigram_finder = BigramCollocationFinder.from_words(tokens)
    print("Bigram finder : \n--------------------")
    print(bigram_finder)

    #Scores for bigram tokens
    bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 500)
    for bigram_tuple in bigrams:
        x = "%s %s" % bigram_tuple
        tokens.add(x)
    result = [stemmer.stem(x.lower()) for x in tokens
              if len(x) > 1]
    return result
#endregion

#region Get words in dic
def get_feature(word):
    return dict([(word, True)])
#endregion

#region BOW
def bag_of_words(words):
    return dict([(word, True) for word in words])
#endregion

#region Get Training_Set
def get_train_set(texts):
    # Change to buffer `texts`
    train_set = []
    for sense, file in texts.items():
        print("training %s " % sense)
        text = open(file, 'r',encoding='utf-8').read()  # Change later
        features = extract_words(text)
        train_set = train_set + [(get_feature(word), sense) for word in features]
    return train_set
#endregion

#region Classifying
def Language_Identification(text, classifier):

    tokens = bag_of_words(extract_words(text))
    # printing what is the probability that entered sentence are related to => langugae
    print(classifier.prob_classify(tokens).prob('en'),"==>en")
    print(classifier.prob_classify(tokens).prob('es'),"==>es")
    print(classifier.prob_classify(tokens).prob('fr'),"==>fr")
    print (classifier.prob_classify(tokens).prob ('ge'), "==>ge")
    print (classifier.prob_classify(tokens).prob ('ar'), "==>ar")
    print(classifier.prob_classify(tokens).prob('franko'),"==>franko")

    # classifying the entered sentence
    decision = classifier.classify(tokens)
    return decision
#endregion

#region Classifying file
def File_Language_Identification(filename, classifier):
    decision = []
    with open(filename,'r',encoding="UTF-8") as f :
        sentences = f.readlines()

    print(sentences)
    for text in sentences:
        tokens = bag_of_words(extract_words(text))
        # printing what is the probability that entered sentence are related to => langugae
        print(classifier.prob_classify(tokens).prob('en'),"==>en")
        print(classifier.prob_classify(tokens).prob('es'),"==>es")
        print(classifier.prob_classify(tokens).prob('fr'),"==>fr")
        print (classifier.prob_classify(tokens).prob ('de'), "==>ge")
        print (classifier.prob_classify(tokens).prob ('ar'), "==>ar")
        print(classifier.prob_classify(tokens).prob('franko'),"==>franko")

        # classifying the entered sentence
        language = classifier.classify(tokens)
        decision.append((text,language))

    return decision
#endregion

#region Prepare the classifier
def Main(string , classifier_name):
    domain = "text"
    #classifier_name = "MaxEntropy"
    #classifier_name = "NaiveBayes"

    texts = {}
    pickled_classifier = r'E:\NLP_Project\language_identification_classifier-%s.%s.pickle' % (classifier_name, domain)

    if not os.path.exists (pickled_classifier):
        texts['en'] = 'en.txt'
        texts['es'] = 'es.txt'
        texts['fr'] = 'fr.txt'
        texts['ar'] = 'ar.txt'
        texts['ge'] = 'de.txt'
        texts['franko'] = 'franko.txt'

        print ("Training on Files", texts)
        print ("Will be pickling", pickled_classifier)

        train_set = get_train_set (texts)
        if (classifier_name == "MaxEntropy"):
            classifier = MaxentClassifier.train(train_set,max_iter=4)
        else:
            classifier = NaiveBayesClassifier.train (train_set)

        pickle.dump (classifier, open (pickled_classifier, 'wb'))
    else:
        classifier = pickle.load (open (pickled_classifier, "rb"))

    return File_Language_Identification(string, classifier)
#endregion
































