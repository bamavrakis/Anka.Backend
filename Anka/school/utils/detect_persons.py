from .utils import *
import face_recognition


def detect_persons(img_data):
    # Al final esto debe recibir la imagen y los encodings realmente
    img = img_data
    if img is None:
        return []

    known_face_encodings = []
    known_face_names = []

    # Ojalá que encodings esté globalmente instanciado
    encodings = load_encodings()

    for (name, encode) in encodings:
        known_face_names.append(name)
        known_face_encodings.append(encode)

    img = resize(img, 0.5)
    rgb_small_frame = img_to_rgb(img)
    ordered_countours = face_recognition.face_locations(img, 1, "cnn")
    if ordered_countours is None:
        return []

    face_encodings = face_recognition.face_encodings(
        rgb_small_frame, ordered_countours)

    face_names = []
    for face_encoding in face_encodings:
        distances = list(face_distance(
            known_face_encodings, face_encoding))
        for _ in range(len(distances)):
            best = min(distances)
            name = known_face_names[distances.index(best)]
            if best <= 0.55 and name not in face_names:
                face_names.append(name)
                distances[distances.index(best)] = 10000
                break

    return face_names


if __name__ == "__main__":
    print(detect_persons('test.jpg'))
