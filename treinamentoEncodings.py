import json
import os
import cv2

import face_recognition
import numpy as np
from PIL import Image

# DIRETORIO COM AS IMAGENS DA PESSOA

diretorio = 'imagens/leonardo costa'

# INICIANDO UMA LISTA VAZIA PARA RECEBER OS ENCODINGS
face_encodings = []

# LOOP PARA PERCORRER TODAS AS IMAGENS DO DIRETORIO
for filename in os.listdir(diretorio):
    if filename.endswith(".jpg") or filename.endswith(".png"):

        # REDIMENCIONANDOS AS IMAGENS PARA ECONOMIA DE RECURSOS
        imagem = Image.open(os.path.join(diretorio, filename))
        imagem = imagem.resize((100, 100))

        # CONVERTENDO DE PILL PARA NUMPY
        imagem = np.array(imagem)
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

        # INDENTIFICAÇÃO DAS FACES NAS IMAGENS E REGISTRO DOS ENCODINGS
        face_locations = face_recognition.face_locations(imagem, model="cnn")
        encodings = face_recognition.face_encodings(
            imagem, face_locations, num_jitters=10)

        if len(encodings) > 0:
            # ADICIONANDO OS ENCODINGS NO DICIONARIO
            face_encodings.extend(encodings)
            print(f"O encoding da imagem {filename} foi um sucesso.")
        else:
            print(f"Não foi possível encontrar face na imagem {filename}.")

# CONVERTENDO DE NUNPY PARA LIST, (FORMATO PARA O JSON)
face_encodings = [encoding.tolist() for encoding in face_encodings]

# CRINANDO DICIONARIO PARA ARMAZENAMENTO DOS DADOS ENCODINGS
data = {
    "nome": 'Leonardo Cabral da Costa',
    "face_encodings": face_encodings
}

# SALVANDO OS ENCODINGS DENTRO DO ARQUIVO JSON, DENTRO DA PASTA SCRIPTS
script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, 'scripts', 'encodings.json')

# CARREGANDO OS DADOS DOS ARQUIVOS JSON JÁ EXISTENTES, CASO NECESSÁRIO
dados_json = {"pessoas": []}
if os.path.exists(file_path) and os.stat(file_path).st_size != 0:
    with open(file_path, 'r') as arquivo:
        dados_json = json.load(arquivo)

# ADICIONANDO OS NOVOS DADOS NO ARQUIVO JSON
dados_json['pessoas'].append(data)

# SALVANDO OS DADOS NOVOS NO ARQUIVO JSON
with open(file_path, 'w') as arquivo:
    json.dump(dados_json, arquivo, indent=4,
              default=lambda x: x.tolist() if isinstance(x, np.ndarray) else x)
    print("dados salvos com sucesso no aquivo encodings.json")
