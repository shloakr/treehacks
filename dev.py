import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
import time
import cv2
import mediapipe as mp
import math
# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize the Firebase app with your Firebase credentials
cred = credentials.Certificate('treehacks24-5080b-firebase-adminsdk-bortu-b0ffbf466c.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://treehacks24-5080b-default-rtdb.firebaseio.com/'
})

def get_midpoint(p1, p2):
    # Calculate the midpoint between two points
    midpoint = {
        'x': (p1.x + p2.x) / 2,
        'y': (p1.y + p2.y) / 2,
        'z': (p1.z + p2.z) / 2,
        'visibility': (p1.visibility + p2.visibility) / 2 if hasattr(p1, 'visibility') else 0,
        'presence': (p1.presence + p2.presence) / 2 if hasattr(p1, 'presence') else 0
    }
    return midpoint

def calculate_head_pose(landmarks):
    # Retrieve the landmarks
    left_ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR.value]
    right_ear = landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value]
    left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE.value]
    right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value]

    # Calculate the midpoints for eyes and ears
    eyes_midpoint = get_midpoint(left_eye, right_eye)
    ears_midpoint = get_midpoint(left_ear, right_ear)

    # Calculate the roll angle based on the line between the ears
    roll = math.degrees(math.atan2(ears_midpoint['y'] - eyes_midpoint['y'], ears_midpoint['x'] - eyes_midpoint['x']))

    # For pitch and yaw, we would need a more sophisticated approach involving a 3D model
    # Placeholder values are used here
    pitch = 0
    yaw = 0

    return roll, pitch, yaw

# Start capturing video from the camera.
cap = cv2.VideoCapture('/Users/shloakrathod/Desktop/treehacks/RPReplay_Final1708216904.mov')

       
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB.
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame for pose detection.
    pose_results = pose.process(frame_rgb)
        

    if pose_results.pose_landmarks:
        head_vector = calculate_head_pose(pose_results.pose_landmarks.landmark)
        left_shoulder = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP.value]

        # Frame dimensions for converting normalized coordinates to pixel coordinates
        frame_height, frame_width = frame.shape[:2]

        # Convert normalized coordinates (0.0-1.0) to pixel coordinates
        left_shoulder_pixel = (int(left_shoulder.x * frame_width), int(left_shoulder.y * frame_height))
        right_shoulder_pixel = (int(right_shoulder.x * frame_width), int(right_shoulder.y * frame_height))
        left_hip_pixel = (int(left_hip.x * frame_width), int(left_hip.y * frame_height))
        right_hip_pixel = (int(right_hip.x * frame_width), int(right_hip.y * frame_height))

        # Calculate the midpoint in pixel coordinates
        midpoint_pixel1 = ((left_shoulder_pixel[0] + right_shoulder_pixel[0]) // 2, 
                        (left_shoulder_pixel[1] + right_shoulder_pixel[1]) // 2)
        midpoint_pixel2 = ((left_hip_pixel[0] + right_hip_pixel[0]) // 2, 
                (left_hip_pixel[1] + right_hip_pixel[1]) // 2)
        
        
        midpoint_pixel3 = ((5*(midpoint_pixel1[0]) + 2*(midpoint_pixel2[0]))//7, (5*(midpoint_pixel1[1]) + 2*(midpoint_pixel2[1]))//7)
        print(midpoint_pixel3)
        

        # Draw a circle at the midpoint
        cv2.circle(frame, midpoint_pixel3, radius=5, color=(0, 255, 0), thickness=-1)
        # cv2.circle(frame, midpoint_pixel1, radius=5, color=(0, 255, 0), thickness=-1)
        #  print(f"Landmark 11 (Left Shoulder): x={left_shoulder.x}, y={left_shoulder.y}, z={left_shoulder.z}, visibility={left_shoulder.visibility}")
        print(f"Landmark 12 (Right Shoulder): x={right_shoulder.x}, y={right_shoulder.y}, z={right_shoulder.z}, visibility={right_shoulder.visibility}")
        print(f"Head Vector: {head_vector}")

    # Draw the pose annotation on the frame.
    mp.solutions.drawing_utils.draw_landmarks(
        frame, 
        pose_results.pose_landmarks, 
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
        connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
    )
    ref = db.reference('/')
    
    # Updating the database
    if pose_results.pose_landmarks:
        print("here")
        ref.update({
            'body_tilt': head_vector[0],
            # 'body_tilt': body_tilt
            
        })

    # Display the frame.
    cv2.imshow('Pose', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()