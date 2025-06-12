import xml.etree.ElementTree as ET
import mysql.connector

NAMESPACES = {'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}

def carregar_dados(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    table = root.find('.//ss:Table', NAMESPACES)
    linhas = table.findall('ss:Row', NAMESPACES)

    dados = []

    for i, row in enumerate(linhas[1:]):  # Ignora cabeçalho
        celulas = row.findall('ss:Cell', NAMESPACES)
        linha = [''] * 13
        idx = 0
        for cell in celulas:
            index_attr = cell.attrib.get('{urn:schemas-microsoft-com:office:spreadsheet}Index')
            if index_attr:
                idx = int(index_attr) - 1
            data = cell.find('ss:Data', NAMESPACES)
            linha[idx] = data.text.strip() if data is not None and data.text else ''
            idx += 1
        if linha[0]:
            item = {
                'codigo': linha[0],
                'disciplina': linha[1],
                'curso': linha[2],
                'professor': linha[4],
                'horario': linha[5],
                'sala': linha[10]
            }
            dados.append(item)
    return dados

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Thais2004!",
        database="ifsp"
    )

def importar_para_banco(dados):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM dados_ifsp")  # Limpa tabela antes de importar

    for d in dados:
        cursor.execute(
            "INSERT INTO dados_ifsp (codigo, disciplina, curso, professor, horario, sala) VALUES (%s, %s, %s, %s, %s, %s)",
            (d['codigo'], d['disciplina'], d['curso'], d['professor'], d['horario'], d['sala'])
        )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"{len(dados)} registros importados com sucesso.")

if __name__ == "__main__":
    dados = carregar_dados('dados_ifsp.xml')
    importar_para_banco(dados)
