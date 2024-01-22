import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
import os
import random

import keras
from keras import layers
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from sklearn.preprocessing import LabelEncoder

image_dir = "icons/"

img_width, img_height = 128, 128
batch_size = 1

labels = {"Controller", "Sentinel", "Duelist", "Initiator"}


def extract_labels(file_name):
    for label in labels:
        if label in file_name:
            return label


all_images = os.listdir(image_dir)

random.shuffle(all_images)

train_ds = keras.utils.image_dataset_from_directory(
    f"{image_dir}/training",
    validation_split=0.2,
    subset="training",
    seed=3,
    label_mode="categorical",
    image_size=(img_height, img_width),
    batch_size=batch_size,
)

val_ds = keras.utils.image_dataset_from_directory(
    f"{image_dir}/validation",
    validation_split=0.2,
    subset="validation",
    seed=3,
    label_mode="categorical",
    image_size=(img_height, img_width),
    batch_size=batch_size,
)

label_encoder = LabelEncoder()
train_ds_labels = label_encoder.fit_transform(train_ds.class_names)
val_ds_labels = label_encoder.transform(val_ds.class_names)


train_ds = keras.utils.image_dataset_from_directory(
    f"{image_dir}/training",
    validation_split=0.2,
    subset="training",
    seed=3,
    label_mode="int",  # Change label_mode to "int"
    image_size=(img_height, img_width),
    batch_size=batch_size,
)

val_ds = keras.utils.image_dataset_from_directory(
    f"{image_dir}/validation",
    validation_split=0.2,
    subset="validation",
    seed=3,
    label_mode="int",  # Change label_mode to "int"
    image_size=(img_height, img_width),
    batch_size=batch_size,
)

normalization_layer = keras.layers.Rescaling(1.0 / 255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixel values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

num_classes = 4

model = tf.keras.Sequential(
    [
        tf.keras.layers.Rescaling(1.0 / 255),
        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(num_classes),
    ]
)

model.compile(
    optimizer="adam",
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"],
)

model.fit(train_ds, validation_data=val_ds, epochs=100)

evaluation = model.evaluate(val_ds)

loss, accuracy = evaluation

print(type(evaluation))
print(f"Validation Loss: {loss}")
print(f"Validation Accuracy: {accuracy}")

# Assuming your model is already trained

# Load and preprocess a single image for prediction
image_path = "icons/validation/Sentinel/Sentinel_79.png"
img = keras.preprocessing.image.load_img(
    image_path, target_size=(img_height, img_width)
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Add batch dimension

# Normalize the input image
img_array = normalization_layer(img_array)

# Make predictions
predictions = model.predict(img_array)

# Get the predicted class index
predicted_class_index = np.argmax(predictions)

# Decode the predicted class index to the original label
predicted_label = label_encoder.inverse_transform([predicted_class_index])[0]

# Print the results
print(f"Predicted Class Index: {predicted_class_index}")
print(f"Predicted Label: {predicted_label}")
