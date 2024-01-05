import logging
import os
import time
from dataclasses import field
from datetime import datetime
from multiprocessing import Process

from src.data import *
from src.driver import nueva_prueba


@dataclass
class SingleInstruction:
    name: str
    params: [str]


@dataclass
class InstructionList:
    list: [SingleInstruction]


@dataclass
class Prueba:
    explorador: WebBrowser
    oculto: bool = False
    instruction_set: InstructionSet = field(default_factory=dict)
    instruction_list: InstructionList

    def __post_init__(self):
        pass

    def load_instruction_list(self, path: str):
        with open(path, 'r', encoding='utf-8') as file:
            file_list = file.read()

        self.instruction_list = file_list  # TODO

    def load_instruction_set(self, path: str):
        self.instruction_set = init_instruction_set(path)

    def load_logger(self, log_path: str):
        date = datetime.now().strftime("[%Y-%m-%d %H%M%S]")

        logging.basicConfig(
            filename=f"log/{date} {os.path.basename(log_path).split('/')[-1][:-4]}.log",
            encoding='utf-8',
            level=logging.INFO)

        logging.info(f"Nueva prueba:")

    def parse(self):
        driver = nueva_prueba(self)

        prueba_time = datetime.now()
        for instruccion in self.instrucciones:
            runtime = datetime.now()
            try:
                driver.action(instruccion)
            except Exception as e:
                logging.error(
                    f'Instruction: {instruccion.__str__()} returned {type(e).__name__}:\n {str(e)}')
                break
            else:
                runtime = (datetime.now() - runtime).total_seconds()
                logging.info(f"Instruction: {instruccion.__str__()} executed in {runtime:.2f} seconds")

        logging.info(f"Final duration: {(datetime.now() - prueba_time).total_seconds():.2f} seconds")
        logging.shutdown()
        driver.quit()
        return


@dataclass
class TestBattery:
    base: Prueba
    paralelo: int = field(default=0)
    repeticiones: int = field(default=1)
    frecuencia: int = field(default=0)

    def ejecutar_todo(self):
        procesos = []
        for usuarix in range(self.paralelo):
            if len(procesos) == self.paralelo:
                [p.join() for p in procesos]
                procesos = []

                time.sleep(self.frecuencia)

            p = Process(target=self.base.parse, args=[usuarix])
            procesos.append(p)
            p.start()
