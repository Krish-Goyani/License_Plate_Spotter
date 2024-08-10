from ultralytics import YOLO
import cv2
from sort.sort import *
import numpy as np
from utils.util import get_car, read_license_plate, write_csv



class DetectLicensePlate:
    def __init__(self):
        #loading models
        self.coco_model = YOLO("yolov8n.pt")
        self.license_plate_detector = YOLO("models\license_plate_detector.pt")
        self.vehicles_tracker = Sort()


    def detect_license_plate(self, video_file_path):
        
        results = {}

        #loading the video
        cap = cv2.VideoCapture(video_file_path)

        vehicles_class = [2, 3, 5, 7]

        #read frames
        frame_nbr = -1
        ret = True
        while ret:
            
            frame_nbr = frame_nbr +1
            ret, frame = cap.read()

            if ret:
                results[frame_nbr] = {}
                #detecting vehicles
                detections = self.coco_model(frame)[0]
                detections_ = []
                for detection in detections.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = detection
                    if int(class_id) in vehicles_class:
                        detections_.append([x1, y1, x2, y2, score])


                # track vehicles
                track_ids = self.vehicles_tracker.update(np.asarray(detections_))

                #detect license plate number

                license_plates = self.license_plate_detector(frame)[0]
                for license_plate in license_plates.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = license_plate

                    #assigning license plate with appropriate car
                    xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

                    if car_id != -1:

                        # cropping license plate
                        license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]


                        # processing license plate so we get better result in ocr

                        license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                        _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                        # our license plate crop is pre processde and we can read it using the OCR
                        license_plate_text , license_plate_text_score = read_license_plate(license_plate_crop_thresh)

                        if license_plate_text is not None:
                            results[frame_nbr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                        'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                            'text': license_plate_text,
                                                                            'bbox_score': score,
                                                                            'text_score': license_plate_text_score}}
                            

        # write results
        write_csv(results, './test.csv')

        return "./test.csv"


