import copy

def frogprince():
    '''
	This function returns the story of the frog prince. Stories are lists of
    the form [state, action, state, action ...]
	'''
    story = []
    #State 1
    state1 = State()
	state1.time = 1
    state1.state['princess'] = ['princess_abilities:companionship',
            'princess_needs:ball', 'princess_race:human']
    state1.state['frog'] = ['frog_abilities:ball', 'frog_needs:companionship', 'frog_race:animal']
    #state1.state['princess_abilities:companionship'] = ['frog_needs:companionship']
    #state1.state['princess_needs:ball'] = ['frog_abilities:ball']
    story.append(state1)
    
    #State 2
	story.append('frog promises ball. princess promises companionship')
    state2 = copy(state1)
	state2.time = state1.time+1
	state2.state['promise:1'] = ['frog_abilities:ball', 'princess_needs:ball']
	state2.state['promise:2'] = ['princess_abilities:companionship', 'frog_needs:companionship']
    story.append(state2)

    #State 3
	story.append('frog does ball')
    state3 = copy(state2)
	state3.time = state2.time+1
    state3.remove('promise:1')
	state3.remove('princess_needs:ball')
	story.append(state3)
	
	#State 4
	story.append('princess goes home, has dinner with king')
	state4 = copy(state3)
	state4.time = state3.time+1
	state4.state['king'] = ['king_abilities:enforce(promise)', 'king_needs:honesty', 'king_race:human']
	#state4.state['king_abilities:enforce(promise:companionship)'] = ['promise:companionship']
	story.append(state4)
	
	#State 5
	story.append('frog asks princess for promise:2, princess refuses')
	story.append('king uses king_abilities:enforce(promise)')
	story.append('princess uses companionship')
	state5 = copy(state4)
	state5.time = state4.time+1
	state5.remove('promise:2')
	state5.remove('frog_needs:companionship')
	story.append(state5)
	
	#State 6
	story.append('frog transforms into a human')
	state6 = copy(state5)
	state6.time = state5.time+1
	#state6.remove('frog_abilities:ball')
	state6.remove('frog_race:animal')
	state6.state['frog'].append('frog_race:human')
	#state6.state['prince'] = []
	story.append(state6)
	
	#State 7
	story.append('frog marries princess')
	state7 = copy(state6)
	state7.time = state6.time+1
	state7.state['marriage:1'] = ['frog', 'princess']
	
	return story

#Caliph Stork is nog met een oude representatie gedaan, dus dat moet nog veranderd worden
def stork():
    story = []
    #State 1
    state1 = State()
	state1.time = 1
    state1.state['peddler'] = ['peddler_abilities:magic_powder',
            'peddler_needs:wealth',
			'peddler_race:human']
    state1.state['caliph'] = ['caliph_abilities:wealth',
            'caliph_abilities:lord_of_baghdad',
            'caliph_needs:speak_with_animals',
			'caliph_race:human']
    state1.state['vizier'] = ['vizier_needs:accompany_caliph', 'vizier_race:human']
    state1.state['caliph_abilities:wealth'] = ['peddler_needs:wealth']
    state1.state['peddler_abilities:magic_powder'] = ['caliph_needs:speak_with_animals']
    story.append(state1)
    #State 2
    story.append('caliph buys magic_powder')
    state2 = copy(state1)
	state2.time = state1.time+1
    state2.remove('peddler_abilities:magic_powder')
    state2.remove('peddler_needs:wealth')
	state2.state['caliph'].append('caliph_abilities:magic_powder')
	state2.state['caliph_abilities:magic_powder'] = ['caliph']
	story.append(state2)
	#State 3
	story.append('caliph learns about magic powder: speak mutabor to transform into animal, speak mutabor to transform into human, if you laugh you forget the word mutabor')
	state3.time = state2.time+1
	state3 = copy(state2)
	#how do I represent these rules? magic_powder as a node, connected with parts of the rule? predicate logic?
	state3.state['caliph_abilities:magic_powder'].append('rule:know(x,"mutabor")&&speak(x,"mutabor")&&animal(x)->human(x)')
	state3.state['caliph_abilities:magic_powder'].append('rule:know(x,"mutabor")&&speak(x,"mutabor")&&human(x)->animal(x)')
	state3.state['caliph_abilities:magic_powder'].append('rule:animal(x)&&laugh(x)->not(know(x, "mutabor"))')
	state3.state['caliph'].append('caliph_abilities:know(caliph, "mutabor")')
	state3.state['vizier'].append('vizier_abilities:know(vizier, "mutabor")')
	story.append(state3)
	#State 4
	story.append('caliph and vizier use magic_powder, speak "mutabor" and become animals')
	state4 = copy(state3)
	state4.time = state3.time+1
	state4.remove('caliph_race:human')
	state4.state['caliph'].append('caliph_race:animal')
	state4.remove('vizier_race:human')
	state4.state['vizier'].append('vizier_race:animal')
	story.append(state4)
	#State 5
	story.append('caliph and vizier listen to an animal')
	state5 = copy(state4)
	state5.time = state4.time+1
	state5.remove('caliph_needs:speak_with_animals')
	story.append(state5)
	#State 6
	story.append('caliph and vizier laugh')
	state6 = copy(state5)
	state6.time = state5.time+1
	state6.remove('caliph_abilities:know(caliph, "mutabor")')
	state6.remove('vizier_abilities:know(vizier, "mutabor")')
	story.append(state6)
	#State 7
	story.append('mirza, the son of evil magician kaschnur, an enemy of the caliph, becomes lord_of_baghdad.')
	state7 = copy(state6)
	state7.time = state6.time+1
	state7.remove('caliph_abilities:lord_of_baghdad')
	state7.state['mirza'] = ['mirza_race:human', 'mirza_abilities:lord_of_baghdad']
	state7.state['kaschnur'] = ['kaschnur_race:human']
	state7.state['parent:1'] = ['kaschnur', 'mirza']
	state7.state['enemy:1'] = ['kaschnur', 'caliph']
	story.append(state7)
	#State 8
	story.append('caliph and vizier meet owl')
	story.append('owl tells that owl is the daughter of king_of_the_indies.')
	state8 = copy(state7)
	state8.time = state7.time+1
	state8.state['owl']  = ['owl_race:animal']
	story.append(state8)
	#State 9 (parallel story of the owl/princess starts here)
	story_owl = []
	story_owl.append('kaschnur asks king_of_the_indies if mirza could marry owl. king_of_the_indies denies kaschnur.')
	state9 = State()
	state9.time = -2
	state9.state['owl'] = ['owl_race:human']
	state9.state['king_of_the_indies']  = ['king_of_the_indies_race:human']
	state9.state['mirza'] = ['mirza_race:human']
	state9.state['kaschnur'] = ['kaschnur_race:human']
	state9.state['parent:1'] = ['kaschnur', 'mirza']
	state9.state['parent:2'] = ['king_of_the_indies', 'owl']
	state9.state['enemy:2'] = ['kaschnur', 'king_of_the_indies']
	story_owl.append(state9)
	#State 10
	story_owl.append('kaschnur transforms owl into animal.')
	story_owl.append('owl can transform into human by marriage.')
	state10 = copy(state9)
	state10.time = state9.time+1
	state10.remove('owl_race:human')
	state10.state['owl'].append('owl_race:animal')
	state10.state['owl'].append('rule:exists(y)&&marriage(owl,y)&&animal(owl)->human(owl)')
	state10.state['owl'].append('owl_abilities:location(peddler)')
	story_owl.append(state10)
	story.append(story_owl)
	#State 11 (main story resumes here)
	story.append('owl promises location(peddler), caliph promises marriage(owl, caliph)')
	state11 = copy(state8)
	state11.time = state8.time+1
	state9.state['king_of_the_indies']  = ['king_of_the_indies_race:human']
	state11.state['promise:1'] = ['owl_abilities:location(peddler)', 'marriage(owl, caliph)']
	state11.state['enemy:2'] = ['kaschnur', 'king_of_the_indies']
	story.append(state11)
	#State 12
	story.append('owl, caliph and vizier go to location(peddler) and learn mutabor from peddler')
	state12 = copy(state11)
	state12.time = state11.time+1
	state12.state['caliph'].append('caliph_abilities:know(caliph, "mutabor")')
	state12.state['vizier'].append('vizier_abilities:know(vizier, "mutabor")')
	story.append(state12)
	#State 13
	story.append('caliph and vizier transform into human')
	state13 = copy(state12)
	state13.time = state12.time+1
	state13.remove('caliph_race:animal')
	state13.state['caliph'].append('caliph_race:human')
	state13.remove('vizier_race:animal')
	state13.state['vizier'].append('vizier_race:human')
	story.append(state13)
	#State 14
	story.append('caliph marries owl')
	state14 = copy(state13)
	state14.time = state13.time+1
	state14.state['marriage:1'] = ['caliph', 'owl']
	story.append(state14)
	#State 15
	story.append('owl transform into human')
	state15 = copy(state14)
	state15.time = state14.time+1
	state15.remove('owl_race:animal')
	state15.state['owl'].append('owl_race:human')
	story.append(state15)
	story.append('caliph kills kaschnur.')
	story.append('caliph transforms mirza into animal.')
	state15 = copy(state14)
	state15.time = state14.time+1
	remove('kaschnur')
	state15.remove('mirza_race:human')
	state15.remove('mirza_abilities:lord_of_baghdad')
	state15.state['mirza'].append('mirza_race:animal')
	story.append(state15)
	return story

    
class State:    
    #This is basically just a dictionary, but with some helper functions

    def __init__(self):
        self.state = {}
		self.time = 0 #this represents the time at which this event occured, as opposed to story time (relevant for flashbacks)

    def remove(self, node):
        #remove the node itself
        if node in self.state:
            del self.state[node]
        #also remove it from all other nodes
        for n in self.state:
            if node in self.state[n]:
                self.state[n].remove(node)
				
	def character_transform(self, old_char, new_char):
		#This transforms the character, while keeping relations and abilities intact
		if old_char in self.state:
			rels = self.state[old_char]
			self.state[new_char] = []
            del self.state[old_char]
			
