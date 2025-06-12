import mysql.connector
from meta_ai_api import MetaAI
import re

# Conexão com o banco de dados
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Thais2004!',
    database='ifsp'
)
cursor = conn.cursor(dictionary=True)

# Inicializar IA
ai = MetaAI()

print("\n🤖 Chatbot IFSP Campinas | Digite '/sair' para encerrar.\n")

while True:
    pergunta = input("Você: ")
    if pergunta.lower() == '/sair':
        print("Bot: Até mais!")
        break

    # Adiciona instrução para gerar SQL
    prompt = f"Responda à pergunta abaixo usando SQL para a tabela 'dados_ifsp':\n\n{pergunta}\n\nRetorne apenas as queries SQL necessárias para responder, sem explicações."

    resposta = ai.prompt(message=prompt)
    resposta_ia = resposta['message']
    print(f"\nSQL gerado pela IA:\n{resposta_ia}\n")

    # Extrair todas as consultas SQL válidas usando regex
    sqls = re.findall(r"SELECT .*?FROM dados_ifsp.*?;", resposta_ia, flags=re.IGNORECASE | re.DOTALL)

    if not sqls:
        print("Bot: A resposta não parece conter consultas SQL válidas.")
        continue

    # Executa cada SQL e mostra os resultados
    for sql in sqls:
        try:
            cursor.execute(sql)
            resultados = cursor.fetchall()
            if resultados:
                print("Bot:")
                for linha in resultados:
                    print(" - " + " | ".join(f"{k}: {v}" for k, v in linha.items()))
            else:
                print("Bot: Nenhum resultado encontrado.")
        except mysql.connector.Error as err:
            print(f"Erro na execução da consulta:\n{sql}\n{err}")

    print()

# Encerrar conexão
cursor.close()
conn.close()
