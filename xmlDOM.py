#!/usr/bin/python

import xml.dom.minidom


class XML_State(object):
    def __init__(self):
        self.name = ""
        self.transitions = []


class XML_Transition(object):
    def __init__(self):
        self.event = ""
        self.targetStateName = ""


# list of all states
XML_states = []

# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("FSM2.xml")
collection = DOMTree.documentElement

# Get all the states in the collection
states = collection.getElementsByTagName("state")

for state in states:
    XML_state = XML_State()
    XML_state.name = state.getAttribute("id")

    transitions = state.getElementsByTagName('transition')
    XML_Transitions = []
    for transition in transitions:
        trans = XML_Transition()
        trans.event = transition.getAttribute("event")
        trans.targetStateName = transition.getAttribute("target")
        XML_Transitions.append(trans)

    XML_state.transitions = XML_Transitions
    XML_states.append(XML_state)

print len(XML_states)


def codeGenStates(XML_states):
    code = "states = ["

    arrayOfStates = []
    for state in XML_states:
        arrayOfStates.append("State(name='" + state.name + "') ")

    code += ",".join(str(item) for item in arrayOfStates)
    code += "]"
    return code


def codeGenTransitions(XML_states):
    code = "transitions = ["

    arrayOfTransition = []
    for state in XML_states:
        for trans in state.transitions:
            print trans.event
            arrayOfTransition.append(
                "{'trigger': '" + trans.event + "', 'source': '" + state.name + "', 'dest': '" + trans.targetStateName + "'}")

    code += ",".join(str(item) for item in arrayOfTransition)
    code += "]"
    return code


def generateCode(XML_state):
    code = "#Define the class of your object \n\nclass CLASS_NAME(object):\n   pass\n\n#instance of your object" \
           "\nOBJECT_NAME = CLASS_NAME()\n\n"
    code += codeGenStates(XML_states)
    code += "\n"
    code += codeGenTransitions(XML_states)
    code += "\n# Initialize\n"
    code += "machine = Machine(OBJECT_NAME, states=states, transitions=transitions, initial='" + XML_states[
        0].name + "')"

    return code


f = open('gen.py.partial', 'w+')
f.write(generateCode(XML_states))
f.close()
