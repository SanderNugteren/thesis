def parse_story(story):
    '''
    This function will parse the actions into a more machine-readable format
    '''
    parsed_story = []
    for i in xrange(len(story)):
        if isinstance(story[i], str):
            parsed_story.append(parse_sentence(story[i]))
        else:
            parsed_story.append(story[i])
    return parsed_story

def state_diff(state1, state2):
    '''
    This function find the differences between 2 states, such as nodes
    and edges appearing and disappearing.
    states are dictionaries, mapping nodes to a list of connecting ones
    '''
    diff = {}
    nodes1 = state1.keys()
    nodes2 = state2.keys()
    diff['nodes_gone'] = set(nodes1) - set(nodes2)
    diff['nodes_appeared'] = set(nodes2) - set(nodes1)
    diff['edges_gone'] = []
    for n1 in nodes1:
        for n2 in state1[n1]:
            if not has_edge(n1, n2, state2):
                diff['edges_gone'].append(tuple(n1,n2))
    diff['edges_appeared'] = []
    for n2 in nodes2:
        for n1 in state2[n2]:
            if not has_edge(n1, n2, state2):
                diff['edges_appeared'].append(tuple(n1,n2))
    return diff

def has_edge(node1, node2, state):
    '''
    This function returns True if there is a edge between node1 and node2
    in state. These edges are transitive
    '''
    #TODO maybe check if nodes exist in the state? or just catch exceptions
    #whenever this function is called?
    return node2 in state[node1] or node1 in state[node2]

class StoryRule:
    '''
    In this object story rules are stored. 
    A rule consists of the action (for example "X kills Y"),
    a precondition (for this example "X hates Y")
    an effect ("remove Y")
    and a dictionary of 'typical' actors (for example {X:[(assassin,1), (criminal,1)], Y:[(king,2)]} would denote actor X was once observed to be an assassin, and actor Y was twice observed to be a king)
    '''
    #TODO think about storing typical actors
    
    def __init__(self, action=None):
        self.action = action
        self.precondition = ''
        self.effect = ''
        self.actors = []
