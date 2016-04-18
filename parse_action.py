#idea: every time a new word has been seen, add a new rule for it to the grammar
import nltk
from nltk import grammar, parse

words_seen = []
GRAMMARSTR = """
% start S
S[SUB=?sub, VERB=?verb, OBJ=?obj, DAT=?dat] -> NP[N=?sub] VP[V=?verb, N=?obj, DAT=?dat]
VP[V=?verb, N=?obj] -> NNS[SEM=?verb] NP[N=?obj] 
VP[V=?verb, N=?obj, DAT=?dat] -> VP[V=?verb, N=?obj] PP[DAT=?dat]
NP[N=?np] -> NN[SEM=?np] 
NP[N=<?jj(?nn)>] -> JJ[SEM=?jj] NN[SEM=?nn] 
NP[N=?np] -> VBP[SEM=?np]
PP[DAT=?np] -> IN[SEM=with] NP[N=?np]
IN[SEM=with] -> with
"""
GRAMMAR = grammar.FeatureGrammar.fromstring(GRAMMARSTR)
PARSER = parse.FeatureEarleyChartParser(GRAMMAR)

def add_to_grammar(rules):
    '''
    This function adds in new rules for the grammar.
    '''
    global GRAMMARSTR
    global PARSER
    for rule in rules:
        GRAMMARSTR += '\n' + rule
    GRAMMAR = grammar.FeatureGrammar.fromstring(GRAMMARSTR)
    PARSER = parse.FeatureEarleyChartParser(GRAMMAR)

def parse_sentence(sentence):
    '''
    This function will parse an action desribed in a plain sentence
    For example, the sentence "frog kill princess" should yield
    S[OBJ='frog', SUB='princess', VERB='kill']
    '''
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    #try to extract semantics
    new_rules = set()
    for t in tagged:
        if t not in words_seen:
            #new_t = t[1]+"[SEM="+t[0]+"] -> '"+t[0]+"'"
            new_t = make_rule(t)
            new_rules.add(new_t)
            words_seen.append(t)
            print new_t
    add_to_grammar(new_rules)
    trees = PARSER.parse(tokens)
    return trees.next().label()

def make_rule(tag):
    if tag[1] == 'JJ':
        return "JJ[SEM=<\\x."+tag[0]+"(x)>] -> '"+tag[0]+"'"
    else:
        return tag[1]+"[SEM="+tag[0]+"] -> '"+tag[0]+"'"

if __name__ == "__main__":
    sentences = []
    #sentences.append("princess kills frog")
    #sentences.append("princess kills frog with magic")
    #sentences.append("caliph buys magic powder")
    sentences.append("magic powder")
    for s in sentences:
        print s
        p = parse_sentence(s)
        print p
