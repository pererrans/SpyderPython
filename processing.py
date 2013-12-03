#Mariana Matus
#Parser for data from Stack Exchange

#Import libraries
import sys, re
import logging, gensim, bz2
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler('infolog.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

from gensim import corpora, models, similarities
from gensim.corpora import TextCorpus, MmCorpus, Dictionary

#############################

def makeList(fileobject):
    #Input: fileobject
    #Output: a dictionary of sequences, with sequence names as keys and sequences (strings, all upper-case) as values
    documents = fileobject.readlines()
    fileobject.close()
#    print documents[0]
#    print len(documents)
            
    return documents




#######################
def main():  
    #Check for errors in reading input sequence
    try:
        f = open('title_question_nostop_filteredwords.txt', 'r')
#        f = open('C:\Users\pererrans\Dropbox\final_projectReal\Data\title_question_nostop_filteredwords.txt')
    except IOError:
        print "Error: Could not open file:", sys.argv[1]
        print "Please check file exists in the current directory and you have permission to read it."
        sys.exit() 
    except IndexError:
        print "Usage: python", sys.argv[0], "[input]"
        sys.exit()
    
    #Read lines from file and store them as a list 
    #Input is already filtered for infrequent words (appearing in 3 docs or fewer)
    documents = makeList(f)
#    logger.info("Document made. First entry: %s /n length is %d documents", documents[0], len(documents))

    #Remove common words and tokenize
    #i appears in many topics so is also removed as a common word
    stoplist = set('for a of the and to in i is it that have on this with be are my'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
            for document in documents]
    #remove empty tokens
    #
            
    # create dictionary from the texts
    dictionary = corpora.Dictionary(texts)
    dictionary.save('dictionary.dict')
#    dictionary = corpora.Dictionary.load('dictionary.dict')  
    print dictionary
    logger.info("dict done")  
    
    #create corpus
    mycorpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('mycorpus.mm', mycorpus)
#    mycorpus = corpora.MmCorpus('mycorpus.mm')
    logger.info("length of corpus exist? %s length %d", mycorpus, len(mycorpus)) 
    logger.info("corpus done")
    
    ## Build LDA models with different numbers of topics  
#    numtopics = [5,10,20,30,50]
    numtopics = [50]
    for k in numtopics:    
        lda = gensim.models.ldamodel.LdaModel(corpus=mycorpus, id2word=dictionary, num_topics=k)    
        lda.save('myldamodel'+str(k))
    #    gensim.models.ldamodel.LdaModel.load('myldamodel50') 
        logger.info("LDA with %d topics done", k)
    #    lda.show_topics(topics=-1, topn=10, log=True, formatted=False)
        logfile = open(str(k)+'topics.txt', 'w')
        print>>logfile, lda.show_topics(topics=-1, topn=10, formatted=False)


    
main()