from PIL import Image
import face_recognition

# Carrega o arquivo em um Array
image = face_recognition.load_image_file("Item 02\obama.jpg")

# Encontre todos os rostos na imagem usando o modelo padrão baseado em HOG.
# Este método é bastante preciso, mas não tão preciso quanto o modelo CNN e não é acelerado por GPU.

face_locations = face_recognition.face_locations(image)

print("Foram encontrados {} rostos nesta imagem.".format(len(face_locations)))

for face_location in face_locations:

    # Imprime a localização de cada rosto na imagem
    top, right, bottom, left = face_location
    print("Um rosto está localizado na localização do pixel Superior: {}, Esquerda: {}, Inferior: {}, Direita: {}".format(top, left, bottom, right))

    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.show()