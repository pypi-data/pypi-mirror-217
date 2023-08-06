# Basic stuff
from termcolor import colored
from .utils import *
import time
# Word2Vec
from gensim.models import Word2Vec
# File stuff
from pickle import dump,load
from os.path import exists
from os import mkdir
import gzip


def load_word2vec_model(session, w2v_vector_size, rebuild, stopwords, verbose=1):
    """
    Builds a word2vec model, or loads a previously built model.

    Args:
        session: Session object (created in load_data())
        w2v_vector_size (int): Size of word vectors
        rebuild (bool): Set to True if force rebuild word2vec model
        stopwords (str, list or None): Lists of stopwords to be used for text pre-processing. Can be either languages (from the nltk.corpus package) or paths to csv files, for example ['english', 'data/custom_stopwords.csv']. If None, no stopwords will be used (default: None)
        verbose (int): Set verbose (output messages) level (0 for no output messages) (default: 1)
        
    Returns:
        Word2vec model
    """
    
    # Check if path exists
    fpath = "word2vec"
    if not exists(fpath):
        mkdir(fpath)
    
    # Filename
    fname = session["file"]
    fname = fname[fname.rfind("/")+1:]
    fname = fname.replace(".csv","").replace(".gz","") + f"_{w2v_vector_size}.w2v"
    
    # Check if stored
    if exists(f"word2vec/{fname}") and not rebuild:
        wtovec = load(gzip.open(f"word2vec/{fname}", "rb"))
        if verbose >= 1:
            info("Word2vec model loaded from " + colored(f"word2vec/{fname}", "cyan"))
        return wtovec
    
    # Stopwords
    sw = load_stopwords(stopwords, verbose=verbose)
    if sw is None:
        sw = set()
    else:
        sw = set(sw)
    
    # Convert to list of list of words
    X = []
    for wds in session["X"]:
        xi = []
        for w in wds.split(" "):
            if w not in sw and w.strip() != "":
                xi.append(w)
        X.append(xi)
        
    # Train Word2Vec model
    start = time.time()
    model = Word2Vec(X, vector_size=w2v_vector_size, min_count=1)

    # Generate dict for each word
    vectors = model.wv
    words = list(model.wv.key_to_index.keys())
    wtovec = {}
    for i in range(0,len(vectors)):
        wtovec.update({words[i]: vectors[i]})

    # Done
    end = time.time()
    if verbose >= 1:
        info("Word2vec model generated in " + colored(f"{end-start:.2f}", "blue") + " sec")

    # Store model
    dump(wtovec, gzip.open(f"word2vec/{fname}", "wb"))
    if verbose >= 1:
        info("Word2vec model stored to " + colored(f"word2vec/{fname}", "cyan"))

    return wtovec


def load_word2vec_data(session, w2v_vector_size, rebuild, stopwords, verbose=1):
    """
    Loads and pre-processes word2vec vectors for the loaded text data.

    Args:
        session: Session object (created in load_data())
        w2v_vector_size (int): Size of word vectors
        rebuild (bool): Set to True if force rebuild word2vec model
        stopwords (str, list or None): Lists of stopwords to be used for text pre-processing. Can be either languages (from the nltk.corpus package) or paths to csv files, for example ['english', 'data/custom_stopwords.csv']. If None, no stopwords will be used (default: None)
        verbose (int): Set verbose (output messages) level (0 for no output messages) (default: 1)
        
    Returns:
        Word2vec word vectors data
    """
    
    # Check if path exists
    fpath = "word2vec"
    if not exists(fpath):
        mkdir(fpath)

    # Filename
    fname = session["file"]
    fname = fname[fname.rfind("/")+1:]
    fname = fname.replace(".csv","").replace(".gz","") + f"_{w2v_vector_size}.emb"
    
    # Check if stored
    if exists(f"word2vec/{fname}") and not rebuild:
        obj = load(gzip.open(f"word2vec/{fname}", "rb"))
        if verbose >= 1:
            info("Word2vec embeddings loaded from " + colored(f"word2vec/{fname}", "cyan"))
        session["X"] = obj[0]
        session["y"] = obj[1]
        return
    
    # Get Word2Vec model
    wtovec = load_word2vec_model(session, w2v_vector_size=w2v_vector_size, rebuild=rebuild, stopwords=stopwords, verbose=verbose)
    
    # Generate new word vectors
    start = time.time()
    X = []
    y = []
    for xi,yi in zip(session["X"], session["y"]):
        vec = [0] * w2v_vector_size
        nn = 0
        for w in xi.split(" "):
            # Add vectors for each word
            if w.strip() != "" and w in wtovec:
                vec = [x1+x2 for x1,x2 in zip(vec,wtovec[w])]
                nn += 1
        if nn > 0:
            # Calculate mean values for the word vectors
            vec = [x/nn for x in vec]
            X.append(vec)
            y.append(yi)
            
    # Update data
    session["X"] = X
    session["y"] = y
    
    # Done
    end = time.time()
    if verbose >= 1:
        info("Word2vec embeddings generated in " + colored(f"{end-start:.2f}", "blue") + " sec")

        
def word_vector(xi, session):
    """
    Creates a word vector for an example.

    Args:
        xi: The example of text data
        session: Session object (created in load_data())
        
    Returns:
        Word2vec vector for the example
    """
    
    # Get vector size
    if type(session["X"][0]) == list:
        size = len(session["X"][0])
    else:
        size = session["X"][0].shape[1]
        
    # Get Word2Vec model
    wtovec = load_word2vec_model(session, w2v_vector_size=size, rebuild=False, stopwords=None, verbose=0)
    
    # Generate new word vectors
    vec = [0] * size
    for w in xi.lower().split(" "):
        # Add vectors for each word
        if w.strip() != "" and w in wtovec:
            vec = [x1+x2 for x1,x2 in zip(vec,wtovec[w])]
    return vec
    