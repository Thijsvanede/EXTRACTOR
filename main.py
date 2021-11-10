# Imports
import argformat
import argparse
import re
import signal
from nltk import sent_tokenize

# Imports from package
import graph_generator
import preprocessing
import role_generator
import tokenizer

# Load NLP module
import spacy
nlp = spacy.load('en_core_web_lg')


if __name__ == "__main__":

    ########################################################################
    #                           Parse arguments                            #
    ########################################################################

    # Parse arguments
    parser = argparse.ArgumentParser(
        formatter_class = argformat.StructuredFormatter,
    )

    # Required arguments
    parser.add_argument('input_file', type=str, help='input file')

    # Optional arguments
    parser.add_argument('--asterisk', type=str, default='true' , help='asterisk task')
    parser.add_argument('--crf'     , type=str, default='true' , help='crf task')
    parser.add_argument('--rmdup'   , type=str, default='true' , help='remove duplicate task')
    parser.add_argument('--elip'    , type=str, default='false', help='ellipsis resolution')
    parser.add_argument('--gname'   , type=str, default='graph', help='graph name')

    # Parse arguments
    args = parser.parse_args()

    ########################################################################
    #                              Load data                               #
    ########################################################################

    # Load input file
    with open(args.input_file, encoding='iso-8859-1') as input_file:
        text = input_file.readlines()
        text = " ".join(text)
        text = text.replace('\n', ' ')


    from lists_patterns import load_lists, fpath

    # Load lists
    loaded_lists = load_lists(fpath)

    ########################################################################
    #                        Tokenizer preparation                         #
    ########################################################################

    titles_list = loaded_lists['MS_TITLES']
    titles_list = titles_list.replace("'", "").strip('][').split(', ')
    main_verbs  = loaded_lists['verbs']
    main_verbs  = main_verbs.replace("'", "").strip('][').split(', ')

    text = tokenizer.delete_brackets(text)
    text = text.strip(" ")

    all_sentences_list = tokenizer.removable_token(text)

    text_tokenized = tokenizer.sentence_tokenizer(all_sentences_list, titles_list, nlp, main_verbs)
    print("*****sentence_tokenizer:", len(tokenizer.sent_tokenize(text_tokenized)), tokenizer.sentence_tokenizer(all_sentences_list, titles_list, nlp, main_verbs))

    print("*****Tokenizer*****")

    for i,val in enumerate(tokenizer.sent_tokenize(text_tokenized)):
        print(i,val)


    print("End tokenizer")

    ########################################################################
    #                      Preprocessing preparation                       #
    ########################################################################

    print("Start preprocessing")

    # TODO - move load somewhere else?
    signal.signal(signal.SIGSEGV, preprocessing.SIGSEGV_signal_arises)

    print("------------communicate ---------------")
    text = tokenizer.sentence_tokenizer(all_sentences_list, titles_list, nlp, main_verbs)
    text = preprocessing.delete_brackets(text)
    text = preprocessing.pass2acti(text, nlp)
    text = re.sub(' +', ' ', text)
    print("*********8",text)

    if args.crf == 'true':
        text = preprocessing.coref_(text, nlp)
        print("coref_",len(text),text)
    else:
        text = preprocessing.wild_card_extansions(text)


    text = preprocessing.try_to(text)
    print("try_to__",text)
    text = preprocessing.is_capable_of(text)

    if args.elip == 'true':
        text = preprocessing.replcae_surrounding_subject(text)
    else:
        print("is capble of__",text)
        text = preprocessing.ellipsis_subject(text, nlp)
        print("ellipsis_subject", len(text), text)

    print('------------ coref_the_following_colon ------------')
    out = preprocessing.coref_the_following_colon(text)

    for i,val in enumerate(tokenizer.sent_tokenize(out)):
        print(i,val)

    print('------------ coref_the_following_middle ------------')

    midle = preprocessing.coref_the_following_middle(out)

    for i,val in enumerate(tokenizer.sent_tokenize(midle)):
        print(i,val)

    out_translate = preprocessing.translate_obscure_words(out)
    print("*****homogenization:", preprocessing.homogenization(out_translate))
    homo = preprocessing.homogenization(out_translate)
    comm = preprocessing.communicate_to_sr(homo)
    print(comm)
    cc = preprocessing.CـC(comm)
    print("------------ modification ---------------")


    print('----Preprocessed:----')
    for i,val in enumerate(tokenizer.sent_tokenize(preprocessing.modification_(cc))):
        print(i,val)

    print("End preprocessing")

    text = preprocessing.modification_(cc)
    text = text.strip()
    text = role_generator.colon_seprator_multiplication(text)
    text = re.sub(' +', ' ', text)
    sentences_ = sent_tokenize(text)
    lst = role_generator.roles(sentences_, nlp)
    lst = role_generator.fix_srl_spacing(lst)
    all_nodes = role_generator.negation_clauses(lst)
    if args.asterisk == 'true':
        all_nodes = role_generator.astriks(all_nodes)
        all_nodes = role_generator.triplet_builder(all_nodes)
    else:
        all_nodes = role_generator.triplet_builder(all_nodes)
    all_nodes = graph_generator.remove_no_sub(all_nodes)
    lst = graph_generator.remove_c_colon_toprevent_graphvizbug(all_nodes)
    for i in lst:
        if "\\'" in i:
            i.replace("\\'", "'")
    if args.rmdup == "true":
        lst = graph_generator.rm_duplictes(lst)
        graph_generator.graph_builder(lst, args.gname)
    else:
        graph_generator.graph_builder(lst, args.gname)
