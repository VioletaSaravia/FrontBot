from dataclasses import dataclass, field
from enum import Enum


class Web(Enum):
    capar = "http://181.209.31.158/"
    test = "http://172.26.241.34"
    preprod = "http://172.26.241.83"
    prod = "http://172.26.241.24"
    local = ""


class Explorador(Enum):
    chrome = 1
    firefox = 2
    edge = 3


class Operador(Enum):
    formulario = 1
    boton = 2
    login = 3
    logout = 4
    captura = 5
    menu = 6
    solapa = 7
    link = 8
    tecla = 9
    esperar = 10
    loop = 11


@dataclass
class OperadorOpciones:
    saltear: int
    captura: bool
    test: bool


@dataclass
class InstruccionArgs:
    saltear: int = field(default=0)
    test: bool = field(default=False)
    capturar: bool = field(default=False)


@dataclass
class InstruccionBase:
    args: InstruccionArgs


@dataclass
class Menu(InstruccionBase):
    menu: str
    submenu: str


@dataclass
class Solapa(InstruccionBase):
    nombre: str


class FormularioTipo(Enum):
    desplegable = 1
    opciones = 2
    input = 3

    def __repr__(self) -> str:
        return self.name


@dataclass
class Formulario(InstruccionBase):
    tipo: FormularioTipo
    nombre: str
    valor: str


@dataclass
class Boton(InstruccionBase):
    nombre: str


@dataclass
class Link(InstruccionBase):
    url: str


@dataclass
class Esperar(InstruccionBase):
    tiempo: int


@dataclass
class Captura(InstruccionBase):
    nombre: str | None


Instruccion = Menu | Solapa | Formulario | Boton | Captura | Link | Esperar


@dataclass
class Usuarix:
    correo: str
    password: str = "123456"
