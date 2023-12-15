import face_recognition
import cv2
import numpy as np

# Obtem a referencia da Webcam
video_capture = cv2.VideoCapture(1)

# Carrega uma imagem de amostra e aprenda como reconhecê-la.
obama_image = face_recognition.load_image_file("Item 02\obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Carrega uma segunda imagem de amostra e aprenda como reconhecê-la.
biden_image = face_recognition.load_image_file("Item 02\joebiden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Cria matrizes de codificações faciais conhecidas e seus nomes
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden"
]

while True:
    # Pega um único quadro de vídeo
    ret, frame = video_capture.read()

    # Converte a imagem da cor BGR (que o OpenCV usa) para a cor RGB (que o face_recognition usa)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Encontra todos os rostos e codificações de rosto no quadro do vídeo
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Percorre cada face neste quadro de vídeo
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Vê se o rosto corresponde ao(s) rosto(s) conhecido(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # Se uma correspondência foi encontrada em known_face_encodings, basta usar a primeira.
        # se True nas correspondências:
            #first_match_index=matches.index(True)
            #nome = known_face_names[first_match_index]

        # Ou, em vez disso, use a face conhecida com a menor distância até a nova face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Desenhe uma caixa ao redor do rosto
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Desenhe uma etiqueta com um nome abaixo da face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Exibe a imagem resultante
    cv2.imshow('Video', frame)

    # Pressione 'q' no teclado para sair!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Solte o identificador da webcam
video_capture.release()
cv2.destroyAllWindows()