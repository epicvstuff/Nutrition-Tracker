import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# ----------------------
# Configuration Settings
# ----------------------

# Base directory where dataset folders are located.
BASE_DIR = "archive"  # Update this to your dataset's folder if needed

# Define paths for train, validation, and test directories.
TRAIN_DIR = os.path.join(BASE_DIR, "train")
VALIDATION_DIR = os.path.join(BASE_DIR, "validation")
TEST_DIR = os.path.join(BASE_DIR, "test")  # Optional: used for final evaluation

# Hyperparameters for image processing and training
IMG_WIDTH, IMG_HEIGHT = 150, 150  # Adjust image dimensions if necessary
BATCH_SIZE = 32
EPOCHS = 25

# Seed for reproducibility
SEED = 42

# --------------------------
# Data Preparation & Augmentation
# --------------------------

# For the training set, we use data augmentation to enhance generalization.
train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# For validation and testing, we only normalize the images.
test_val_datagen = ImageDataGenerator(rescale=1.0/255.0)

# Create the training data generator from the TRAIN_DIR.
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',   # categorical for multi-class classification
    seed=SEED
)

# Create the validation data generator from the VALIDATION_DIR.
validation_generator = test_val_datagen.flow_from_directory(
    VALIDATION_DIR,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    seed=SEED
)

# Optional: Create a test data generator from the TEST_DIR.
test_generator = test_val_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False  # For evaluation, it's usually best to keep the order
)

# Determine number of classes automatically from the training data
num_classes = len(train_generator.class_indices)
print("Number of classes:", num_classes)

# --------------------------
# Build the CNN Model
# --------------------------
model = Sequential([
    # First convolutional block
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    MaxPooling2D(pool_size=(2, 2)),

    # Second convolutional block
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    # Third convolutional block
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    # Flattening layer to convert 3D feature maps to a 1D feature vector
    Flatten(),

    # Dropout layer to reduce overfitting
    Dropout(0.5),

    # Dense layer for further feature extraction
    Dense(512, activation='relu'),

    # Output layer with softmax activation for multi-class classification
    Dense(num_classes, activation='softmax')
])

# Display the model summary for quick inspection
model.summary()

# --------------------------
# Compile the Model
# --------------------------
model.compile(
    optimizer=Adam(),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# --------------------------
# Train the Model
# --------------------------
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE,
    epochs=EPOCHS
)

# --------------------------
# Save the Trained Model
# --------------------------
model.save("fruit_vegetable_classifier.h5")
print("Model saved as fruit_vegetable_classifier.h5")

# --------------------------
# Optional: Evaluate on the Test Set
# --------------------------
test_loss, test_accuracy = model.evaluate(test_generator, steps=test_generator.samples // BATCH_SIZE)
print("Test Loss: {:.4f}, Test Accuracy: {:.4f}".format(test_loss, test_accuracy))

# --------------------------
# Plot Training History
# --------------------------
# Plot accuracy history
plt.figure(figsize=(8, 4))
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Plot loss history
plt.figure(figsize=(8, 4))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()
