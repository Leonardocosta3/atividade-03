# /modulos/face_recognition_scripts.py

import json
from datetime import datetime
import cv2
import face_recognition
import mysql.connector
import numpy as np

# CONECTANDO AO BANCO DE DADOS
def carregar_banco_dados():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lista"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

mydb, mycursor = carregar_banco_dados()

# INCIALIZANDO UMA TABELA PARA RECEBERR OS DADOS DOS ALUNOS
alunos = []

# CARREGANDO AS IMAGENS E ARMAZENDANDO OS DADOS ATRAVÉS DAS IMAGENS

def carregar_alunos():
    with open('scripts/encodings.json', 'r') as arquivo:
        dados_json = json.load(arquivo)
        alunos = []
        for pessoa in dados_json["pessoas"]:
            encodings = pessoa["face_encodings"]
            for encoding in encodings:
                encoding_array = np.array(encoding)
                alunos.append({
                    "nome": pessoa["nome"],
                    "encoding": encoding_array
                })
    return alunos

alunos = carregar_alunos()

# CARREGANDO VARIAVEIS PARA APLICAÇÃO DOS SCRIPTS
registros_feitos = set()

na_area_verde = set()
na_area_vermelha = set()

entradas_registradas = {}
saidas_registradas = {}

time_interval = 7200

fr = None

# APLICANDO FUNCIONALIDADES DENTRO DOS FRAMES (fr)
# O CODIGO NÃO INICIALIZA A CAMERA APENAS APLICA DENTRO DA FUNÇÃO AS TAREFAS DO FACE RECOGNITION E ATUALIZAÇÃO DE BANCO DE DADOS


def carregar_scripts(fr, mydb, mycursor, alunos, registros_feitos, na_area_verde, na_area_vermelha, entradas_registradas, saidas_registradas, time_interval):
    try:
        # GARANTINDO CONEXÃO COM BANCO DE DADOS
        if not mydb.is_connected() or not mycursor:
            mydb, mycursor = carregar_banco_dados()

        # APLICANDO AS LOGICAS DENTROS DOS FRAMES (fr)
        if fr is not None:
            fr = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)

            # APLICANDO LOCALIZAÇÃO E O FACE_ENCODING
            face_locations = face_recognition.face_locations(fr)
            face_encodings = face_recognition.face_encodings(
                fr, face_locations)

            # DEFININDO AREAS DE ENTRADA E SAIDA
            # SAIDA
            half_width = fr.shape[1] // 2
            red_overlay = fr.copy()
            red_overlay[:, :half_width] = (0, 0, 255)
            fr = cv2.addWeighted(red_overlay, 0.15, fr, 0.85, 0)

            # ENTRADA
            green_overlay = fr.copy()
            green_overlay[:, half_width:] = (0, 255, 0)
            fr = cv2.addWeighted(green_overlay, 0.15, fr, 0.85, 0)

            # INICIANDO LOOP PARA RECONHECIMENTO E LOCALIZAÇAO
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                nome_identificado = "Desconhecido"

                # VERIFICAÇÃO DA POSIÇÃO DE UM ROSTO NA ENTRADA OU SAIDA
                if left < half_width:
                    area = "Saida"
                else:
                    area = "Entrada"

                # INICIANDO LOOP PARA RECONHECIMENTO DA PESSOA
                # NÃO ACONTECE REGISTROS NO BANCO DE DADOS ANTES DE TER UMA ENTRADA
                for aluno in alunos:
                    comparison_result = face_recognition.compare_faces(
                        [aluno['encoding']], face_encoding)
                    if comparison_result[0]:
                        nome_identificado = aluno['nome']
                        current_time = datetime.now()
                        if nome_identificado not in registros_feitos:

                            # VERIFICANDO SE UM ALUNO É REGISTRADO NO BANCO DE DADOS NA TABELA ALUNOS
                            mycursor.execute(
                                "SELECT * FROM alunos WHERE nome = %s", (nome_identificado,))
                            aluno_registrado = mycursor.fetchone()
                            if aluno_registrado:

                                # AQUI É APLICADO A INSERÇÃO DE DADOS PARA TABELA REGISTROS, COM OS DADOS DO ALUNO, DATA E HORA DE ENTRADA E SAIDA
                                if area == "Entrada":
                                    if nome_identificado not in entradas_registradas or (current_time - entradas_registradas[nome_identificado]).total_seconds() >= time_interval:
                                        entradas_registradas[nome_identificado] = current_time
                                        if nome_identificado in saidas_registradas:
                                            del saidas_registradas[nome_identificado]
                                        na_area_verde.add(nome_identificado)
                                        if nome_identificado in na_area_vermelha:
                                            na_area_vermelha.remove(
                                                nome_identificado)
                                        data_hora_entrada = current_time.strftime(
                                            '%Y-%m-%d %H:%M:%S')
                                        try:
                                            sql = "INSERT INTO registros (nome, telefone, email, matricula, turma, data_hora_entrada) VALUES (%s, %s, %s, %s, %s, %s)"
                                            val = (
                                                nome_identificado, aluno_registrado[2], aluno_registrado[3], aluno_registrado[4], aluno_registrado[5], data_hora_entrada)
                                            mycursor.execute(sql, val)
                                            mydb.commit()
                                            print(
                                                f"Registro de entrada atualizado no banco de dados para {nome_identificado}, {data_hora_entrada}.")
                                        except mysql.connector.Error as err:
                                            print(
                                                f"Erro ao inserir os dados: {err}")

                                # AQUI É APLICADO UMA ATUALIZAÇÃO COM A SAIDA DO ALUNO, LEMBRANDO QUE SEM ENTRADA ANTES NÃO SÃO REGISTRADAS AS SAIDAS
                                elif area == "Saida":
                                    if nome_identificado not in saidas_registradas or (current_time - saidas_registradas[nome_identificado]).total_seconds() >= time_interval:
                                        saidas_registradas[nome_identificado] = current_time
                                        if nome_identificado in entradas_registradas:
                                            del entradas_registradas[nome_identificado]
                                        na_area_vermelha.add(nome_identificado)
                                        if nome_identificado in na_area_verde:
                                            na_area_verde.remove(
                                                nome_identificado)
                                        data_hora_saida = current_time.strftime(
                                            '%Y-%m-%d %H:%M:%S')
                                        try:
                                            sql = "UPDATE registros SET data_hora_saida = %s WHERE nome = %s AND data_hora_saida IS NULL"
                                            val = (data_hora_saida,
                                                   nome_identificado)
                                            mycursor.execute(sql, val)
                                            mydb.commit()
                                            print(
                                                f"Registro de saída atualizado no banco de dados para {nome_identificado}, {data_hora_saida}.")
                                        except mysql.connector.Error as err:
                                            print(
                                                f"Erro ao atualizar os dados: {err}")

                # POR QUESTÕES DE SEGURANÇA, APLIQUEI TAMBEM A LOGICA PARA PESSOAS DESCONHECIDAS

                # NESSE CASO, ALUNOS DESCONHECIDOS NÃO SÃO PESSOAS REGISTRADAS OU CADASTRADAS, ENTÃO A LOGICA É APLICADA QUANDO O NOME = 'DESCONHECIDO'
                if nome_identificado == 'Desconhecido':
                    current_time = datetime.now()
                    if area == "Entrada":
                        if 'desconhecido_entrada' not in entradas_registradas or (current_time - entradas_registradas['desconhecido_entrada']).total_seconds() >= time_interval:
                            entradas_registradas['desconhecido_entrada'] = current_time
                            if 'desconhecido_saida' in saidas_registradas:
                                del saidas_registradas['desconhecido_saida']
                            data_hora_entrada = current_time.strftime(
                                '%Y-%m-%d %H:%M:%S')
                            try:
                                sql = "INSERT INTO registros (nome, data_hora_entrada) VALUES (%s, %s)"
                                val = (nome_identificado, data_hora_entrada)
                                mycursor.execute(sql, val)
                                mydb.commit()
                                print(
                                    f"Registro de entrada atualizado no banco de dados para {nome_identificado}, {data_hora_entrada}.")
                            except mysql.connector.Error as err:
                                print(f"Erro ao inserir os dados: {err}")

                    elif area == "Saida":
                        if 'desconhecido_saida' not in saidas_registradas or (current_time - saidas_registradas['desconhecido_saida']).total_seconds() >= time_interval:
                            saidas_registradas['desconhecido_saida'] = current_time
                            if 'desconhecido_entrada' in entradas_registradas:
                                del entradas_registradas['desconhecido_entrada']
                            data_hora_saida = current_time.strftime(
                                '%Y-%m-%d %H:%M:%S')
                            try:
                                sql = "UPDATE registros SET data_hora_saida = %s WHERE nome = %s AND data_hora_saida IS NULL"
                                val = (data_hora_saida, nome_identificado)
                                mycursor.execute(sql, val)
                                mydb.commit()
                                print(
                                    f"Registro de saída atualizado no banco de dados para {nome_identificado}, {data_hora_saida}.")
                            except mysql.connector.Error as err:
                                print(f"Erro ao atualizar os dados: {err}")

                # AQUI É DESENHANDO UM RETANGULO COM OS PONTOS FEITOS PELO FACE LOCATION
                cv2.rectangle(fr, (left, top), (right, bottom), (0, 0, 255), 2)

                # AQUI É APLICADO UMA FONTE DA LETRA E O NOME DO ALUNO DENTRO DO VIDEO, RECEBE O NOME IDENTIFICADO E A AREA ONDE ESTÁ
                font = cv2.FONT_HERSHEY_DUPLEX

                # METODO SPLIT PARA EXIBIR NO VIDEO SOMENTE O PRIMEIRO NOME DO IDENTIFICADO
                primeiroNome = nome_identificado.split(' ')[0]
                cv2.putText(fr, f"{primeiroNome} - {area}", (left + 6,
                            bottom - 6), font, 0.7, (255, 255, 255), 1)

    # GARANTINDO O ENCERRAMENTO COM BANCO DE DADOS
    finally:
        if mycursor:
            mycursor.close()
        if mydb and mydb.is_connected():
            mydb.close()

        return fr, mydb, mycursor, alunos, registros_feitos, na_area_verde, na_area_vermelha, entradas_registradas, saidas_registradas, time_interval


carregar_scripts(fr, mydb, mycursor, alunos, registros_feitos, na_area_verde,
                 na_area_vermelha, entradas_registradas, saidas_registradas, time_interval)
