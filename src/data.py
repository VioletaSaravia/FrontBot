import codecs
import json
from dataclasses import dataclass
from enum import Enum


class WebAction(Enum):
    click = 1
    input = 2


@dataclass
class Instruction:
    xpath: [str]
    action: [WebAction]
    param_count: int

    def __init__(self, xpath: [str], action: [WebAction]):
        self.xpath = xpath
        self.action = action
        self.param_count = 0
        for i in xpath:
            self.param_count += i.count('%')

        for i in action:
            if i == WebAction.input:
                self.param_count += 1


# TODO alises tipo boton[nombre, xpath]
InstructionSet = dict[str, Instruction]


def init_instruction_set(path: str) -> InstructionSet:
    data: dict[str, [[str]]] = json.load(codecs.open(path, 'r', 'utf-8-sig'))

    result: InstructionSet = {}
    for name, values in data.items():
        xpaths: [str] = []
        actions: [WebAction] = []
        for pair in values:
            xpaths.append(pair[0])
            match pair[1]:
                case "click":
                    actions.append(WebAction.click)
                case "input":
                    actions.append(WebAction.input)
                case invalid:
                    raise ValueError(f"action doesn't exist: {invalid}")

        result[name] = Instruction(xpaths, actions)

    return result


class WebBrowser(Enum):
    chrome = 1
    firefox = 2
    edge = 3
