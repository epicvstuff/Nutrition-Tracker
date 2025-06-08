import os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

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

# Create the training dataset with augmentation
train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE
)

# Create the validation dataset
val_ds = tf.keras.utils.image_dataset_from_directory(
    VALIDATION_DIR,
    seed=SEED,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE
)

# Create the test dataset (if exists)
try:
    test_ds = tf.keras.utils.image_dataset_from_directory(
        TEST_DIR,
        seed=SEED,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        shuffle=False
    )
    has_test_data = True
except:
    print("No test directory found, skipping test evaluation.")
    has_test_data = False

# Get number of classes
class_names = train_ds.class_names
num_classes = len(class_names)
print("Number of classes:", num_classes)
print("Class names:", class_names)

# Normalize pixel values and apply data augmentation
normalization_layer = tf.keras.layers.Rescaling(1./255)

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
])

# Apply normalization and augmentation
def prepare_ds(ds, shuffle=False, augment=False):
    # Normalize pixel values
    ds = ds.map(lambda x, y: (normalization_layer(x), y), num_parallel_calls=tf.data.AUTOTUNE)
    
    if shuffle:
        ds = ds.shuffle(1000)
    
    # Apply data augmentation
    if augment:
        ds = ds.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=tf.data.AUTOTUNE)
    
    # Use buffered prefetching
    return ds.prefetch(buffer_size=tf.data.AUTOTUNE)

train_ds = prepare_ds(train_ds, shuffle=True, augment=True)
val_ds = prepare_ds(val_ds)
if has_test_data:
    test_ds = prepare_ds(test_ds)

# --------------------------
# Build the CNN Model
# --------------------------
model = tf.keras.Sequential([
    # First convolutional block
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Second convolutional block
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Third convolutional block
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Flattening layer to convert 3D feature maps to a 1D feature vector
    tf.keras.layers.Flatten(),

    # Dropout layer to reduce overfitting
    tf.keras.layers.Dropout(0.5),

    # Dense layer for further feature extraction
    tf.keras.layers.Dense(512, activation='relu'),

    # Output layer with softmax activation for multi-class classification
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

# Display the model summary for quick inspection
model.summary()

# --------------------------
# Compile the Model
# --------------------------
model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# --------------------------
# Train the Model
# --------------------------
history = model.fit(
    train_ds,
    validation_data=val_ds,
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
if has_test_data:
    test_loss, test_accuracy = model.evaluate(test_ds)
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
