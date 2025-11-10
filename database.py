import psycopg2
#eimport os
#from dotenv import load_dotenv
from psycopg2 import Error

#load_dotenv()

#password = os. getenv

def conecta():
    try:
        conn = psycopg2.connect(
            user="postgres",
            password= 1010,
            host="localhost",
            port="5432",
            database="oficina"
        )
        print("Conectado com sucesso")

        return conn 


    except Error as e: 
        print(f"Ocorreu um erro ao conectar {e}")

def encerra_conexao(conn):
    if conn:
        conn.close()
    print("conexao encerrada com o bd")