import os
import time
from sys import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as edgeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
from selenium.webdriver.support.expected_conditions import element_to_be_clickable as clickable
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located as all_present
from selenium.webdriver.support.expected_conditions import presence_of_element_located as present
from selenium.webdriver.support.expected_conditions import visibility_of_any_elements_located as any_visible
from selenium.webdriver.support.wait import WebDriverWait

from src.data import *

WAIT_TIME = 20


def nueva_prueba(prueba):  # Prueba):
    executable = ""
    options = None

    browser: type[webdriver.Chrome] | type[webdriver.Firefox] | type[webdriver.Edge]
    match prueba.explorador:
        case Explorador.chrome:
            browser = webdriver.Chrome
            options = chromeOptions()
            options.add_argument("start-maximized")
            options.add_experimental_option("detach", True)

            if prueba.oculto:
                options.add_argument('--headless')
            options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])
            if platform == "win32":
                executable = "include/chromedriver.exe"
            elif platform == "linux":
                executable = "include/chromedriver"

        case Explorador.firefox:
            browser = webdriver.Firefox
            options = firefoxOptions()
            options.add_argument("start-maximized")
            if prueba.oculto:
                options.add_argument('--headless')
            if platform == "win32":
                executable = "include/geckodriver.exe"
            elif platform == "linux":
                executable = "include/geckodriver"

        case Explorador.edge:
            browser = webdriver.Edge
            options = edgeOptions()
            options.add_argument("start-maximized")
            options.add_experimental_option("detach", True)
            if prueba.oculto:
                options.add_argument('--headless')
            if platform == "win32":
                executable = "include/msedgedriver.exe"
            elif platform == "linux":
                executable = "include/msedgedriver"

    class Driver(browser):  # type: ignore
        def __init__(self, web: Web, options, executable: str):
            browser.__init__(self, options=options)  # , executable_path=executable)
            self.contador_capturas = 1
            self.get(web.value)

        def scrollear(self, dist: int) -> None:
            self.execute_script(f"window.scrollTo(0, {dist})")

        def accion(self, evento: Instruccion):
            path = ''
            WebDriverWait(self, WAIT_TIME).until(present((By.XPATH, path)))
            element = self.find_element(By.XPATH, value=path)
            ActionChains(self).scroll_to_element(
                element).scroll_by_amount(0, -200).perform()
            WebDriverWait(self, WAIT_TIME).until(clickable(element)).click()
            return

        def tecla(self, tecla: str) -> None:
            actions = ActionChains(self)
            match tecla:
                case "enter":
                    pass
                case "bajar":
                    actions.key_down(Keys.PAGE_DOWN).perform()
                case "subir":
                    pass

        def captura(self, log: str, evento: Captura) -> None:
            """Toma una captura de la pantalla actual y guarda en log/"""

            if not os.path.exists(f"{log}"):
                os.makedirs(f"{log}", exist_ok=True)
            nombre_captura = "0" * (2 - len(str(self.contador_capturas)))

            if evento.nombre is None:
                path = f'{log}/captura{nombre_captura}{str(self.contador_capturas)}.png'
            else:
                path = f'{log}/Caso {evento.nombre}.png'
            # self.save_screenshot(path)

            element = self.find_element(By.CLASS_NAME, "nav-tabs-body")

            required_height = self.execute_script('return document.body.parentNode.scrollHeight')
            self.set_window_size(1080, required_height * 2)

            element.screenshot(path)

            self.contador_capturas += 1

        def link(self, url: Link) -> None:
            time.sleep(2)
            # self.implicitly_wait(2) # TODO por qué no anda?¿?¿
            self.get(url.url)

        def menu(self, evento: Menu) -> None:
            """Abre una sección del menu (primer argumento) y entra a una página (segundo argumento)"""

            path = f"//div[@class='hkt-sidebar']/hkt-sidemenu/ul/li/button[contains(text(),'{evento.menu}')]"
            WebDriverWait(self, WAIT_TIME).until(present((By.XPATH, path)))
            element = self.find_element(By.XPATH, value=path)
            ActionChains(self).scroll_to_element(element).perform()
            element.click()

            path = f"//hkt-collapse/div[@class='collapse show']/hkt-sidemenu//a[contains(text(),'{evento.submenu}')]"
            WebDriverWait(self, WAIT_TIME).until(present((By.XPATH, path)))
            element = self.find_element(By.XPATH, value=path)
            ActionChains(self).scroll_to_element(element).perform()
            element.click()

            return

        def solapa(self, evento: Solapa) -> None:
            """Selecciona una solapa de un formulario con varias páginas
            (Acompañar, MF, etc.)."""
            acciones = ActionChains(self)
            path = f"//button[contains(text(), '{evento.nombre}')]"
            print(path)
            elements = WebDriverWait(self, WAIT_TIME).until(
                any_visible((By.XPATH, path)))

            # elements = self.find_elements(By.XPATH, path)
            print(elements)

            for element in elements[evento.args.saltear:]:
                acciones.scroll_to_element(element).perform()
                element.click()
                break
            return

        def boton(self, evento: Boton) -> None:
            """Aprieta un botón"""
            BOTONES_SIMBOLOS = {
                "lapiz": "fas fa-pencil-alt",
                "cruz": "fas fa-times",
                "ojo": "fa-eye fa-fw fas",
                "llave": "fa-fw fa-key fas",
                "tacho": "fa-fw fa-trash-alt fas",
                "mas": "fas fa-fw fa-plus",
                "menos": "fas fa-minus",
                "lupa": "fas fa-fw fa-search",
                "tic": "fas fa-fw fa-check"
            }

            acciones = ActionChains(self)
            if evento.nombre in BOTONES_SIMBOLOS.keys():
                path = f"//button[i[@class='{BOTONES_SIMBOLOS[evento.nombre]}']]"
            else:
                path = f"//button[contains(text(),'{evento.nombre}')]"

            botones = WebDriverWait(self, WAIT_TIME).until(
                any_visible((By.XPATH, path)))
            for boton in botones[evento.args.saltear:]:
                if clickable(boton)(self):
                    acciones.scroll_to_element(boton).perform()
                    boton.click()
                    return

        def formulario(self, evento: Formulario) -> None:
            """Completa un casillero de un formulario"""
            acciones = ActionChains(self)
            match evento.tipo:
                case FormularioTipo.desplegable:
                    path = f"//hkt-form-input-select[div/span/label[contains(text(),'{evento.nombre}')]]"
                    option = f"{path}//span[contains(text(),'{evento.valor}')]"
                    path = f"{path}//input"

                    element1 = WebDriverWait(self, WAIT_TIME).until(
                        any_visible((By.XPATH, path)))
                    # element1 = self.find_elements(By.XPATH, value=path)
                    for element in element1[evento.args.saltear:]:
                        if clickable(element)(self):
                            acciones.scroll_to_element(element).perform()
                            element.click()
                            break

                    WebDriverWait(self, WAIT_TIME).until(
                        all_present((By.XPATH, option)))
                    element2 = self.find_elements(
                        By.XPATH, value=option)
                    for element in element2:
                        if clickable(element)(self):
                            element.click()
                            return

                case FormularioTipo.opciones:
                    path = ""
                    if evento.nombre == "Efectos en la salud/integridad física/mental":  # no tiene label
                        path = f"//hkt-form-input-select-radio[@name='efectosSaludOpciones']" \
                               f"//label[contains(text(),'{evento.valor}')]"
                    elif evento.nombre == "Tipo de información":
                        # if len(args) == 2:
                        if evento.nombre:
                            path = f"//hkt-form-input-checkbox//div[label[contains(text(),'{evento.nombre}')]]/label"
                        # if len(args) == 3:
                        if evento.nombre:
                            path = f"//hkt-form-input-select-radio[@name='opciones']" \
                                   f"//div[label[contains(text(),'{evento.valor}')]]/label"
                    else:
                        path = f"//hkt-form-input-select-radio[@label='{evento.nombre}']" \
                               f"//div[label[contains(text(),'{evento.valor}')]]/label"

                    WebDriverWait(self, WAIT_TIME).until(
                        present((By.XPATH, path)))
                    element = self.find_element(By.XPATH, value=path)
                    if clickable(element)(self):
                        acciones.scroll_to_element(element).perform()
                        element.click()
                        return

                case FormularioTipo.input:
                    match evento.nombre:
                        case "Fecha nacimiento (dd/mm/yyyy)":
                            path = f"//hkt-form-input-date[@label='{evento.nombre}']//input"
                        case "Nota nueva":
                            path = "//hkt-form-input-textarea[@name='notas']//textarea"
                        case "Otra información":
                            path = "//hkt-form-input-text[@name='opcionOtro']//input"
                        case otro:
                            path = f"//hkt-form-input-text[@label='{otro}']//input"

                    WebDriverWait(self, WAIT_TIME).until(present((By.XPATH, path)))
                    element = self.find_element(By.XPATH, value=path)

                    if clickable(element)(self):
                        acciones.scroll_to_element(element).perform()
                        element.send_keys(evento.valor)
                        return

        def logout(self) -> None:
            path1 = "//span[@class='account-name']"
            path2 = "//a[contains(text(),'Salir')]"
            self.find_element(By.XPATH, value=path1).click()
            self.find_element(By.XPATH, value=path2).click()

    return Driver(prueba.web, options, executable)
