import requests
import logging
import msal
import json

# import configparser
# config = configparser.ConfigParser()
# config.read('config.cfg')

app = msal.ConfidentialClientApplication(
    client_id='a515ffad-42b1-4fb8-8da1-a0b36ef67015',
    authority='https://login.microsoftonline.com/34f3cdbc-8533-4faa-a2c8-b782028891fa',
    client_credential='Vtd8Q~lW2Mx7TKcxS7D-syiN8y1JBw_gzeiE3b6H'
)

SCOPE = ["https://graph.microsoft.com/.default"]
URL = "https://graph.microsoft.com/v1.0"
TEST_ENDPOINT = "https://graph.microsoft.com/v1.0/users"
ENDPOINTS = {
    "excel_celda": lambda id, solapa, fila, col:
    f"{URL}/me/drive/items/{id}/workbook/worksheets('{solapa}')/cell(row={fila}, column={col})",
    "excel_rango": lambda id, solapa, dir:
    f"{URL}/me/drive/items/{id}/workbook/worksheets('{solapa}')/range(address='{dir}')"
}

resultado = app.acquire_token_silent(SCOPE, account=None)

if not resultado:
    logging.info("No hay token.")
    resultado = app.acquire_token_for_client(scopes=SCOPE)

if "access_token" in resultado:
    graph_data = requests.get(
        TEST_ENDPOINT,
        headers={'Authorization': 'Bearer ' + resultado['access_token']}, ).json()
    print("Graph API call result: ")
    print(json.dumps(graph_data, indent=2))
else:
    print(resultado.get("error"))
    print(resultado.get("error_description"))


# GET https://graph.microsoft.com/v1.0/me/drive/items/01V73LF2P3UTODBS5325D37PJKIFBIJ2NH/workbook/worksheets('PRIMERA')/cell(row=0,column=0)
# GET https://graph.microsoft.com/v1.0/me/drive/items/{id}/workbook/worksheets/{name}/range(address='{address}')
# PATCH https://graph.microsoft.com/v1.0/me/drive/items/{id}/workbook/worksheets/{name}/range(address='{address}')
