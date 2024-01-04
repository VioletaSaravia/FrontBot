import csv
import os
import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGridLayout,
    QPushButton, QComboBox, QWidget,
    QTreeWidget, QTreeWidgetItem,
    QLabel, QHBoxLayout, QSpinBox,
    QGroupBox, QCheckBox)

from src.data import *


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        with open('static/style.qss', 'r') as stylesheet:
            self.setStyleSheet(stylesheet.read())
        self.setWindowTitle('SICVG Tester')
        self.setFixedWidth(400)
        self.setMinimumHeight(720)

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self._crear_layout())

    def _crear_layout(self):
        layout = QGridLayout()
        layout.setVerticalSpacing(10)
        widgets = []

        # Lista de pruebas
        self.pruebas = self._listar_pruebas()
        widgets.append(self.pruebas)

        # Explorador
        self.explorador = QComboBox()
        for item in WebBrowser:
            self.explorador.addItem(item.name)
        widgets.append(self.explorador)

        # Procesos
        self.procesos = self._listar_procesos()
        widgets.append(self.procesos)

        # Repetición
        self.repeticion = self._listar_repeticion()
        widgets.append(self.repeticion)

        # Ocultar
        self.ocultar = QCheckBox("Ocultar explorador")
        widgets.append(self.ocultar)

        # Ejecutar
        self.boton_ejecutar = QPushButton("Ejecutar")
        self.boton_ejecutar.clicked.connect(self.ejecutar)
        widgets.append(self.boton_ejecutar)

        for x, w in zip(range(1, len(widgets) + 1), widgets):
            layout.addWidget(w, x, 0)
        return layout

    def _listar_procesos(self):
        procesos = QWidget()
        layout = QHBoxLayout()
        procesos.setLayout(layout)

        procesos_max = 200
        label = QLabel(procesos)
        label.setText(f"Pruebas en paralelo (max. {procesos_max}): ")
        layout.addWidget(label)

        self.procesos_input = QSpinBox(procesos)
        self.procesos_input.setMaximum(procesos_max)
        self.procesos_input.setMinimum(1)

        layout.addWidget(self.procesos_input)

        return procesos

    def _listar_repeticion(self):
        repeticion = QWidget()
        layout = QHBoxLayout()
        repeticion.setLayout(layout)

        label = QLabel(repeticion)
        label.setText("Repetir")
        layout.addWidget(label)

        self.repeticiones_input = QSpinBox(repeticion)
        self.repeticiones_input.setMaximum(10000)
        self.repeticiones_input.setMinimum(1)
        layout.addWidget(self.repeticiones_input)

        label = QLabel(repeticion)
        label.setText("veces, cada")
        layout.addWidget(label)

        self.frecuencia_input = QSpinBox(repeticion)
        self.frecuencia_input.setMaximum(10000)
        self.frecuencia_input.setMinimum(0)
        layout.addWidget(self.frecuencia_input)

        label = QLabel(repeticion)
        label.setText("seg.")
        layout.addWidget(label)

        return repeticion

    def _listar_pruebas(self):
        widget = QTreeWidget(self)
        widget.setColumnCount(1)
        widget.setHeaderLabels(["Pruebas"])

        for directorio in os.walk('tests'):
            subdir = QTreeWidgetItem([f"{directorio[0][6:]}"])
            for archivo in directorio[2]:
                if archivo[-4:] == ".csv":
                    archivo = QTreeWidgetItem([f'{archivo[:-4]}'])
                    subdir.addChild(archivo)
            widget.addTopLevelItem(subdir)

        widget.expandAll()
        return widget

    def ejecutar(self):
        explorador = str(self.explorador.currentText())
        web = str(self.web.currentText())
        repeticiones = int(self.repeticiones_input.text())
        frecuencia = int(self.frecuencia_input.text())
        paralelo = int(self.procesos_input.text())

        return


def main():
    tester = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(tester.exec_())
