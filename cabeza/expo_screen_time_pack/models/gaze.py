import numpy as np
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

IDX_LEFT_EAR = 234
IDX_RIGHT_EAR = 454
IDX_NOSE_TIP = 1

class HeadPose:
    def __init__(self):
        self.mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1,
                                          refine_landmarks=False, min_detection_confidence=0.5,
                                          min_tracking_confidence=0.5)

    def yaw_from_frame(self, frame_bgr, face_rect):
        x1,y1,x2,y2 = face_rect
        x1 = max(0,int(x1)); y1 = max(0,int(y1))
        x2 = min(frame_bgr.shape[1]-1,int(x2)); y2 = min(frame_bgr.shape[0]-1,int(y2))
        roi = frame_bgr[y1:y2, x1:x2]
        if roi.size == 0:
            return None
        rgb = roi[:,:,::-1]
        res = self.mesh.process(rgb)
        if not res.multi_face_landmarks:
            return None
        lm = res.multi_face_landmarks[0].landmark

        def denorm(p):
            return np.array([p.x*(x2-x1)+x1, p.y*(y2-y1)+y1], dtype=np.float32)

        left = denorm(lm[IDX_LEFT_EAR]); right = denorm(lm[IDX_RIGHT_EAR]); nose = denorm(lm[IDX_NOSE_TIP])
        dl = np.linalg.norm(nose - left)
        dr = np.linalg.norm(nose - right)
        yaw_score = (dl - dr) / (dl + dr + 1e-6)  # [-1,1]
        yaw_deg = yaw_score * 60.0
        return yaw_deg
