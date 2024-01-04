import os
import time
from sys import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as edgeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
from selenium.webdriver.support.expected_conditions import element_to_be_clickable as clickable
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located as all_present
from selenium.webdriver.support.expected_conditions import presence_of_element_located as present
from selenium.webdriver.support.expected_conditions import visibility_of_any_elements_located as any_visible
from selenium.webdriver.support.wait import WebDriverWait

from src.data import *

WAIT_TIME = 20


def nueva_prueba(prueba):
    executable = ""
    options = None

    browser: type[webdriver.Chrome] | type[webdriver.Firefox] | type[webdriver.Edge]
    match prueba.explorador:
        case WebBrowser.chrome:
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

        case WebBrowser.firefox:
            browser = webdriver.Firefox
            options = firefoxOptions()
            options.add_argument("start-maximized")
            if prueba.oculto:
                options.add_argument('--headless')
            if platform == "win32":
                executable = "include/geckodriver.exe"
            elif platform == "linux":
                executable = "include/geckodriver"

        case WebBrowser.edge:
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

    @dataclass
    class Driver(browser):  # type: ignore
        inst_set: InstructionSet

        def __init__(self, options, executable: str, set_path: str):
            browser.__init__(self, options=options)  # , executable_path=executable)
            self.inst_set = load_instruction_set(set_path)
            self.contador_capturas = 1

        def action(self, name: str, *args):
            inst = self.inst_set[name]
            cur_arg = 0

            for i in range(len(inst.xpath)):
                path: str = inst.xpath[i]
                # TODO loop
                path = path.replace('%', args[cur_arg], __count=1)
                cur_arg += 1

                WebDriverWait(self, WAIT_TIME).until(present((By.XPATH, path)))
                element = self.find_element(By.XPATH, value=path)
                ActionChains(self).scroll_to_element(
                    element).scroll_by_amount(0, -200).perform()

                match inst.action[i]:
                    case Action.click:
                        WebDriverWait(self, WAIT_TIME).until(clickable(element)).click()
                    case Action.input:
                        WebDriverWait(self, WAIT_TIME).until(clickable(element)).send_keys(args[cur_arg])
                        cur_arg += 1  # ???
                    case invalid:
                        return AttributeError(f"Action doesn't exist: {invalid}")
            return

        def log_screenshot(self, log: str, evento: str) -> None:
            """Toma una captura de la pantalla actual y guarda en log/"""

            if not os.path.exists(f"{log}"):
                os.makedirs(f"{log}", exist_ok=True)
            nombre_captura = "0" * (2 - len(str(self.contador_capturas)))

            path = f'{log}/captura{nombre_captura}{str(self.contador_capturas)}.png' \
                if not evento \
                else f'{log}/Caso {evento}.png'
            # self.save_screenshot(path)

            element = self.find_element(By.CLASS_NAME, "nav-tabs-body")

            required_height = self.execute_script('return document.body.parentNode.scrollHeight')
            self.set_window_size(1080, required_height * 2)

            element.screenshot(path)

            self.contador_capturas += 1

        def link(self, url: str) -> None:
            time.sleep(2)
            # self.implicitly_wait(2) # TODO por qué no anda?¿?¿
            self.get(url)

    return Driver(prueba.web, options, executable)
