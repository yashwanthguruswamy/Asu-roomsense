import cv2
import torch
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# --- SETUP ---
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.classes = [0]  # Only detect people

cap = cv2.VideoCapture(0)
log = []

print("🎥 Starting real-time people tracking with zone monitoring...")
print("🔴 Press 'q' to stop monitoring.")

# Define zones (example)
zones = {
    'entry': [(0, 0), (300, 480)],
    'help_desk': [(300, 0), (640, 480)]
}

def get_zone(person_box, zones):
    x_center = (person_box[0] + person_box[2]) / 2
    y_center = (person_box[1] + person_box[3]) / 2
    for name, ((x1, y1), (x2, y2)) in zones.items():
        if x1 <= x_center <= x2 and y1 <= y_center <= y2:
            return name
    return 'unknown'

THRESHOLD = 5  # overall people threshold
os.makedirs("snapshots", exist_ok=True)
frame_counter = 0

# --- LIVE MONITORING LOOP ---
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera error. Exiting.")
        break

    results = model(frame)
    boxes = results.xyxy[0].cpu().numpy()
    people_count = len(boxes)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    zone_counts = {}
    for box in boxes:
        zone = get_zone(box[:4], zones)
        zone_counts[zone] = zone_counts.get(zone, 0) + 1

    # Draw zones
    for name, ((x1, y1), (x2, y2)) in zones.items():
        cv2.rectangle(results.ims[0], (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(results.ims[0], name, (x1 + 5, y1 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Alert if over threshold
    if people_count > THRESHOLD:
        cv2.putText(results.ims[0], "⚠️ ALERT: Over Capacity!", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        if frame_counter % 10 == 0:
            snapshot_alert = f"snapshots/alert_frame_{frame_counter}.png"
            cv2.imwrite(snapshot_alert, results.ims[0])

    # Render and show
    results.render()
    cv2.imshow("🔴 ASU RoomSense Live Feed (Zones)", results.ims[0])

    # Save some snapshots every 50 frames
    if frame_counter % 50 == 0:
        snapshot_path = f"snapshots/frame_{frame_counter}.png"
        cv2.imwrite(snapshot_path, results.ims[0])

    # Log
    log.append({'time': timestamp, 'count': people_count, 'zones': zone_counts})

    frame_counter += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("📝 Saving log data...")
df = pd.DataFrame(log)
df.to_csv("live_tracking_zone_log.csv", index=False)
print("✅ Log saved as live_tracking_zone_log.csv")

# --- POST ANALYSIS ---
print("📊 Generating analysis charts...")

# Load saved log
df['time'] = pd.to_datetime(df['time'])

# Plot occupancy over time
plt.figure(figsize=(12,5))
plt.plot(df['time'], df['count'], marker='o', linestyle='-')
plt.title("👥 Room Occupancy Over Time with Zone Monitoring")
plt.xlabel("Time")
plt.ylabel("Number of People")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Basic stats
print("\n📋 Summary Statistics:")
print(df['count'].describe())
