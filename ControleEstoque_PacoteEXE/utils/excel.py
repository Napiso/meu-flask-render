import pandas as pd
from flask import make_response
from io import BytesIO

def exportar_excel(titulo, colunas, dados):
    df = pd.DataFrame(dados, columns=colunas)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=titulo)
    output.seek(0)
    response = make_response(output.read())
    response.headers["Content-Disposition"] = f"attachment; filename={titulo}.xlsx"
    response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return response
