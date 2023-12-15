# app.py

import time

import cv2

from scripts.face_recognition_scripts import (carregar_alunos,
                                              carregar_banco_dados,
                                              carregar_scripts)


def main():
    mydb, mycursor = carregar_banco_dados()
    alunos = carregar_alunos()

    fr = None
    registros_feitos = set()
    na_area_verde = set()
    na_area_vermelha = set()
    entradas_registradas = {}
    saidas_registradas = {}
    time_interval = 7200

    cap = cv2.VideoCapture(1)

    try:
        while True:

            ret, frame = cap.read()

            if not ret:
                print("Erro ao capturar os frames")
                break

            fr, mydb, mycursor, alunos, registros_feitos, na_area_verde, na_area_vermelha, entradas_registradas, saidas_registradas, time_interval = carregar_scripts(
                frame,
                mydb,
                mycursor,
                alunos,
                registros_feitos,
                na_area_verde,
                na_area_vermelha,
                entradas_registradas,
                saidas_registradas,
                time_interval)

            cv2.imshow('video', fr)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if cv2.getWindowProperty('video', cv2.WND_PROP_VISIBLE) < 1:
                break

            if cv2.waitKey(1) == 27:
                break

            time.sleep(0.01)

    except KeyboardInterrupt:
        print('Script parado manualmente')
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
