from PIL import Image, ImageDraw
import face_recognition

# Carrega o arquivo em um Array
image = face_recognition.load_image_file("Item 02\obama.jpg")

# Encontrar todas as características faciais em todos os rostos da imagem
face_landmarks_list = face_recognition.face_landmarks(image)

print("Foram encontrados {} rostos nesta imagem.".format(len(face_landmarks_list)))

# Cria um objeto PIL para desenhar a imagem
pil_image = Image.fromarray(image)
d = ImageDraw.Draw(pil_image)

for face_landmarks in face_landmarks_list:

    # Mostra a localização de cada caracteristica facial na imagem
    for facial_feature in face_landmarks.keys():
        print("O {} nesta face possui os seguintes pontos: {}".format(facial_feature, face_landmarks[facial_feature]))

    # Traça uma linha em cada caracteristica facial da imagem
    for facial_feature in face_landmarks.keys():
        d.line(face_landmarks[facial_feature], width=5)

# Exibe a Foto
pil_image.show()