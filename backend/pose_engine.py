import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(point_a, point_b, point_c):
    """
    Calculates the angle at point_b between three joint points.
    Example: point_a=hip, point_b=knee, point_c=ankle
    gives you the knee angle.
    """
    a = np.array(point_a)
    b = np.array(point_b)
    c = np.array(point_c)

    vector_ba = a - b
    vector_bc = c - b

    cosine_angle = np.dot(vector_ba, vector_bc) / (
        np.linalg.norm(vector_ba) * np.linalg.norm(vector_bc)
    )
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return round(angle, 2)


def get_landmark_coords(landmarks, landmark_name):
    """
    Gets x and y position of a specific body joint.
    Example: get_landmark_coords(landmarks, 'LEFT_KNEE')
    returns [x_position, y_position]
    """
    landmark = landmarks[mp_pose.PoseLandmark[landmark_name]]
    return [landmark.x, landmark.y]


def analyze_frame(frame):
    """
    Takes one video frame.
    Finds all body joints using MediaPipe.
    Calculates all joint angles using NumPy.
    Returns joint angles and the frame with skeleton drawn on it.
    """
    results_data = {
        "landmarks_detected": False,
        "joint_angles": {},
    }

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:

        # Convert BGR to RGB because MediaPipe needs RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run MediaPipe on this frame
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            results_data["landmarks_detected"] = True
            lm = results.pose_landmarks.landmark

            # Get joint positions
            left_hip    = get_landmark_coords(lm, 'LEFT_HIP')
            left_knee   = get_landmark_coords(lm, 'LEFT_KNEE')
            left_ankle  = get_landmark_coords(lm, 'LEFT_ANKLE')

            right_hip   = get_landmark_coords(lm, 'RIGHT_HIP')
            right_knee  = get_landmark_coords(lm, 'RIGHT_KNEE')
            right_ankle = get_landmark_coords(lm, 'RIGHT_ANKLE')

            left_shoulder = get_landmark_coords(lm, 'LEFT_SHOULDER')
            left_elbow    = get_landmark_coords(lm, 'LEFT_ELBOW')
            left_wrist    = get_landmark_coords(lm, 'LEFT_WRIST')

            right_shoulder = get_landmark_coords(lm, 'RIGHT_SHOULDER')
            right_elbow    = get_landmark_coords(lm, 'RIGHT_ELBOW')
            right_wrist    = get_landmark_coords(lm, 'RIGHT_WRIST')

            # Calculate all joint angles
            results_data["joint_angles"] = {
                "left_knee":      calculate_angle(left_hip, left_knee, left_ankle),
                "right_knee":     calculate_angle(right_hip, right_knee, right_ankle),
                "left_elbow":     calculate_angle(left_shoulder, left_elbow, left_wrist),
                "right_elbow":    calculate_angle(right_shoulder, right_elbow, right_wrist),
                "left_hip":       calculate_angle(left_shoulder, left_hip, left_knee),
                "right_hip":      calculate_angle(right_shoulder, right_hip, right_knee),
            }

            # Draw skeleton on the frame
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

    return results_data, frame