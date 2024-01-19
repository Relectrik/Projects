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

image_dir = "icons/"

img_width, img_height = 128, 128
batch_size = 8

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

normalization_layer = keras.layers.Rescaling(1.0 / 255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixel values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))

# AUTOTUNE = tf.data.AUTOTUNE

# train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
# val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

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

model.fit(train_ds, validation_data=val_ds, epochs=3)

# split_ratio = 0.8

# split_index = int(split_ratio * len(all_images))

# train_images = all_images[:split_index]
# validation_images = all_images[split_index:]

# train_datagen = ImageDataGenerator(
#     rescale=1.0 / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True
# )

# validation_datagen = ImageDataGenerator(rescale=1 / 255)

# train_generator = train_datagen.flow_from_list(
#     [os.path.join(image_dir, file) for file in train_images],
#     target_size=(img_width, img_height),
#     batch_size=batch_size,
#     class_mode="categorical",  # Use categorical for multi-class classification
#     labels=labels,
#     label_func=extract_labels(file),
# )

# validation_generator = validation_datagen.flow_from_list(
#     [os.path.join(image_dir, file) for file in validation_images],
#     target_size=(img_width, img_height),
#     batch_size=batch_size,
#     class_mode="categorical",
#     labels=labels,
#     label_func=extract_labels(file),
# )
