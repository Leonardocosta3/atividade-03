import face_recognition
from PIL import Image, ImageDraw

# Carregue a imagem com as faces
image_path = 'Item 02\obama.jpg'
image = face_recognition.load_image_file(image_path)

# Encontre todas as faces na imagem
face_locations = face_recognition.face_locations(image)

# Abra a imagem usando PIL (Python Imaging Library)
pil_image = Image.open(image_path)

# Crie um objeto de desenho
draw = ImageDraw.Draw(pil_image)

# Desenhe um retângulo em volta de cada rosto encontrado
for face_location in face_locations:
    top, right, bottom, left = face_location
    draw.rectangle([left, top, right, bottom], outline="green", width=4)

# Mostra a imagem com as faces destacadas
pil_image.show()
