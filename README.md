# Gesture-Based Volume Control

A computer vision project that controls Windows system volume using hand gestures. Built with Python, OpenCV, MediaPipe, NumPy, and Pycaw.

## Features

- Real-time hand tracking using a webcam
- Detection of thumb and index fingertip landmarks
- Calculates the distance between fingertips
- Maps finger distance to system volume
- Displays the volume percentage on the webcam feed
- Supports intuitive, contactless volume control

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Pycaw
- Comtypes

## How It Works

1. The webcam captures video frames.
2. MediaPipe detects hand landmarks.
3. The distance between the thumb tip and index fingertip is calculated.
4. The distance is mapped to the available system volume range.
5. Pycaw adjusts the Windows system volume.
6. The current volume percentage is displayed on the screen.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

Run the Python script from your project directory:

```bash
python VolumeHandControl.py
```

Move your thumb and index finger apart to increase the volume, or bring them closer together to decrease it.

Press `q` to exit the webcam window.

## Requirements

- Windows operating system
- Python installed
- Working webcam
- Compatible audio output device
- Compatible Python and MediaPipe versions

## Project Structure

```text
Gesture-Volume-Control/
├── VolumeHandControl.py
├── README.md
└── requirements.txt
```

## Notes

- This project uses Pycaw to control Windows system audio.
- The gesture-to-volume mapping depends on fingertip distance and may require calibration.
- Audio-device compatibility may vary.
- The project should be tested on the target computer before use.

## Author

Developed as a computer vision and gesture-control learning project.
