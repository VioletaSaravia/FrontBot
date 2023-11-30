from src.data import *
from src.driver import nueva_prueba
import csv
import os
from datetime import datetime
import logging
import time
from multiprocessing import Process
from time import sleep

@dataclass
class Prueba:
    path: str
    explorador: Explorador
    web: Web
    oculto: bool = False
    instrucciones: list[Instruccion] = field(default_factory=list)

    def __post_init__(self):
        pruebacsv = open(f'tests\\{self.path}', 'r', newline='', encoding='utf-8')
        csv_iter = csv.reader(pruebacsv, delimiter=',')
        csv_iter.__next__()  # Saltear títulos

        saltear = 0
        for linea in csv_iter:
            accion = Operador[linea[0]]

            match accion:
                case Operador.boton:
                    self.instrucciones.append(Boton(InstruccionArgs(saltear), linea[1]))
                case Operador.formulario:
                    self.instrucciones.append(Formulario(
                        InstruccionArgs(saltear), FormularioTipo[linea[1]], linea[2], linea[3]))
                # TODO pasar a Macro()
                case Operador.login:
                    self.instrucciones.append(Formulario(
                        InstruccionArgs(saltear), FormularioTipo["input"], 'Correo Electrónico', linea[1]))
                    self.instrucciones.append(Formulario(
                        InstruccionArgs(saltear), FormularioTipo["input"], 'Contraseña', linea[2]))
                    self.instrucciones.append(Boton(InstruccionArgs(saltear), "Entrar"))
                case Operador.captura:
                    self.instrucciones.append(Captura(InstruccionArgs(saltear), linea[1] if linea[1] else None))
                case Operador.menu:
                    self.instrucciones.append(
                        Menu(InstruccionArgs(saltear), linea[1], linea[2]))
                case Operador.solapa:
                    self.instrucciones.append(Solapa(InstruccionArgs(saltear), linea[1]))
                case Operador.link:
                    self.instrucciones.append(Link(InstruccionArgs(saltear), linea[1]))
                case Operador.esperar:
                    self.instrucciones.append(Esperar(InstruccionArgs(saltear), int(linea[1])))

        pruebacsv.close()

    def parse(self, usuarix: Usuarix | None = None):
        path = datetime.now().strftime("[%Y-%m-%d %H%M%S]")

        logging.basicConfig(
            filename=f"log/{path} {os.path.basename(self.path).split('/')[-1][:-4]}.log",
            encoding='utf-8',
            level=logging.INFO)

        logging.info(f"Nueva prueba: {self.path} con {self.explorador.name.upper()} en {self.web.name.upper()}")

        driver = nueva_prueba(self)

        login: list[Instruccion] = []
        if usuarix is not None:
            login.append(Formulario(InstruccionArgs(), FormularioTipo["input"], 'Correo Electrónico', usuarix.correo))
            login.append(Formulario(InstruccionArgs(), FormularioTipo["input"], 'Contraseña', usuarix.password))
            login.append(Boton(InstruccionArgs(), "Entrar"))

        prueba_time = datetime.now()
        for instruccion in login + self.instrucciones:
            time = datetime.now()
            try:
                match instruccion:
                    case Link():
                        driver.link(instruccion)
                    case Menu():
                        driver.menu(instruccion)
                    case Formulario():
                        driver.formulario(instruccion)
                    case Solapa():
                        driver.solapa(instruccion)
                    case Boton():
                        driver.boton(instruccion)
                    case Captura():
                        driver.captura(f'log/{path}', instruccion)
                    case Esperar():
                        sleep(instruccion.tiempo)
            except Exception as e:
                logging.error(
                    f'Instrucción: {instruccion.__str__()} devolvió {type(e).__name__}:\n {str(e)}')
                break
            else:
                time = (datetime.now() - time).total_seconds()
                logging.info(f"Instrucción: {instruccion.__str__()} ejecutada en {time:.2f} segundos")

        logging.info(f"Duración final: {(datetime.now() - prueba_time).total_seconds():.2f} segundos")
        logging.shutdown()
        driver.quit()
        return


@dataclass
class SetPruebas:
    base: Prueba
    usuarixs: list[Usuarix] = field(default_factory=list[Usuarix])
    paralelo: int = field(default=0)
    repeticiones: int = field(default=1)
    frecuencia: int = field(default=0)

    def ejecutar_todo(self):
        self.usuarixs *= self.repeticiones
        procesos = []
        for usuarix in self.usuarixs:
            if len(procesos) == self.paralelo:
                [p.join() for p in procesos]
                procesos = []
				
                time.sleep(self.frecuencia)

            p = Process(target=self.base.parse, args=[usuarix])
            procesos.append(p)
            p.start()