# -*- coding: utf-8 -*-
"""20217011-20215016-20216094-20216129

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qGm9ZyE7GxUqo8G0-ECjKA0KBxpCqjaW

# Deep Learning Libraries
"""

from google.colab import drive
drive.mount('/content/drive')

pip install numpy opencv-python tensorflow matplotlib seaborn scikit-learn

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import cv2

# Deep Learning Libraries
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, regularizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16, ResNet50
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

"""#  1. Loadtheimages.
# 2. Discard images that correspond to ages outside the range [10, 90].
"""

def load_and_preprocess_data(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall('dataset')

    images = []
    ages = []

    dataset_folder ="/content/drive/MyDrive/FCAI /utkcropped"

    # Walk through extracted directory
    for filename in os.listdir(dataset_folder):
        if filename.endswith('.jpg'):
            parts = filename.split('_')
            try:
                age = int(parts[0])

                if 10 <= age <= 90:
                    img_path = os.path.join(dataset_folder, filename)
                    img = cv2.imread(img_path)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, (64, 64))

                    images.append(img)
                    ages.append(age)
            except ValueError:
                continue

    X = np.array(images) / 255.0
    y = np.array(ages)

    return X, y

"""## Pre Model"""

# Split the data
def split_data(X, y, test_size=0.2, val_size=0.2):
    from sklearn.model_selection import train_test_split

    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_size, random_state=42
    )

    return X_train, X_val, X_test, y_train, y_val, y_test

def train_model(model, X_train, y_train, X_val, y_val, data_augmentation=None):
    # Callbacks
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )

    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=3,
        min_lr=0.00001
    )

    # Training
    if data_augmentation:
        history = model.fit(
            data_augmentation.flow(X_train, y_train, batch_size=32),
            validation_data=(X_val, y_val),
            epochs=10,
            callbacks=[early_stopping, reduce_lr]
        )
    else:
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=20,
            batch_size=32,
            callbacks=[early_stopping, reduce_lr]
        )

    return history

def plot_training_history(histories, model_names):
    plt.figure(figsize=(15, 5))

    # Training Loss
    plt.subplot(1, 2, 1)
    for history, name in zip(histories, model_names):
        plt.plot(history.history['loss'], label=f'{name} Training Loss')
        plt.plot(history.history['val_loss'], label=f'{name} Validation Loss')

    plt.title('Model Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.tight_layout()
    plt.show()

"""# Two large convolutional neural network (CNN) models with custom architectures.

## Modle 1
"""

# Custom CNN Model 1: Deep CNN
def create_deep_cnn_model1(input_shape=(64, 64, 3)):
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape,
                      kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(64, (3, 3), activation='relu',
                      kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(128, (3, 3), activation='relu',
                      kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),
        layers.Dense(256, activation='relu',
                     kernel_regularizer=regularizers.l2(0.001)),
        layers.Dropout(0.5),
        layers.Dense(1, activation='linear')
    ])

    model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['mae'])
    return model

def main():
    zip_file_path = "/content/drive/MyDrive/FCAI /DL_Assignment 1.zip"
    X, y = load_and_preprocess_data(zip_file_path)

    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)

    model = create_deep_cnn_model1()
    history = train_model(model, X_train, y_train, X_val, y_val)

    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    # Evaluate Model
    test_loss, test_mae = model.evaluate(X_test, y_test)
    print(f"Test Mean Absolute Error: {test_mae}")

main()

"""## Modle 2"""

def create_deep_cnn_model2(input_shape=(64, 64, 3)):
    model = models.Sequential([
        layers.Conv2D(64, (3, 3), activation='relu', input_shape=input_shape,
                      kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(128, (3, 3), activation='relu',
                      kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(256, (3, 3), activation='relu',
                      kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(512, (3, 3), activation='relu',
                      kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),
        layers.Dense(1024, activation='relu',
                     kernel_regularizer=regularizers.l2(0.001)),
        layers.Dropout(0.5),
        layers.Dense(1, activation='linear')
    ])

    model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['mae'])
    return model

def main1():

    zip_file_path = "/content/drive/MyDrive/FCAI /DL_Assignment 1.zip"
    X, y = load_and_preprocess_data(zip_file_path)

    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)

    model = create_deep_cnn_model2()
    history = train_model(model, X_train, y_train, X_val, y_val)

    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    test_loss, test_mae = model.evaluate(X_test, y_test)
    print(f"Test Mean Absolute Error: {test_mae}")

main1()

"""#Two smaller models that apply transfer learning by taking the features  extracted by a base CNN model of a well-known architecture as their input, and learning to leverage these features for the age estimation task.

# ResNet50
"""

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, regularizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16, ResNet50
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

def load_and_preprocess_data(zip_file_path):

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall('dataset')

    images = []
    ages = []

    dataset_folder =r"/content/drive/MyDrive/FCAI /utkcropped"

    for filename in os.listdir(dataset_folder):
        if filename.endswith('.jpg'):
            parts = filename.split('_')
            try:
                age = int(parts[0])
                if 10 <= age <= 90:
                    img_path = os.path.join(dataset_folder, filename)
                    img = cv2.imread(img_path)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, (64, 64))

                    images.append(img)
                    ages.append(age)
            except ValueError:
                continue

    X = np.array(images) / 255.0
    y = np.array(ages)

    return X, y

def create_transfer_learning_model2(input_shape=(64, 64, 3)):
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)

    model = models.Sequential([
        base_model,
        layers.Flatten(),
        layers.Dense(512, activation='relu',
                     kernel_regularizer=regularizers.l2(0.001)),
        layers.Dropout(0.6),
        layers.Dense(1, activation='linear')
    ])

    model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['mae'])
    return model

def split_data(X, y, test_size=0.2, val_size=0.2):
    from sklearn.model_selection import train_test_split

    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_size, random_state=42
    )

    return X_train, X_val, X_test, y_train, y_val, y_test

def train_model(model, X_train, y_train, X_val, y_val, data_augmentation=None):
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )

    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=2,
        min_lr=1e-6
    )

    if data_augmentation:
        history = model.fit(
            data_augmentation.flow(X_train, y_train, batch_size=32),
            validation_data=(X_val, y_val),
            epochs=10,
            callbacks=[early_stopping, reduce_lr]
        )
    else:
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=50,
            batch_size=32,
            callbacks=[early_stopping, reduce_lr]
        )

    return history

def main3():
    zip_file_path = r"/content/drive/MyDrive/FCAI /DL_Assignment 1.zip"
    X, y = load_and_preprocess_data(zip_file_path)

    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)

    model = create_transfer_learning_model2()
    history = train_model(model, X_train, y_train, X_val, y_val)

    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    test_loss, test_mae = model.evaluate(X_test, y_test)
    print(f"Test Mean Absolute Error: {test_mae}")

    model.save("age_prediction_model.h5")
    print("Model saved as 'age_prediction_model.h5'.")

main3()



"""# VGG16"""

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, regularizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

def load_and_preprocess_data(zip_file_path):

    images = []
    ages = []

    dataset_folder ='/content/drive/MyDrive/faces/utkcropped'

    for filename in os.listdir(dataset_folder):
        if filename.endswith('.jpg'):

            parts = filename.split('_')
            try:
                age = int(parts[0])

                if 10 <= age <= 90:
                    img_path = os.path.join(dataset_folder, filename)
                    img = cv2.imread(img_path)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, (64, 64))

                    images.append(img)
                    ages.append(age)
            except ValueError:
                continue

    X = np.array(images) / 255.0
    y = np.array(ages)

    return X, y

def create_transfer_learning_model1(input_shape=(64, 64, 3)):
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)

    model = models.Sequential([
        base_model,
        layers.Flatten(),
        layers.Dense(256, activation='relu',
                     kernel_regularizer=regularizers.l2(0.001)),
        layers.Dropout(0.5),
        layers.Dense(1, activation='linear')
    ])

    model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['mae'])
    return model


def split_data(X, y, test_size=0.2, val_size=0.2):
    from sklearn.model_selection import train_test_split

    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_size, random_state=42
    )

    return X_train, X_val, X_test, y_train, y_val, y_test

def train_model(model, X_train, y_train, X_val, y_val, data_augmentation=None):

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )

    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=2,
        min_lr=1e-6
    )

    if data_augmentation:
        history = model.fit(
            data_augmentation.flow(X_train, y_train, batch_size=32),
            validation_data=(X_val, y_val),
            epochs=10,
            callbacks=[early_stopping, reduce_lr]
        )
    else:
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=50,
            batch_size=32,
            callbacks=[early_stopping, reduce_lr]
        )

    return history

def main2():
    # Load Data
    zip_file_path = '/content/drive/MyDrive/faces/utkcropped'
    X, y = load_and_preprocess_data(zip_file_path)

    # Split Data
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)

    # Create and Train Model
    model = create_transfer_learning_model1()
    history = train_model(model, X_train, y_train, X_val, y_val)

    # Plot Training History
    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    # Evaluate Model
    test_loss, test_mae = model.evaluate(X_test, y_test)
    print(f"Test Mean Absolute Error: {test_mae}")
    model.save("age_prediction_model.h5")
    print("Model saved as 'age_prediction_model.h5'")

main2()

"""# 8. Select the best model, use it to make age predictions on face images of your team, and plot these images with the estimated ages."""

import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

def predict_and_visualize(model_path, image_paths):

    model = tf.keras.models.load_model(model_path)

    images = []
    valid_image_paths = []

    for img_path in image_paths:
        if not os.path.exists(img_path):
            print(f"Image not found: {img_path}")
            continue
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load image: {img_path}")
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (64, 64))
        images.append(img)
        valid_image_paths.append(img_path)

    if not images:
        print("No valid images to process.")
        return

    images = np.array(images) / 255.0

    predictions = model.predict(images)
    predicted_ages = predictions.flatten()

    plt.figure(figsize=(12, 6))
    for i, img in enumerate(images):
        plt.subplot(1, len(images), i + 1)
        plt.imshow(img)
        plt.title(f"Predicted Age: {int(predicted_ages[i])}")
        plt.axis('off')
    plt.show()

image_paths = [
"/content/Menna.jpg",
    "/content/Mariam.jpg",
    "/content/jana.jpg",
    "/content/Zaynab.jpg"
]

predict_and_visualize("age_prediction_model.h5",image_paths)



"""# VGG16"""

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, regularizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import os  # Import the os module
from tensorflow.keras.applications import VGG16, ResNet50
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import cv2

# Deep Learning Libraries
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, regularizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16, ResNet50
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
def load_and_preprocess_data(zip_file_path):

    images = []
    ages = []

    dataset_folder ='/content/drive/MyDrive/FCAI /utkcropped'

    for filename in os.listdir(dataset_folder):
        if filename.endswith('.jpg'):

            parts = filename.split('_')
            try:
                age = int(parts[0])

                if 10 <= age <= 90:
                    img_path = os.path.join(dataset_folder, filename)
                    img = cv2.imread(img_path)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, (64, 64))

                    images.append(img)
                    ages.append(age)
            except ValueError:
                continue

    X = np.array(images) / 255.0
    y = np.array(ages)

    return X, y

def create_transfer_learning_model1(input_shape=(64, 64, 3)):
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)

    model = models.Sequential([
        base_model,
        layers.Flatten(),
        layers.Dense(256, activation='relu',
                     kernel_regularizer=regularizers.l2(0.001)),
        layers.Dropout(0.5),
        layers.Dense(1, activation='linear')
    ])

    model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['mae'])
    return model


def split_data(X, y, test_size=0.2, val_size=0.2):
    from sklearn.model_selection import train_test_split

    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_size, random_state=42
    )

    return X_train, X_val, X_test, y_train, y_val, y_test

def train_model(model, X_train, y_train, X_val, y_val, data_augmentation=None):

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )

    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=2,
        min_lr=1e-6
    )

    if data_augmentation:
        history = model.fit(
            data_augmentation.flow(X_train, y_train, batch_size=32),
            validation_data=(X_val, y_val),
            epochs=10,
            callbacks=[early_stopping, reduce_lr]
        )
    else:
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=50,
            batch_size=32,
            callbacks=[early_stopping, reduce_lr]
        )

    return history

import cv2 # Import the OpenCV library
import numpy as np #Import the numpy Library

def main2():
    # Load Data
    zip_file_path = '/content/drive/MyDrive/FCAI /DL_Assignment 1.zip'
    X, y = load_and_preprocess_data(zip_file_path)

    # Split Data
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)

    # Create and Train Model
    model = create_transfer_learning_model1()
    history = train_model(model, X_train, y_train, X_val, y_val)

    # Plot Training History
    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    # Evaluate Model
    test_loss, test_mae = model.evaluate(X_test, y_test)
    print(f"Test Mean Absolute Error: {test_mae}")
    model.save("age_prediction_model.h5")
    print("Model saved as 'age_prediction_model.h5'")

main2()

import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

def predict_and_visualize(model_path, image_paths):

    model = tf.keras.models.load_model(model_path)

    images = []
    valid_image_paths = []

    for img_path in image_paths:
        if not os.path.exists(img_path):
            print(f"Image not found: {img_path}")
            continue
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load image: {img_path}")
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (64, 64))
        images.append(img)
        valid_image_paths.append(img_path)

    if not images:
        print("No valid images to process.")
        return

    images = np.array(images) / 255.0

    predictions = model.predict(images)
    predicted_ages = predictions.flatten()

    plt.figure(figsize=(12, 6))
    for i, img in enumerate(images):
        plt.subplot(1, len(images), i + 1)
        plt.imshow(img)
        plt.title(f"Predicted Age: {int(predicted_ages[i])}")
        plt.axis('off')
    plt.show()

image_paths = [
"/content/Menna.jpg",
    "/content/Mariam.jpg",
    "/content/Jana.jpg",
    "/content/Zaynab.jpg"
]

predict_and_visualize("age_prediction_model.h5",image_paths)

