import cv2
import pandas as pd
from pose_engine import analyze_frame

def check_video_quality(video_path):
    """
    Opens the video and checks if it is good enough to process.
    Checks resolution and frame rate.
    Returns True if good, False if bad quality.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return False, "Cannot open video file"

    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    cap.release()

    # Minimum requirements
    if width < 320 or height < 240:
        return False, f"Resolution too low: {width}x{height}. Minimum is 320x240."
    if fps < 10:
        return False, f"Frame rate too low: {fps}fps. Minimum is 10fps."
    if total_frames < 30:
        return False, "Video too short. Please upload at least 1 second of footage."

    return True, f"Video quality OK: {width}x{height} at {fps}fps, {total_frames} frames"


def process_video(video_path, output_path):
    """
    Opens the video frame by frame.
    Runs pose estimation on each frame using MediaPipe.
    Collects all joint angles across all frames.
    Saves output video with skeleton drawn on it.
    Returns a Pandas DataFrame with all frame data.
    """
    cap = cv2.VideoCapture(video_path)

    # Get video properties for writing output
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)

    # Set up output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    all_frames_data = []
    frame_number = 0

    print(f"Processing video: {video_path}")

    while cap.isOpened():
        ret, frame = cap.read()

        # ret is False when video ends
        if not ret:
            break

        frame_number += 1
        timestamp = round(frame_number / fps, 3)

        # Run pose estimation on this frame
        frame_data, processed_frame = analyze_frame(frame)

        # Collect data for this frame
        row = {
            "frame_number": frame_number,
            "timestamp_seconds": timestamp,
            "landmarks_detected": frame_data["landmarks_detected"]
        }

        # Add all joint angles to the row
        if frame_data["landmarks_detected"]:
            row.update(frame_data["joint_angles"])
        else:
            # If no person detected, fill with None
            row.update({
                "left_knee": None, "right_knee": None,
                "left_elbow": None, "right_elbow": None,
                "left_hip": None, "right_hip": None
            })

        all_frames_data.append(row)

        # Write processed frame to output video
        out.write(processed_frame)

        # Show progress every 30 frames
        if frame_number % 30 == 0:
            print(f"Processed frame {frame_number}, timestamp: {timestamp}s")

    cap.release()
    out.release()

    print(f"Video processing complete. Total frames: {frame_number}")

    # Convert all frame data to Pandas DataFrame
    df = pd.DataFrame(all_frames_data)
    return df