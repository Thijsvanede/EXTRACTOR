# EXTRACTOR
EXTRACTOR helps to extract the system level attack behavior from unstructured threat reports. The extracted attack behavior will be represented in form of directed graphs, where the nodes represent system entities and edges represent system calls. EXTRACTOR leverages Natural Language Processing (NLP) techniques to transform a raw threat report into a graph representation.

---
**NOTE**

This repository is a rework of the original implementation of EXTRACTOR [[PDF]](https://arxiv.org/abs/2104.08618), **original source code:** https://github.com/ksatvat/EXTRACTOR.
The aim is to make the code run quicker and be easier to extend for future research.

---


## Instructions
### Requirements

This repository uses `python 3.5+` and has the following requirements:
```
nltk == 3.4.5
spaCy == 2.1.0
allennlp == 0.8.4
neuralcoref == 4.0.0
graphviz == 0.13.2
textblob == 0.15.3
pattern == 3.6
numpy == 1.18.1
```
You can directly install the requirements using `pip install -r requirements.txt`

In addition to the required packages, please also install the following modules:
```bash
# en_core_web_lg
python3 -m spacy download en_core_web_lg
```

```python
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
```

```bash
wget -c -t 0 https://s3-us-west-2.amazonaws.com/allennlp/models/srl-model-2018.05.25.tar.gz
mv srl-model-2018.05.25.tar.gz srl-model.tar.gz
```

```bash
sudo apt install graphviz
```

### Usage

Run EXTRACTOR with `python3 main.py [-h] [--asterisk ASTERISK] [--crf CRF] [--rmdup RMDUP] [--elip ELIP] [--gname GNAME] [--input_file INPUT_FILE]`.

Depending on the usage, each argument helps to provide a different representation of the attack behavior.
`[--asterisk true]` creates abstraction and can be used to replace anything that is not perceived as IOC/system entity into a wild-card. This representation can be used to be searched within the audit-logs.  

`[--crf true/false]` allows activating or deactivating of the co-referencing module.

`[--rmdup true/false]` enables removal of duplicate nodes-edge.

`[--elip true/false]` is to choose whether to replace ellipsis subjects using the surrounding subject or not.

`[--input_file path/filename.txt]` is to pass the text file to the application.

`[--gname graph_name]` is to specify the name output graph (two files will be created, e.g., graph.pdf and graph.dot).

#### Example
`python3 main.py --asterisk true --crf true --rmdup true --elip true --input_file input.txt --gname mygraph`

## Summarizer
To perform the prediction/text summarization, you need to first convert the `txt` file to the required format `tsv` using `python3 txt2tsv.py`.


### Prediction
To do the extractive summarization, run `python3 prediction.py`
