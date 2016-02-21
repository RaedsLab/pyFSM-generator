#!/usr/bin/python

import time
import xml.dom.minidom

import jinja2


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


def codeGenStates(XML_states):
    code = []
    code.append("states = [")

    arrayOfStates = []
    for state in XML_states:
        arrayOfStates.append("\t\t\tState(name='" + state.name + "')")

    code.append(",\n".join(str(item) for item in arrayOfStates))
    code.append("\t\t]")
    return code


def codeGenTransitions(XML_states):
    code = []
    code.append("transitions = [")

    arrayOfTransition = []
    for state in XML_states:
        for trans in state.transitions:
            print trans.event
            arrayOfTransition.append(
                "\t\t\t{'trigger': '" + trans.event + "', 'source': '" + state.name + "', 'dest': '" + trans.targetStateName + "'}")

    code.append(",\n".join(str(item) for item in arrayOfTransition))
    code.append("\t\t]")
    return code


def generateCode(XML_state):
    templateLoader = jinja2.FileSystemLoader(searchpath=".")

    templateEnv = jinja2.Environment(loader=templateLoader)

    TEMPLATE_FILE = "FSMModelTemplate.jinja"

    template = templateEnv.get_template(TEMPLATE_FILE)

    # Specify any input variables to the template as a dictionary.
    templateVars = {"instanceCode": "self.objectName = ClassName()",
                    "classCode": "class ClassName(object):\n\tpass\n",
                    "initializeCode": "machine = Machine(self.objectName, states=self.states, transitions=self.transitions, initial='" +
                                      XML_states[0].name + "')",
                    "statesCode": '\n'.join([str(x) for x in codeGenStates(XML_states)]),
                    "transitionsCode": '\n'.join([str(x) for x in codeGenTransitions(XML_states)]),
                    "day": str(time.strftime("%d/%m/%Y")) + " " + str(time.strftime("%X"))
                    }

    # Finally, process the template to produce our final text.
    outputText = template.render(templateVars)
    return outputText


f = open('gen.py', 'w+')
f.writelines(generateCode(XML_states))
f.close()
