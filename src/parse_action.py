#idea: every time a new word has been seen, add a new rule for it to the grammar
import nltk
from nltk import grammar, parse

words_seen = ['a', 'an', 'with', 'for', 'to', 'the', 'into', 'and']
GRAMMARSTR = """
% start S
S[SUB=?sub, VERB=?verb, OBJ=?obj, DAT=?dat] -> NP[N=?sub] VP[V=?verb, N=?obj, DAT=?dat]
VP[V=?verb] -> VERB[SEM=?verb]
VP[V=?verb, N=?obj] -> VERB[SEM=?verb] NP[N=?obj] 
VP[V=?verb, N=?obj, DAT=?dat] -> VP[V=?verb, N=?obj] PP[DAT=?dat]
VP[V=?verb, N=?obj, DAT=?dat] -> VP[V=?verb, N=?obj] SUBCL[DAT=?dat]
NP[N=?np] -> IN[SEM=<about>] PropNP[N=?np]
NP[N=?np] -> TO[SEM=<to>] PropNP[N=?np]
NP[N=?np] -> PropNP[N=?np]
NP[N=<?and(?np1)(?np2)>] -> PropNP[N=?np1] CC[SEM=?and] NP[N=?np2]
PropNP[N=?np] -> NN[SEM=?np]
PropNP[N=?np]-> DT[SEM=?dt] NN[SEM=?np]
PropNP[N=?np]-> DT[SEM=?dt] JJ[SEM=?np]
PropNP[N=?np] -> VBP[SEM=?np]
PropNP[N=?np] -> VBN[SEM=?np]
PP[DAT=?np] -> IN[SEM=<with>] NP[N=?np]
PP[DAT=?np] -> IN[SEM=<for>] NP[N=?np]
PP[DAT=?np] -> IN[SEM=<into>] NP[N=?np]
SUBCL[DAT=?np] -> TO[SEM=<to>] NP[N=?np]
VERB[SEM=?verb] -> V[SEM=?verb]
VERB[SEM=?verb] -> V[SEM=?verb] IN[SEM=<into>]
V[SEM=?verb] -> VBZ[SEM=?verb]
DT[SEM=<a>] -> 'a'
DT[SEM=<a>] -> 'an'
IN[SEM=<with>] -> 'with'
IN[SEM=<for>] -> 'for'
IN[SEM=<about>] -> 'about'
TO[SEM=<to>]-> 'to'
DT[SEM=<the>] -> 'the'
IN[SEM=<into>] -> 'into'
CC[SEM=<\\x.(\\y.(x & y))>] -> 'and'
"""
#stuff that doesn't work yet
"""
NP[N=<?jj(?nn)>] -> JJ[SEM=?jj] NN[SEM=?nn] 
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
    #tokens = nltk.word_tokenize(sentence)
    tokens = sentence.split()
    tagged = nltk.pos_tag(tokens)
    #print tagged
    #try to extract semantics
    new_rules = set()
    for t in tagged:
        print t
        if t[0] not in words_seen:
            #new_t = t[1]+"[SEM="+t[0]+"] -> '"+t[0]+"'"
            new_t = make_rule(t)
            new_rules.add(new_t)
            words_seen.append(t)
    add_to_grammar(new_rules)
    trees = PARSER.parse(tokens)
    parse_result = trees.next().label()
    parse_result = parse_result.remove_variables()
    for k in parse_result:
        if isinstance(k, unicode):
            parse_result[k] = str(parse_result[k])
            print parse_result[k]
    return parse_result

def make_rule(tag):
    """
    if tag[1] == 'JJ':
        return "JJ[SEM=<\\x."+tag[0]+"(x)>] -> '"+tag[0]+"'"
    else:
        return tag[1]+"[SEM=<"+tag[0]+">] -> '"+tag[0]+"'"
    """
    return tag[1]+"[SEM=<"+tag[0]+">] -> '"+tag[0]+"'"

if __name__ == "__main__":
    sentences = []
    #sentences.append("the princess kills the frog")
    #sentences.append("the princess and the king and the caliph kills the frog")
    #sentences.append("princess kills frog with magic")
    #sentences.append("caliph buys magic powder")
    #sentences.append("the frog transforms into a human")
    sentences.append("the caliph transforms into an animal")
    for s in sentences:
        print s
        p = parse_sentence(s)
        print p
