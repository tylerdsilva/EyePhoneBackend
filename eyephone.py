import json
import os
import cv2
from flask import Flask
from flask_cors import CORS
from ellipse import computeEllipse
from metrics import computeMetrics
from model import unet
import tensorflow as tf
import numpy as np
from skimage.transform import resize
from tensorflow.keras.models import Model, load_model

firebaseConfig = {
    "apiKey": "AIzaSyA7_Vtd1KtxTNsVphWKB6MmU1uOrR1LPU8",
    "authDomain": "eyephone-51d80.firebaseapp.com",
    "projectId": "eyephone-51d80",
    "storageBucket": "eyephone-51d80.appspot.com",
    "messagingSenderId": "745363148986",
    "appId": "1:745363148986:web:286daba9bf395f0f3f7283",
    "measurementId": "G-3GXCPPEFC8",
    "databaseURL": "gs://eyephone-51d80.appspot.com/"
}


IMG_HEIGHT = 128
IMG_WIDTH = 128
IMG_CHANNELS = 1


def prediction(imagePath):
    img = cv2.imread(imagePath, 0)
    img = cv2.equalizeHist(img)
    height, width = np.shape(img)[0:2]
    img = np.expand_dims(resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True), axis=-1)
    x_test = np.zeros((1, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
    # testimg=resize(img,(self.IMG_HEIGHT,self.IMG_WIDTH),mode='constant',preserve_range=True)
    x_test[0] = img
    model = unet()
    model.load_weights('model-dsbowl2018-1.h5')
    model.compile(optimizer='adam', loss='binary_crossentropy',
                  metrics=["accuracy", tf.keras.metrics.MeanIoU(num_classes=2)])
    preds_test = model.predict(x_test, verbose=1)

    preds_test_t = (preds_test > 0.4).astype(np.uint8)
    squeezed_pred = np.squeeze(preds_test_t[0])
    reshaped_pred = resize(squeezed_pred, (height, width), mode='constant', preserve_range=True)
    reshaped_pred = reshaped_pred * 255
    print(np.shape(reshaped_pred))
    cv2.imwrite("mask.png", reshaped_pred)


# @app.route('/metrics/', methods=['POST'])
def process_audio():
    FILE_OUTPUT = 'output.avi'

    # data = request.get_data()
    # data_length = request.content_length
    #
    # if data_length > 1024 * 1024 * 10:
    #     return 'File too large!', 400
    #
    # # process data here:
    # print("Processing data: ", data)

    # # Checks and deletes the output file
    # # You cant have a existing file or it will through an error
    # if os.path.exists(FILE_OUTPUT):
    #     os.remove(FILE_OUTPUT)
    #
    # # opens the file 'output.avi' which is accessible as 'out_file'
    # with open(FILE_OUTPUT, "wb") as out_file:  # open for [w]riting as [b]inary
    #     out_file.write(data)
    # out_file.close()

    # convert video to images, stored in image frames folder
    vidcap = cv2.VideoCapture('2.avi')
    success, image = vidcap.read()
    count = 0
    frameCount = []
    imageFrames = []
    width, height = 0, 0

    while success:
        success, image = vidcap.read()
        count += 1
        if not image is None:
            width, height = np.shape(image)[0:2]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.equalizeHist(image)
            image = np.expand_dims(resize(image, (128, 128), mode='constant', preserve_range=True), axis=-1)
            imageFrames.append(image)
            frameCount.append(count)

    set = np.zeros((len(imageFrames), 128, 128, 1), dtype=np.uint8)
    for i in range(0, len(imageFrames)):
        set[i] = imageFrames[i]
    ### Compute Metrics
    # masks from ML, assume to be binary data e.g. cv2.imread(file, 0)
    lmodel = unet()
    print(np.shape(imageFrames))
    print(np.shape(set))
    preds_test = lmodel.predict(set, verbose=1)
    masks = (preds_test > 0.4).astype(np.uint8)
    masks = masks * 255
    # preds = []
    squeezed_mask = np.squeeze(masks)
    preds = np.expand_dims(resize(squeezed_mask, (height, width), mode='constant', preserve_range=True), axis=-1)
    # for i in range(0, len(masks)):
    #     squeezed_mask = np.squeeze(masks[i])
    #     preds.append(resize(squeezed_mask, (height, width), mode='constant', preserve_range=True))

    image_frames = imageFrames
    diameters = computeEllipse(preds)
    print(diameters)

    velocity = computeMetrics(diameters, image_frames)
    print(velocity)

    return json.dumps({"diameter": 50, "constriction_velocity": 30}), 200


process_audio()
print("Done")
