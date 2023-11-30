# FrontBot

## Requirements

- Python 3.10+
- Chrome/Firefox/Edge
- Chromedriver ([Link](https://chromedriver.chromium.org/))
- Geckodriver ([Link](https://github.com/mozilla/geckodriver/releases))
- Edgedriver ([Link](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/))

Add drivers to the *include/* folder.

## Usage

Open a terminal on the FrontBot folder and type:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m venv .venv
pip install -r requirements.txt
python run.py
```

Make sure you run all pip commands with the virtual environment activated:

![VSCode example](/static/venv_terminal.png)

Tests are csv files that go on the *tests/* folder. Each row corresponds to an instruction: the first row is its name and the rest are parameters. Once finished, logs and screenshots go on the *logs/* folder.

### Instructions (TODO)

| Acción     | Valor 1                             | Valor 2                                 | Valor 3 |
| ---------- | ----------------------------------- | --------------------------------------- | ------- |
| login      | usuario                             | contraseña                              |         |
| menu       | menu                                | submenu                                 |         |
| solapa     | nombre                              |                                         |         |
| formulario | tipo (desplegable, opciones, input) | nombre                                  | valor   |
| boton      | nombre                              | numero (si hay más de uno en la solapa) |         |
| captura    |                                     |                                         |         |
| link       | url (escribir con IP)               |                                         |         |