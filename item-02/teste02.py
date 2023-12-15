from PIL import Image
import face_recognition

# Carrega o arquivo jpg em um array numpy
image = face_recognition.load_image_file("Item 02\obama.jpg")

# Encontre todos os rostos na imagem usando uma rede neural convolucional pré-treinada.
# Este método é mais preciso que o modelo HOG padrão, mas é mais lento
# a menos que você tenha uma GPU nvidia e um dlib compilado com extensões CUDA. Mas se você fizer isso,
# isso usará a aceleração da GPU e terá um bom desempenho.

face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

print("Foram encontrados {} rostos nesta imagem.".format(len(face_locations)))

for face_location in face_locations:

    # Imprima a localização de cada rosto nesta imagem
    top, right, bottom, left = face_location
    print("Um rosto está localizado na localização do pixel Superior: {}, Esquerda: {}, Inferior: {}, Direita: {}".format(top, left, bottom, right))

    # Você pode acessar o rosto real assim:
    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.show()