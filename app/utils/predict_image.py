from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import os


def predict_image(image_path):
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model(os.path.abspath("app/keras_model/model_4_v3.h5"), compile=False)

    # Load the labels
    class_names = open(os.path.abspath("app/keras_model/labels.txt"), "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 48, 48), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(image_path).convert("L")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (48, 48)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    # print("Class:", class_name[2:], end="")
    # print("Confidence Score:", confidence_score)

    result = {
        "mood": class_name[2:].replace("\n", ""),
        "confidence_score": float(confidence_score),
    }

    return result
