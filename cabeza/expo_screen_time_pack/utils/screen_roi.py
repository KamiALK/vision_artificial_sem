import cv2
import numpy as np

def select_polygon_roi(frame):
    pts = []
    clone = frame.copy()
    instructions = "Click 4 puntos (esquinas de la pantalla). ENTER confirma, 'r' reset."
    def click_event(event, x, y, flags, param):
        nonlocal pts, clone
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(pts) < 4:
                pts.append((x, y))
                cv2.circle(clone, (x, y), 4, (0, 255, 0), -1)

    cv2.namedWindow("ROI")
    cv2.setMouseCallback("ROI", click_event)

    while True:
        vis = clone.copy()
        cv2.putText(vis, instructions, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
        if len(pts) >= 1:
            for i in range(len(pts)-1):
                cv2.line(vis, pts[i], pts[i+1], (0, 255, 0), 2)
            if len(pts) == 4:
                cv2.line(vis, pts[3], pts[0], (0, 255, 0), 2)
        cv2.imshow("ROI", vis)
        key = cv2.waitKey(20) & 0xFF
        if key == 13 and len(pts) == 4:  # ENTER
            break
        if key in (27, ord('q')):
            pts = []
            break
        if key in (ord('r'), ord('R')):
            pts = []
            clone = frame.copy()
    cv2.destroyWindow("ROI")
    return np.array(pts, dtype=np.int32) if len(pts) == 4 else None

def polygon_center(poly):
    M = cv2.moments(poly)
    if M["m00"] == 0:
        return (int(poly[:,0].mean()), int(poly[:,1].mean()))
    cx = int(M["m10"]/M["m00"]); cy = int(M["m01"]/M["m00"])
    return (cx, cy)

def inside_polygon(point, poly):
    return cv2.pointPolygonTest(poly, point, False) >= 0
