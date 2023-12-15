import face_recognition

# Carrega os arquivos em um Array
biden_image = face_recognition.load_image_file("Item 02\joebiden.jpg")
obama_image = face_recognition.load_image_file("Item 02\obama.jpg")
unknown_image = face_recognition.load_image_file("Item 02\obama2.jpg")

# Obtenha as codificações faciais para cada rosto em cada arquivo de imagem
# Como pode haver mais de um rosto em cada imagem, ele retorna uma lista de codificações.
# Mas como sei que cada imagem tem apenas uma face, só me importo com a primeira codificação de cada imagem, então pego o índice 0.
try:
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
except IndexError:
    print("Não consegui localizar nenhum rosto em pelo menos uma das imagens. Verifique os arquivos de imagem!")
    quit()

known_faces = [
    biden_face_encoding,
    obama_face_encoding
]

# resultados é uma matriz de Verdadeiro/Falso informando se o rosto desconhecido corresponde a alguém na matriz de rostos conhecidos
results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

print("O rosto desconhecido é uma foto de Biden? {}".format(results[0]))
print("O rosto desconhecido é uma foto de Obama? {}".format(results[1]))
print("O rosto desconhecido é uma nova pessoa que nunca vimos antes? {}".format(not True in results))