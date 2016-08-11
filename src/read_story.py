import parse_action
import story_db
import copy
import re

def learn_actions(state1, state2, actions):
    '''
    Learn the preconditions and effects of actions in a story
    '''
    differences = state_diff(state1, state2)
    print "actions: " + str(actions)
    print "differences: " + str(differences)
    rules = []
    for action in actions:
        if isinstance(action, list):
            continue
        a = copy.copy(action)
        #look for the words in the action in the state_diff
        rule = StoryRule(a["VERB"])
        #just to be safe, we don't want to substitute the verb, since this is 
        #the action
        del a["VERB"]
        for k in a:
            #sometimes words can be conjunctions. this is represented as
            #'(king & princess)'
            #here we transform these strings into python lists
            k_split = a[k].strip('()').split('&')
            a[k] = tuple([e.strip() for e in k_split])
        #invert the keys and values in a for ease of looking up the 
        #corresponding function
        #TODO: in a sentence where the same word has multiple functions
        #(e.g.: "dog bites dog") this could cause problems
        a_inv = {v: k for k, v in a.items()}
        #look at all nodes in a_inv and their neighbors (initially just for the first state)
        nodes_and_neighbors = set()
        for nodes in a_inv.keys():
            for node in nodes:
                nodes_and_neighbors.add(node)
                nodes_and_neighbors |= state1.neighbors(node)
        print "action: " + str(action)
        print "nodes_and_neighbors: " + str(nodes_and_neighbors)
        rule.actors = a
        #TODO add preconditions to the rule
        #find the relevant nodes (the ones contained in the "a" object) 
        #and the nodes they connect to
        relevant_edges = set()

        for node in nodes_and_neighbors:
            neighbors = state1.neighbors(node)
            relevant_edges |= set([(node, neighbor) for neighbor in neighbors])

        #substitute words for their function (e.g. "frog" -> "SUB")
        relevant_edges_vars = set()
        var_dict = {}
        for k in a.keys():
            match_string = '(' + ')|('.join(a[k]) + ')'
            var_dict[str(k)] = re.compile("(?<![a-zA-Z])"+match_string+"(?![a-zA-Z])")
        for edge in relevant_edges:
            var_dict, new_edge = var_substitute_edge(var_dict, edge)
            relevant_edges_vars.add(new_edge)
        rule.precondition = relevant_edges_vars

        for node in a_inv.keys():
            nodes_and_neighbors |= state2.neighbors(node)


        #first we look at the effects of the action, by comparing state 2 to state 1
        for d in differences:
            #if the set is empty we don't need to do anything
            if not len(differences[d]):
                continue
            #take some random object to see what type it is
            #(the only way to do this is to pop it, so we need to do it with a 
            #copy to keep the original intact)
            diff_obj = copy.deepcopy(differences[d]).pop()
            if isinstance(diff_obj, str):
                #something happened with a node in state1 when transitioning 
                #to state2
                #look at all nodes in a_inv and their neighbors
                changed_nodes = differences[d] & nodes_and_neighbors
                #put in all the grammatical functions of the words (SUBJ, OBJ, 
                #etc.) for everything that has changed
                #TODO rewrite these substitution expressions
                rule.effect[d] = set([k for k, v in a.items() 
                    if v in changed_nodes])
            elif isinstance(diff_obj, tuple):
                #something happened with an edge in state1 when transitioning 
                #to state2
                changed_edges = [edge for edge in differences[d] if 
                    edge[0] in nodes_and_neighbors or
                    edge[1] in nodes_and_neighbors]
                #substitute words for their grammatical function again
                #(TODO)while substituting the rest with variables (VAR1, VAR2, etc.)
                print "changed_edges: " + str(changed_edges)
                changed_edge_vars = set()
                var_dict = {}
                for k in a.keys():
                    match_string = '(' + ')|('.join(a[k]) + ')'
                    var_dict[str(k)] = re.compile("(?<![a-zA-Z])"+match_string+"(?![a-zA-Z])")
                for edge in changed_edges:
                    var_dict, new_edge = var_substitute_edge(var_dict, edge)
                    changed_edge_vars.add(new_edge)
                rule.effect[d] = changed_edge_vars
            else:
                raise TypeError('difference object contains object of type: '\
                    +type(diff_obj))
        print rule.effect
        rules.append(rule)
    return rules

def var_substitute_edge(var_dict, edge):
    '''
    This function substitutes the node names in the edges with variables from
    the var_dict. var_dict also gets updated by this function for unseen 
    variables
    '''
    new_edge = []
    for e in edge:
        e_sub = e[:]
        for k in var_dict:
            e_sub = var_dict[k].sub(k, e_sub)
        new_edge.append(e_sub)
    return var_dict, tuple(new_edge)

def parse_story(story):
    '''
    This function will parse the actions in a story into a more 
    machine-readable format, and try to learn from each action at the same time
    '''
    parsed_story = []
    story_rules = []
    last_state_index = -1
    for i in xrange(len(story)):
        if isinstance(story[i], str):
            #this is a (series of) actions. Multiple actions can be in the same
            #string, separated by periods ('.').
            sentences = story[i].split('.')
            for s in sentences:
                s.strip()
                parsed_sentence = parse_action.parse_sentence(s)
                parsed_story.append(parsed_sentence)
        elif isinstance(story[i], story_db.State):
            #this is a story state, we want to learn all the actions between
            #this state and the previous one (last_state_index is used for that)
            parsed_story.append(story[i])
            if last_state_index >= 0:
                prev_state = parsed_story[last_state_index]
                current_state = story[i]
                actions = parsed_story[last_state_index+1:-1]
                #print last_state_index, len(parsed_story)-2
                #print parsed_story
                rules = learn_actions(prev_state, current_state, actions)
                story_rules.extend(rules)
            last_state_index = len(parsed_story)-1
        elif isinstance(story[i], list):
            #this is a story within a story
            story_in_story = parse_story(story[i])
            parsed_story.append(story_in_story[0])
            story_rules.extend(story_in_story[1])
        else:
            raise TypeError('story contains object of type: '+type(story[i]))
    return parsed_story, story_rules

def state_diff(state1, state2):
    '''
    This function find the differences between 2 states, such as nodes
    and edges appearing and disappearing.
    states are dictionaries, mapping nodes to a list of connecting ones
    '''
    diff = {}
    nodes1 = state1.state.keys()
    nodes2 = state2.state.keys()
    diff['nodes_gone'] = set(nodes1) - set(nodes2)
    diff['nodes_appeared'] = set(nodes2) - set(nodes1)
    diff['edges_gone'] = set()
    for n1 in nodes1:
        for n2 in state1.state[n1]:
            if not state2.has_edge(n1, n2):
                diff['edges_gone'].add((n1,n2))
    diff['edges_appeared'] = set()
    for n2 in nodes2:
        for n1 in state2.state[n2]:
            if not state1.has_edge(n1, n2):
                diff['edges_appeared'].add((n1,n2))
    return diff

class StoryRule:
    '''
    In this object story rules are stored. 
    A rule consists of the action (for example "kill"),
    a precondition (for this example [("SUB", "hate") ("hate", "OBJ")])
    an effect ({"nodes_gone":["OBJ"]})
    and a dictionary of 'typical' actors 
    (for example {SUB:assassin, OBJ:king} 
    '''
    action = ''
    precondition = []
    effect = {}
    actors = []

    def __init__(self, action=None):
        self.action = action
        self.precondition = []
        self.effect = {}
        self.actors = []

    def metadata(self):
        '''
        This function returns some metadata about this rule instance.
        The idea is that this can be used while generating a story to see how
        complex the rule is. Because of that, it returns the amount of
        preconditions, the amount of effects, and the amount of actors involved
        '''
        metadata = {}
        metadata['precs'] = len(self.precondition)
        metadata['effects'] = sum([len(self.effect[e]) for e in self.effect])
        metadat['actors'] = len(self.actors) #TODO check for (empty) strings
        return metadata

    def print_all(self):
        print '----------------------------------------------------------------'
        print self.action
        print self.actors
        print 'preconditions:'
        print self.precondition
        print 'effects:'
        print self.effect
        print '----------------------------------------------------------------'

class RuleBase:
    '''
    This object stores a list of parsed stories and the rules learned from them.
    It also contains a function to query the probability of a certain rule
    '''

    def __init__(self, story_names):
        '''
        This method creates a rulebase from a list of story names
        '''
        self.story_base = []
        self.rule_base = []
        for story_name in story_names:
            methodToCall = getattr(story_db, story_name)
            story = methodToCall()
            parsed_story, story_rules = parse_story(story)
            self.story_base.append((story_name, parsed_story, story_rules))
            self.rule_base.extend(story_rules)

    def query_rule_base(self, query):
        '''
        This function queries the rule base. 
        the query is a dictionary mapping grammatical function to certain actors.
        for example:
        query = {'VERB':['kill'], 'OBJ':['prince', 'princess']}
        would return the probability of a prince or princess being killed by some story actor
        valid fields in the query are VERB, SUBJ, OBJ and DAT
        '''
        #first, find all rules containing the correct action
        rules = [rule for rule in self.rule_base if rule.action in query['VERB']]
        if not len(rules):
            return None
        del query['VERB']
        rules_sat_q = copy.deepcopy(rules)
        #then, of those rules, find the ones where all other parts of the query are satisfied
        for q in query:
            rules_sat_q = [rule for rule in rules_sat_q 
                if rule.actors[q] in query[q]]
        return len(rules_sat_q)/len(self.rule_base)

def test():
    all_rules = RuleBase(['frogprince', 'stork'])
    actionlist = ['transforms']
    transform_rules = [rule for rule in all_rules.rule_base if rule.action in actionlist]
    print 'printing rules that satisfy query'
    print len(transform_rules)
    for rule in transform_rules:
        rule.print_all()
    """
    fp = story_db.frogprince()
    parsed_fp, rules_fp = parse_story(fp)
    stork = story_db.stork()
    parsed_stork, rules_stork = parse_story(stork)
    all_rules = copy.copy(rules_fp)
    all_rules.extend(rules_stork)
    return all_rules
    """

if __name__ == "__main__":
    print test()

"""
import read_story
story = story_db.frogprince()
parsed_story, rules = read_story.parse_story(story)
"""
