# ASU RoomSense – Real-Time Occupancy Monitoring

A real-time computer vision–powered room occupancy and zone tracking system using YOLOv5 and OpenCV. This system was developed as part of an ASU course project to help university departments optimize space utilization and monitor room usage dynamically.

---

## Objective

Detect and track people entering predefined zones (e.g., entry, help desk) in a closed meeting room, and generate real-time alerts and logs to assist in occupancy planning, capacity management, and staff deployment.

---

## Tools & Technologies

- Python 3.x  
- OpenCV  
- YOLOv5 (pre-trained model)  
- Streamlit (dashboard)  
- CSV logging for occupancy  
- Zone tagging with bounding box logic  

---

## Key Features

-  Real-time person detection using YOLOv5  
-  Dynamic zone mapping (e.g., entry, help_desk)  
-  Occupancy count and CSV log per frame  
-  Alerting logic based on zone thresholds  
-  Streamlit dashboard for real-time demo  

---

## Folder Structure

```
asu-roomsense/
├── code/
│ └── roomsense_live_tracking_zones.py
├── data/
│ └── sample_input_images/
│ ├── 3_person_frame_0.png
│ ├── 2_person_frame_0.png
│ ├── single_frame_50.png
│ └── empty_room_frame_100.png
├── dashboard/
│ └── streamlit_dashboard_demo.png
├── output/
│ └── room_occupancy_log.csv
└── README.md
```


---

##  Sample Detections

| Empty Room | Single Person | Two People | Three People |
|------------|---------------|------------|---------------|
| ![Empty](data/sample_input_images/empty_room_frame_100.png) | ![1](data/sample_input_images/single_frame_50.png) | ![2](data/sample_input_images/2_person_frame_0.png) | ![3](data/sample_input_images/3_person_frame_0.png) |

---

##  Sample Output Log (CSV)

| Frame | Timestamp | Entry Zone | Help Desk Zone | Total Persons |
|-------|-----------|------------|----------------|----------------|
| 100   | 12:03:45  | 0          | 0              | 0              |
| 101   | 12:03:47  | 1          | 1              | 2              |
| ...   | ...       | ...        | ...            | ...            |

---

##  Resume-Ready Description

> Built a real-time occupancy monitoring system using YOLOv5 and OpenCV to detect and track people across multiple room zones. Enabled CSV-based logging, zone tagging, and Streamlit dashboarding for facility managers to analyze space utilization and trigger alerts when thresholds were exceeded.

---

##  Future Enhancements

- Webcam-to-cloud streaming (AWS Lambda or Google Colab)
- Historical occupancy trend analysis
- Dashboard integration with facility booking systems

---



