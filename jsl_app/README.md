# Japanese Sign Language (JSL) Recognition using OpenCV & MediaPipe

## Overview

This project implements a Japanese Sign Language (JSL) recognition system using OpenCV and MediaPipe. It utilizes computer vision techniques to detect hand gestures and keypoints, enabling real-time sign language interpretation.

## Features

- **Hand Tracking**: Uses MediaPipe Hands to detect and track hand landmarks.
- **Gesture Recognition**: Maps detected landmarks to predefined JSL gestures.
- **Real-time Processing**: Implements OpenCV for efficient video frame capture and processing.
- **Model Integration**: Supports custom models trained for JSL recognition.

## Requirements

Ensure you have the following dependencies installed:

```bash
pip install opencv-python mediapipe numpy tensorflow pandas scikit-learn uv
```

Supports Python 3.12.

## Usage

Run the hand detection script:

```bash
python hand_detect.py
```

### Model Training

To train a custom JSL recognition model:

1. Collect hand landmark data using `hand_create_csv.py`.
2. Train the model using `hand_train.ipynb`.
3. Save and integrate the trained model into `hand_detect.py`.

## Directory Structure

- `hand_create_csv.py` - Script for collecting hand landmark data.
- `hand_detect.py` - Script for detecting hand gestures.
- `hand_train.ipynb` - Notebook for training the recognition model.
- `hand_gesture_data.csv` - Dataset for training the model.
- `hand_gesture_model.tflite` - Trained model for gesture recognition.

## Available hand gestures for the following letters:

"A", "I", "U","E", "o"

## Future Improvements

- Expand gesture dataset to cover more JSL signs.

## Acknowledgments

- [OpenCV](https://opencv.org/)
- [MediaPipe](https://developers.google.com/mediapipe/)
- [I made a fork from this project](https://github.com/Thomas9363/How-to-Train-Custom-Hand-Gestures-Using-Mediapipe/tree/main)
