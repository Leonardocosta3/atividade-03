import face_recognition

# Carrega algumas imagens para comparar
known_obama_image = face_recognition.load_image_file("Item 02\obama.jpg")
known_biden_image = face_recognition.load_image_file("Item 02\joebiden.jpg")

# Obtem-se as codificações faciais das imagens conhecidas
obama_face_encoding = face_recognition.face_encodings(known_obama_image)[0]
biden_face_encoding = face_recognition.face_encodings(known_biden_image)[0]

known_encodings = [
    obama_face_encoding,
    biden_face_encoding
]

# Carrega uma imagem de teste e obtém codificações para ela
image_to_test = face_recognition.load_image_file("Item 02\obama2.jpg")
image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]

# Mostra a que distância a imagem de teste está dos rostos conhecidos
face_distances = face_recognition.face_distance(known_encodings, image_to_test_encoding)

for i, face_distance in enumerate(face_distances):
    print("A imagem de teste tem uma distância de {:.2} da imagem conhecida # {}".format(face_distance, i))
    print("Com um corte normal de 0,6, a imagem de teste corresponderia à imagem conhecida? {}".format(face_distance < 0.6))
    print("Com um corte muito estrito de 0,5, a imagem de teste corresponderia à imagem conhecida? {}".format(face_distance < 0.5))
    print()