# Imports
import argformat
import argparse
import re
import signal
import spacy
from nltk import sent_tokenize

# Imports from package
import graph_generator
import preprocessing
import role_generator
import tokenizer

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
    parser.add_argument('--fpath'   , type=str, default='./Data/lists.ini', help='path to lists')

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

    from lists_patterns import load_lists

    # Load lists
    loaded_lists = load_lists(args.fpath)
    titles_list  = loaded_lists['MS_TITLES']
    main_verbs   = loaded_lists['verbs'    ]


    # Load NLP module
    nlp = spacy.load('en_core_web_lg')

    ########################################################################
    #                        Tokenizer preparation                         #
    ########################################################################

    # Remove obsolete text
    text = tokenizer.delete_brackets(text)
    text = text.strip(" ")

    # Tokenize text
    text = tokenizer.sentence_tokenizer(
        tokenizer.removable_token(text, loaded_lists),
        titles_list,
        nlp,
        main_verbs,
    )

    ########################################################################
    #                      Preprocessing preparation                       #
    ########################################################################

    print("Start preprocessing")

    # TODO - move load somewhere else?
    signal.signal(signal.SIGSEGV, preprocessing.SIGSEGV_signal_arises)

    print("------------communicate ---------------")
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
        text = preprocessing.ellipsis_subject(text, nlp, loaded_lists)
        print("ellipsis_subject", len(text), text)

    print('------------ coref_the_following_colon ------------')
    out = preprocessing.coref_the_following_colon(text, loaded_lists)

    for i,val in enumerate(tokenizer.sent_tokenize(out)):
        print(i,val)

    print('------------ coref_the_following_middle ------------')

    midle = preprocessing.coref_the_following_middle(out, loaded_lists)

    for i,val in enumerate(tokenizer.sent_tokenize(midle)):
        print(i,val)

    out_translate = preprocessing.translate_obscure_words(out)
    print("*****homogenization:", preprocessing.homogenization(out_translate))
    homo = preprocessing.homogenization(out_translate)
    comm = preprocessing.communicate_to_sr(homo, loaded_lists)
    print(comm)
    cc = preprocessing.CـC(comm, loaded_lists)
    print("------------ modification ---------------")


    print('----Preprocessed:----')
    for i,val in enumerate(tokenizer.sent_tokenize(preprocessing.modification_(cc, loaded_lists))):
        print(i,val)

    print("End preprocessing")

    text = preprocessing.modification_(cc, loaded_lists)
    text = text.strip()
    text = role_generator.colon_seprator_multiplication(text, loaded_lists)
    text = re.sub(' +', ' ', text)
    sentences_ = sent_tokenize(text)
    lst = role_generator.roles(sentences_, nlp, main_verbs)
    lst = role_generator.fix_srl_spacing(lst)
    all_nodes = role_generator.negation_clauses(lst)
    if args.asterisk == 'true':
        all_nodes = role_generator.astriks(all_nodes, loaded_lists)
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
