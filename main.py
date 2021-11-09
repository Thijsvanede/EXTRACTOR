# Imports
import argformat
import argparse
import re
from nltk import sent_tokenize

# Imports from package
import preprocessing
import role_generator
import graph_generator

# Load NLP module
import spacy
nlp = spacy.load('en_core_web_lg')

# Parse arguments
parser = argparse.ArgumentParser(
    formatter_class = argformat.StructuredFormatter,
)

# Optional arguments
parser.add_argument('--asterisk', type=str, default='true', help='asterisk task')
parser.add_argument('--crf'     , type=str, default='true', help='crf task')
parser.add_argument('--rmdup'   , type=str, default='true', help='remove duplicate task')
parser.add_argument('--elip'    , type=str, default='false', help='ellipsis resolution')
parser.add_argument('--gname'   , type=str, default='graph', help='graph name')
parser.add_argument('input_file', type=str, help='input file')

# Parse arguments
args = parser.parse_args()



def prepare_tokenizer(input_file):

    import tokenizer
    from lists_patterns import load_lists, fpath

    ################################################################################
    #                      Stuff that should be moved to main                      #
    ################################################################################

    # Load input file
    with open(input_file, encoding='iso-8859-1') as input_file:
        txt = input_file.readlines()
        txt = " ".join(txt)
        txt = txt.replace('\n', ' ')

    # Load lists
    loaded_lists = load_lists(fpath)

    titles_list = loaded_lists['MS_TITLES']
    titles_list = titles_list.replace("'", "").strip('][').split(', ')
    main_verbs = loaded_lists['verbs']
    main_verbs = main_verbs.replace("'", "").strip('][').split(', ')

    txt = tokenizer.delete_brackets(txt)
    txt = txt.strip(" ")

    all_sentences_list = tokenizer.removable_token(txt)

    txt_tokenized = tokenizer.sentence_tokenizer(all_sentences_list, titles_list, nlp, main_verbs)
    print("*****sentence_tokenizer:", len(tokenizer.sent_tokenize(txt_tokenized)), tokenizer.sentence_tokenizer(all_sentences_list, titles_list, nlp, main_verbs))

    print("*****Tokenizer*****")

    for i,val in enumerate(tokenizer.sent_tokenize(txt_tokenized)):
        print(i,val)


    print("End tokenizer")


def prepare_preprocessing():
    ################################################################################
    #                             TODO - move to main?                             #
    ################################################################################

    print("Start preprocessing")

    # TODO - move load somewhere else?
    signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)

    print("------------communicate ---------------")
    txt = sentence_tokenizer()
    txt = delete_brackets(txt)
    txt = pass2acti(txt)
    txt = re.sub(' +', ' ', txt)
    print("*********8",txt)

    import main
    from main import nlp

    if main.args.crf == 'true':
        txt = coref_(txt, nlp)
        print("coref_",len(txt),txt)
    else:
        txt = wild_card_extansions(txt)


    txt = try_to(txt)
    print("try_to__",txt)
    txt = is_capable_of(txt)

    if main.args.elip == 'true':
        txt = replcae_surrounding_subject(txt)
    else:
        print("is capble of__",txt)
        txt = ellipsis_subject(txt, nlp)
        print("ellipsis_subject", len(txt), txt)

    print('------------ coref_the_following_colon ------------')
    out = coref_the_following_colon(txt)

    for i,val in enumerate(sent_tokenize(out)):
        print(i,val)

    print('------------ coref_the_following_middle ------------')

    midle = coref_the_following_middle(out)

    for i,val in enumerate(sent_tokenize(midle)):
        print(i,val)

    out_translate = translate_obscure_words(out)
    print("*****homogenization:",homogenization(out_translate))
    homo = homogenization(out_translate)
    comm = communicate_to_sr(homo)
    print(comm)
    cc = CـC(comm)
    print("------------ modification ---------------")


    print('----Preprocessed:----')
    for i,val in enumerate(sent_tokenize(modification_())):
        print(i,val)

    print("End preprocessing")






if __name__ == "__main__":

    print("Prepare tokenizer")
    prepare_tokenizer(args.input_file)
    prepare_preprocessing()
    exit()

    txt = preprocessing.modification_()
    txt = txt.strip()
    txt = role_generator.colon_seprator_multiplication(txt)
    txt = re.sub(' +', ' ', txt)
    sentences_ = sent_tokenize(txt)
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
        graph_generator.graph_builder(lst)
    else:
        graph_generator.graph_builder(lst)
