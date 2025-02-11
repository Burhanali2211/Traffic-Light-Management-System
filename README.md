# Traffic Light Management System using YOLO and OpenCV

## Overview
This project is a Traffic Light Management System that uses a YOLO-based object detection model and OpenCV to monitor traffic density and dynamically control traffic lights. The system analyzes real-time camera input to detect vehicles and adjust the traffic signals accordingly, improving traffic efficiency.

## Features
- Uses **YOLO (You Only Look Once)** for real-time vehicle detection.
- Implements **OpenCV** for video processing and overlaying traffic light visuals.
- Supports **multi-threading** for smooth processing.
- Detects **traffic congestion levels** and changes traffic lights dynamically.
- Displays **real-time vehicle count** and traffic status messages.
- Logs system events for debugging and monitoring.

## Technologies Used
- **Python**
- **OpenCV** (for image processing and video capture)
- **YOLO (Ultralytics)** (for object detection)
- **Threading & ThreadPoolExecutor** (for parallel processing)
- **Logging & JSON Configuration**

## System Requirements
- Python 3.7+
- OpenCV (`opencv-python`)
- Ultralytics YOLO (`ultralytics`)
- NumPy
- A webcam (or a pre-recorded video feed for testing)

## Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/Burhanali2211/Traffic-Light-Management-System.git
   cd traffic-light-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download YOLO model**
   Download a YOLO model (e.g., `yolov8n.pt`) from [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) and place it in the project directory.

4. **Modify `config.json`**
   Configure settings like camera index, model path, and traffic thresholds.

## Configuration (`config.json`)
```json
{
  "model_path": "yolov8n.pt",
  "camera_index": 0,
  "vehicle_classes": [2, 3, 5, 7],
  "high_traffic_threshold": 10,
  "medium_traffic_threshold": 5,
  "min_state_duration": 5
}
```
- **vehicle_classes**: Object classes representing vehicles (YOLO classes: car=2, motorbike=3, bus=5, truck=7)
- **high_traffic_threshold**: Number of vehicles required to trigger red light
- **medium_traffic_threshold**: Number of vehicles required to trigger yellow light
- **min_state_duration**: Minimum duration before switching traffic lights

## Usage
Run the script using:
```bash
python app.py
```
- Press `q` to exit the program.

## How It Works
1. Captures video frames from the camera.
2. Processes frames using YOLO to detect vehicles.
3. Counts detected vehicles and determines traffic congestion level.
4. Changes the traffic light state based on congestion.
5. Overlays traffic light visuals and vehicle count on the video feed.
6. Displays the live feed with updated traffic conditions.

## Demo
Ensure the camera is connected and configured properly in `config.json`. When running, the system will:
- **Show the live feed** with a traffic light overlay.
- **Update traffic lights** dynamically based on vehicle count.
- **Log status messages** for debugging.

## Logging
Logs are saved in `traffic_system.log` for tracking events and debugging issues.

## Future Improvements
- Integrate with **Raspberry Pi** for real-world deployment.
- Use **multiple cameras** for large-scale traffic management.
- Enhance **YOLO model** training with a custom dataset for better accuracy.
- Implement **automated reports** based on traffic patterns.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is open-source and available under the [MIT License](LICENSE).

