import face_recognition
known_image = face_recognition.load_image_file("Item 02\obama.jpg")
unknown_image = face_recognition.load_image_file("Item 02\joebiden.jpg")

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

if results[0]:
    print("Os rostos são iguais!")
else:
    print("Os rostos são diferentes.")
