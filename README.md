# sicvg-testeo-ui

## Requisitos

- Python 3.10+ (No funciona en 3.9)
- Chrome/Firefox/Edge
- Chromedriver ([Link](https://chromedriver.chromium.org/))
- Geckodriver ([Link](https://github.com/mozilla/geckodriver/releases))
- Edgedriver ([Link](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/))

Poner los drivers en la carpeta *include/*.

## Uso

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m venv .venv # Luego cerrar y abrir la terminal para cambiar interpreter
pip install -r requirements.txt
python run.py
```

Asegurarse de correr todos los comandos con el entorno virtual activado:

![Ejemplo en VSCode](/static/venv_terminal.png)

Las pruebas son archivos excel que van dentro de la carpeta *tests/*. Cada fila corresponde a una acción; la primer columna es la función y el resto son los argumentos. Una vez terminada, las capturas de la prueba van a la carpeta *logs*.

### Acciones

| Acción     | Valor 1                             | Valor 2                                 | Valor 3 |
| ---------- | ----------------------------------- | --------------------------------------- | ------- |
| login      | usuario                             | contraseña                              |         |
| menu       | menu                                | submenu                                 |         |
| solapa     | nombre                              |                                         |         |
| formulario | tipo (desplegable, opciones, input) | nombre                                  | valor   |
| boton      | nombre                              | numero (si hay más de uno en la solapa) |         |
| captura    |                                     |                                         |         |
| link       | url (escribir con IP)               |                                         |         |