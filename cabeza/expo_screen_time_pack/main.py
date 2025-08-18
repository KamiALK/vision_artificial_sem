import cv2, time, csv, uuid
from datetime import datetime
from ultralytics import YOLO
from utils.screen_roi import select_polygon_roi, polygon_center, inside_polygon
from models.gaze import HeadPose
from storage.mongo_writer import save_session

def direction_to_roi(face_center, roi_center):
    dx = roi_center[0] - face_center[0]
    return 1 if dx > 0 else -1

def run(source=0, model_path='yolov8n.pt', conf=0.5, yaw_thresh=15.0, show=True, save_csv=True):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir la fuente: {source}")
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("No hay frames.")
    roi = select_polygon_roi(frame)
    if roi is None:
        print("No se definió ROI; saliendo.")
        return

    roi_center = polygon_center(roi)
    tracker_model = YOLO(model_path)
    head_pose = HeadPose()

    totals = {}
    last_time = time.time()
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    print("Sesión:", session_id)

    for result in tracker_model.track(source=source, stream=True, conf=conf, classes=[0], tracker='bytetrack.yaml'):
        frame = result.orig_img.copy()
        now = time.time()
        dt = now - last_time
        last_time = now

        cv2.polylines(frame, [roi], isClosed=True, color=(0,255,255), thickness=2)
        cv2.circle(frame, roi_center, 4, (0,255,255), -1)

        if result.boxes is not None and result.boxes.id is not None:
            ids = result.boxes.id.cpu().numpy().astype(int)
            xyxy = result.boxes.xyxy.cpu().numpy()
            for i, tid in enumerate(ids):
                x1,y1,x2,y2 = xyxy[i]
                cx = int((x1+x2)/2); cy = int((y1+y2)/2)
                face_rect = (x1, y1, x2, y2)
                yaw = head_pose.yaw_from_frame(result.orig_img, face_rect)

                exposed = False
                if inside_polygon((cx,cy), roi):
                    exposed = True
                elif yaw is not None:
                    dir_sign = direction_to_roi((cx,cy), roi_center)
                    if (dir_sign > 0 and yaw > yaw_thresh) or (dir_sign < 0 and yaw < -yaw_thresh):
                        exposed = True

                if exposed:
                    totals[tid] = totals.get(tid, 0.0) + dt

                color = (0,200,0) if exposed else (0,0,200)
                cv2.rectangle(frame, (int(x1),int(y1)), (int(x2),int(y2)), color, 2)
                label = f"ID {tid} | {totals.get(tid,0):.1f}s"
                if yaw is not None:
                    label += f" | yaw {yaw:.0f}"
                cv2.putText(frame, label, (int(x1), int(y1)-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.putText(frame, "q: salir  s: guardar CSV", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        if show:
            cv2.imshow("exposure", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord('q')):
                break
            if key in (ord('s'),):
                save_totals(session_id, totals, roi)

    cap.release()
    cv2.destroyAllWindows()
    if save_csv:
        save_totals(session_id, totals, roi)

def save_totals(session_id, totals, roi):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_name = f"exposure_{session_id}_{ts}.csv"
    with open(csv_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["session_id", "track_id", "seconds"])
        for k,v in totals.items():
            writer.writerow([session_id, k, round(v,2)])
    print("CSV guardado:", csv_name)
    try:
        saved = save_session(session_id, roi, totals)
        if saved: print("Registrado en Mongo.")
    except Exception as e:
        print("Mongo no disponible:", e)

if __name__ == "__main__":
    run(source=0)
