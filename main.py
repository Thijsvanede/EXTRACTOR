from preprocessings  import *
from role_generator  import *
from graph_generator import *


import argformat
import argparse

# Parse arguments
parser = argparse.ArgumentParser(
    formatter_class = argformat.StructuredFormatter,
)

# Optional arguments
parser.add_argument('--asterisk'  , type=str, default='true', help='asterisk task')
parser.add_argument('--crf'       , type=str, default='true', help='crf task')
parser.add_argument('--rmdup'     , type=str, default='true', help='remove duplicate task')
parser.add_argument('--elip'      , type=str, default='false', help='ellipsis resolution')
parser.add_argument('--gname'     , type=str, default='graph', help='graph name')
parser.add_argument('--input_file', type=str, help='input file')

# Parse arguments
args = parser.parse_args()

if __name__ == "__main__":

    txt = modification_()
    txt = txt.strip()
    txt = colon_seprator_multiplication(txt)
    txt = re.sub(' +', ' ', txt)
    sentences_ = sent_tokenize(txt)
    lst = roles(sentences_)
    lst = fix_srl_spacing(lst)
    all_nodes = negation_clauses(lst)
    if args.asterisk == 'true':
        all_nodes = astriks(all_nodes)
        all_nodes = triplet_builder(all_nodes)
    else:
        all_nodes = triplet_builder(all_nodes)
    all_nodes = remove_no_sub(all_nodes)
    lst = remove_c_colon_toprevent_graphvizbug(all_nodes)
    for i in lst:
        if "\\'" in i:
            i.replace("\\'", "'")
    if args.rmdup == "true":
        lst = rm_duplictes(lst)
        graph_builder(lst)
    else:
        graph_builder(lst)
