from transitions import Machine
from transitions import State


class Lamp(object):
    def say_im_turned_on(self): print("Let there be LIGHT !")

    def say_im_turned_off(self): print("Hello darkness, my old friend !")


''' The object '''
lump = Lamp()

'''' THE STUFF'''
# The states
states = [
    State(name='on', on_enter=['say_im_turned_on']),
    State(name='off', on_enter=['say_im_turned_off'])
]

transitions = [
    {'trigger': 'illuminate', 'source': 'off', 'dest': 'on'},
    {'trigger': 'darken', 'source': 'on', 'dest': 'off'}
]

# Initialize
machine = Machine(lump, states=states, transitions=transitions, initial='off')


''' test'''
print lump.state
lump.illuminate()
print lump.state
print lump.is_off()
lump.darken()
