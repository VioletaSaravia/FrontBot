import codecs
import json
from dataclasses import dataclass
from enum import Enum
import pytest


class Action(Enum):
    click = 1
    input = 2


@dataclass
class Instruction:
    xpath: [str]
    action: [Action]
    param_count: int

    def __init__(self, xpath: [str], action: [Action]):
        self.xpath = xpath
        self.action = action
        self.param_count = 0
        for i in xpath:
            self.param_count += i.count('%')

        for i in action:
            if i == Action.input:
                self.param_count += 1


# TODO alises tipo boton[nombre, xpath]
InstructionSet = dict[str, Instruction]


def load_instruction_set(path: str) -> InstructionSet:
    data: dict[str, [[str]]] = json.load(codecs.open(path, 'r', 'utf-8-sig'))

    result: InstructionSet = {}
    for name, values in data.items():
        xpaths: [str] = []
        actions: [Action] = []
        for pair in values:
            xpaths.append(pair[0])
            match pair[1]:
                case "click":
                    actions.append(Action.click)
                case "input":
                    actions.append(Action.input)
                case invalid:
                    raise ValueError(f"action doesn't exist: {invalid}")

        result[name] = Instruction(xpaths, actions)

    return result


class WebBrowser(Enum):
    chrome = 1
    firefox = 2
    edge = 3
