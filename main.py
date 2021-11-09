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

if __name__ == "__main__":

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
