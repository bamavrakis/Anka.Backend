

import cv2
import PIL.Image
import face_recognition_models
import numpy as np
import dlib
import os
import pickle
from tqdm import tqdm

face_detector = dlib.get_frontal_face_detector()

predictor_68_point_model = \
    face_recognition_models.pose_predictor_model_location()
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

predictor_5_point_model = \
    face_recognition_models.pose_predictor_five_point_model_location()
pose_predictor_5_point = dlib.shape_predictor(predictor_5_point_model)

cnn_face_detection_model = \
    face_recognition_models.cnn_face_detector_model_location()
cnn_face_detector = dlib.cnn_face_detection_model_v1(cnn_face_detection_model)

face_recognition_model = \
    face_recognition_models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)


def cnt_to_rect(cnt):
    return dlib.rectangle(cnt[0], cnt[1], cnt[2], cnt[3])


def record(camera_path=0):
    try:
        capture = cv2.VideoCapture(int(camera_path))
    except ValueError:
        capture = cv2.VideoCapture(camera_path)
    return capture


def resize(img, percent):
    return cv2.resize(img, (0, 0), fx=percent, fy=percent)


def img_to_rgb(img):
    return img[:, :, ::-1]


def load_image_file(file, mode='RGB'):
    im = PIL.Image.open(file)
    if mode:
        im = im.convert(mode)
    return np.array(im)


def _raw_face_locations(img, number_of_times_to_upsample=3, model="hog"):
    if model == "cnn":
        return cnn_face_detector(img, number_of_times_to_upsample)
    else:
        return face_detector(img, number_of_times_to_upsample)


def _raw_face_landmarks(face_image, face_locations, model="large"):
    if face_locations is None:
        face_locations = _raw_face_locations(face_image)
    else:
        face_locations = [cnt_to_rect(face_location)
                          for face_location in face_locations]
    pose_predictor = pose_predictor_68_point

    if model == "small":
        pose_predictor = pose_predictor_5_point

    return [pose_predictor(face_image,
                           face_location) for face_location in face_locations]


def face_distance(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))

    return np.linalg.norm(face_encodings - face_to_compare, axis=1)


def face_encodings(face_image, known_face_locations=None, num_jitters=100):
    raw_landmarks = _raw_face_landmarks(
        face_image, known_face_locations, model="large")
    return [np.array(face_encoder.compute_face_descriptor(face_image,
                                                          raw_landmark_set,
                                                          num_jitters))
            for raw_landmark_set in raw_landmarks]


def save_encodings(directory):
    faces = []
    for file in tqdm(os.listdir(directory)):
        filename = os.fsdecode(file)
        if filename == '.DS_Store':
            continue
        faces.append((filename.split('.')[0], face_encodings(
            load_image_file(directory+filename))[0]))
    faces_file = open("school/utils/encodings/faces_names.pickle", "wb")
    pickle.dump(faces, faces_file)
    faces_file.close()


def load_encodings():
    return pickle.load(open("school/utils/encodings/faces_names.pickle", "rb"))
