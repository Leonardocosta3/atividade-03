import face_recognition
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# Carregue a imagem com landmarks faciais
image_path = 'Item 02\obama.jpg'
image = face_recognition.load_image_file(image_path)
face_landmarks_list = face_recognition.face_landmarks(image)

# Abra a imagem usando PIL (Python Imaging Library)
pil_image = Image.open(image_path)
draw = ImageDraw.Draw(pil_image)

# Desenhe os landmarks faciais
for face_landmarks in face_landmarks_list:
    for facial_feature in face_landmarks.keys():
        draw.point(face_landmarks[facial_feature], fill="red")

# Mostrar a imagem com landmarks faciais
#plt.imshow(pil_image)
#plt.show()
pil_image.show()