import nltk
import sys
import os
from string import punctuation
from numpy import log as ln
from heapq import nlargest

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}

    for file in os.listdir(directory):
        if file.endswith('.txt'):
            path = os.path.join(directory, file)
            
            # read contents of file and store into dictionary
            f = open(path, encoding='utf-8')
            contents = f.read()

            files[file] = contents

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # tokenize sentence and convert all characters to lowercase
    words = [word.lower() for word in nltk.word_tokenize(document)]

    # filter out punctuations
    puncs = set(punctuation)
    words = [word for word in words if not all(c in puncs for c in word)]

    # filter out stopwords
    words = list(filter(lambda word: word not in nltk.corpus.stopwords.words('english'), words))  

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}

    for doc in documents:
        for word in documents[doc]:
            
            # skip words that have been added
            if word in idfs:
                continue
                
            # add the new word to idfs dictionary
            idfs[word] = 0
            
            # count the number of documents in which the word appears
            for d in documents:
                if word in documents[d]:
                    idfs[word] += 1
    
    # calculate IDF values for each word
    nDocs = len(documents)
    for word in idfs:
        idfs[word] = ln(nDocs / idfs[word])

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = {}

    for file in files:
        tf_idfs[file] = 0

        for word in query:
            # get term frequency of this word in this file
            tf = files[file].count(word)

            # add the tf-idf value of this word to the file's tf-idf sum
            if tf > 0:
                tf_idfs[file] += tf * idfs[word]

    # rank by tf-idf values
    return nlargest(n, tf_idfs, key=tf_idfs.get)


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranking_values = {}

    for sen in sentences:
        # initialise sentence's IDF sum and QTD (query term density)
        ranking_values[sen] = {'idf': 0, 'qtd': 0}

        for word in query:
            if word in sentences[sen]:
                # if word in query is in sentence, add to IDF and QTD accordingly
                ranking_values[sen]['idf'] += idfs[word]
                ranking_values[sen]['qtd'] += 1

        # calculate query term density
        ranking_values[sen]['qtd'] /= len(sentences[sen])

    # rank by IDF values, then QTD if sentences have the same IDFs
    return nlargest(n, ranking_values, key=lambda s: (ranking_values[s]['idf'], ranking_values[s]['qtd']))


if __name__ == "__main__":
    main()
