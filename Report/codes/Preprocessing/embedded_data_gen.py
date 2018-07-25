from __future__ import division
import pickle
import numpy as np
import pdb
import gensim

#For sentences in 10-15
#no_train = 15000
#no_test = 500

#For sentences in 20-25
no_train = 20000
no_test = 1000
embedding_size = 300


#####################
## Gensim Word2Vec ##
#####################

from gensim.models import Word2Vec

model = gensim.models.KeyedVectors.load_word2vec_format('../../GoogleNews-vectors-negative300.bin', binary=True)
model1 = gensim.models.KeyedVectors.load_word2vec_format('../../google_finetuned.bin', binary=True)

print("Loading Word2Vec done ...")

dirlist = ["train","test"]
predir = "../../Data/refined_"

for direc in dirlist:

    if direc == "train":
        thresh = no_train
    else:
        thresh = no_test

    with open(predir+direc+"_sentence.txt","rb") as fp:
        sentence = pickle.load(fp)

    with open(predir+direc+"_compressed_sentence.txt","rb") as fp:
        compressed_sentence = pickle.load(fp)

    with open(predir+direc+"_binary_output.txt","rb") as fp:
        bin_output = pickle.load(fp)


    #################################################
    ## To get the max sentence length in training. ##
    #################################################

    """
    max_len = len(bin_output[0])
    for i in range(len(bin_output)):
        if bin_output[i].shape[0] > max_len:
            max_len = bin_output[i].shape[0]
    print(max_len)
    """
    max_len = 25

    ###################################
    ## Generate train decoder output ##
    ###################################
    decoder_output = []
    for i in range(len(bin_output)):
        print("Decoder Output: ",i)
        if i < thresh:
            temp_bin = np.zeros((max_len,1))
            temp_bin[:bin_output[i].shape[0],0] = bin_output[i][:,0]
            decoder_output.append(temp_bin)
        else:
            break

    decoder_output = np.array(decoder_output)
    np.save(predir+direc+"_decoder_output.npy",decoder_output)
    print("decoder_output: ",decoder_output.shape)
    del decoder_output

    print('\n',direc," decoder output ......",'\n')


    ##################################
    ## Generate train encoder input ##
    ##################################
    
    if len(sentence) != len(bin_output):
        print("Kuch toh pain hai")

    encoder_input = np.zeros((thresh,max_len,embedding_size))
    for i in range(len(sentence)):
        print("Encoder Input: ",i)
        if i < thresh:
            sentence_em = []
            words_in_sentences = sentence[i].split()
            words_in_sentences = words_in_sentences[::-1]
            for j in range(max_len):
                word_em = np.zeros((1,embedding_size))
                if j < len(words_in_sentences):
                    try:
                        word_em = model[words_in_sentences[j]]
                        word_em = word_em/(np.sqrt(np.linalg.norm(word_em)))
                        #pdb.set_trace()
                    except:
                        yo=1
                        word_em = model1[words_in_sentences[j]]
                        word_em = word_em/(np.sqrt(np.linalg.norm(word_em)))
                encoder_input[i,j,:] = word_em
        else:
            break
    
    #encoder_input = np.array(encoder_input)
    np.save(predir+direc+"_encoder_input.npy",encoder_input)
    print("encoder_input: ",encoder_input.shape)
    del encoder_input

    print('\n',direc," encoder input ......",'\n')

    #pdb.set_trace()

    ##################################
    ## Generate train decoder input ##
    ##################################

    decoder_input = np.zeros((thresh,max_len,embedding_size))
    for i in range(len(sentence)):
        print("Decoder Input: ",i)
        if i < thresh:
            sentence_em = []
            words_in_sentences = sentence[i].split()
            for j in range(max_len):
                word_em = np.zeros((1,embedding_size))
                if j < len(words_in_sentences):
                    try:
                        word_em = model[words_in_sentences[j]]
                        word_em = word_em/(np.sqrt(np.linalg.norm(word_em)))
                    except:
                        yo=1
                        word_em = model1[words_in_sentences[j]]
                        word_em = word_em/(np.sqrt(np.linalg.norm(word_em)))
                decoder_input[i,j,:] = word_em
        else:
            break

    np.save(predir+direc+"_decoder_input.npy",decoder_input)
    print("decoder_input: ",decoder_input.shape)
    del decoder_input

    print("\n",direc," decoder input ......","\n")

pdb.set_trace()
    


