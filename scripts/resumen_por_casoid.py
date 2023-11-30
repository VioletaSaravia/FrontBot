import pandas as pd

# archivo = pd.read_excel("tartagal.xlsx")
archivo = pd.read_csv("tartagal.csv")

# with open("archivos.csv", "w", encoding="utf-8") as test:
#     test.write("Acción,Valor 1,Valor 2,Valor 3\n")
#     for casoid in archivo["caso_id"]:
#         test.write(f"link,http://172.26.241.24/site/modulo-federal/caso-resumen/{casoid}\n")
#         test.write(f"esperar,2\n")
#         test.write("boton,Imprimir\n")
#     test.write(f"esperar,3\n")

with open("capturas.csv", "w", encoding="utf-8") as capturas:
    capturas.write("Acción,Valor 1,Valor 2,Valor 3\n")
    for _, row in archivo.iterrows():
        capturas.write(f"link,http://172.26.241.24/site/acompanar/busqueda/{row['pac_id']}\n")
        capturas.write("solapa,Programa Acompañar\n")
        capturas.write(f"captura,{row['cascao_id']} Acompañar\n")
        match row["pac_estado"]:
            case "caso-nuevo":
                continue
            case "programa-activo" | "solicitud-compatible" | "programa-cese" | "programa-completo":
                capturas.write("solapa,Programa Acompañar: Estados\n")
                capturas.write(f"captura,{row['cascao_id']} Estados\n")
                capturas.write("solapa,Programa Acompañar: Pagos\n")
                capturas.write(f"captura,{row['cascao_id']} Pagos\n")
                capturas.write("solapa,Programa Acompañar: Plan acompañamiento\n")
                capturas.write(f"captura,{row['cascao_id']} Plan acompañamiento\n")
                continue
            case "revision":
                capturas.write("solapa,Programa Acompañar: Estados\n")
                capturas.write(f"captura,{row['cascao_id']} Estados\n")
                continue
            case "revision-pendiente":
                capturas.write("solapa,Programa Acompañar: Estados\n")
                capturas.write(f"captura,{row['cascao_id']} Estados\n")
                capturas.write("solapa,Programa Acompañar: Plan acompañamiento\n")
                capturas.write(f"captura,{row['cascao_id']} Plan acompañamiento\n")
                continue
            case "rechazado-mmgyd":
                capturas.write("solapa,Programa Acompañar: Estados\n")
                capturas.write(f"captura,{row['cascao_id']} Estados\n")
                continue

