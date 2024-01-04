import logging
import os
import time
from dataclasses import field
from datetime import datetime
from multiprocessing import Process

from src.data import *
from src.driver import nueva_prueba


@dataclass
class Prueba:
    path: str
    explorador: WebBrowser
    oculto: bool = False
    instrucciones: InstructionSet = field(default_factory=dict)

    def __post_init__(self):
        pass

    def parse(self):
        path = datetime.now().strftime("[%Y-%m-%d %H%M%S]")

        logging.basicConfig(
            filename=f"log/{path} {os.path.basename(self.path).split('/')[-1][:-4]}.log",
            encoding='utf-8',
            level=logging.INFO)

        logging.info(f"Nueva prueba:")

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
