import cv2
import numpy as np
import time
import logging
import json
from ultralytics import YOLO
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler("traffic_system.log"), logging.StreamHandler()])


class TrafficLightSimulator:
    def __init__(self):
        self.current_state = "red"
        self.lock = Lock()

    def draw_traffic_light(self, frame):
        height, width = frame.shape[:2]
        light_radius = 30
        padding = 20
        light_positions = {
            "red": (width - padding - light_radius, padding + light_radius),
            "yellow": (width - padding - light_radius, padding * 2 + light_radius * 3),
            "green": (width - padding - light_radius, padding * 3 + light_radius * 5)
        }

        for color, (x, y) in light_positions.items():
            cv2.circle(frame, (x, y), light_radius, (50, 50, 50), -1)

        with self.lock:
            active_x, active_y = light_positions[self.current_state]
            color_map = {"red": (0, 0, 255), "yellow": (
                0, 255, 255), "green": (0, 255, 0)}
            cv2.circle(frame, (active_x, active_y), light_radius,
                       color_map[self.current_state], -1)

    def set_light(self, color):
        with self.lock:
            if self.current_state != color:
                self.current_state = color
                logging.info(f"Traffic light changed to {color}")


class TrafficSystem:
    def __init__(self, config):
        self.config = config
        self.model = YOLO(config['model_path'])
        self.traffic_light = TrafficLightSimulator()
        self.vehicle_classes = set(config['vehicle_classes'])
        self.camera = cv2.VideoCapture(config['camera_index'])
        if not self.camera.isOpened():
            raise RuntimeError("Could not open webcam")

        self.frame_queue = deque(maxlen=5)
        self.lock = Lock()
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=2)

    def process_frame(self, frame):
        try:
            small_frame = cv2.resize(
                frame, (640, 480), interpolation=cv2.INTER_LINEAR)
            results = self.model(small_frame, verbose=False)
            vehicle_count = sum(1 for result in results for box in result.boxes if int(
                box.cls[0]) in self.vehicle_classes)
            return vehicle_count
        except Exception as e:
            logging.error(f"Error processing frame: {e}")
            return 0

    def calculate_traffic_state(self, vehicle_count):
        if vehicle_count > self.config['high_traffic_threshold']:
            return 'red', "Heavy traffic, stopping cars"
        elif vehicle_count > self.config['medium_traffic_threshold']:
            return 'yellow', "Moderate traffic, slowing down"
        else:
            return 'green', "Traffic is clear, light is green"

    def run(self):
        self.running = True
        last_state = None
        state_start_time = time.time()
        self.executor.submit(self.capture_frames)

        try:
            while self.running:
                if not self.frame_queue:
                    continue

                with self.lock:
                    frame = self.frame_queue.popleft()

                future = self.executor.submit(self.process_frame, frame)
                vehicle_count = future.result()

                traffic_state, traffic_message = self.calculate_traffic_state(
                    vehicle_count)

                if traffic_state != last_state and time.time() - state_start_time > self.config['min_state_duration']:
                    self.traffic_light.set_light(traffic_state)
                    last_state = traffic_state
                    state_start_time = time.time()
                    logging.info(traffic_message)

                self.traffic_light.draw_traffic_light(frame)
                cv2.putText(frame, f"Vehicles: {vehicle_count}", (
                    20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, traffic_message, (20, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow("Traffic Management System, DevelopersMindset", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            self.shutdown()

    def capture_frames(self):
        while self.running:
            try:
                ret, frame = self.camera.read()
                if not ret:
                    logging.error("Failed to capture frame")
                    break
                with self.lock:
                    self.frame_queue.append(frame)
                time.sleep(0.05)  # Faster frame capture
            except Exception as e:
                logging.error(f"Error capturing frame: {e}")

    def shutdown(self):
        self.running = False
        self.executor.shutdown(wait=True)
        self.camera.release()
        cv2.destroyAllWindows()
        logging.info("System shutdown complete")


if __name__ == "__main__":
    try:
        with open("config.json") as f:
            config = json.load(f)
        traffic_system = TrafficSystem(config)
        traffic_system.run()
    except Exception as e:
        logging.error(f"Failed to start system: {e}")
