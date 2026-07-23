import pandas as pd
import numpy as np

# Safe angle ranges for each joint
# (minimum safe angle, maximum safe angle)
SAFE_RANGES = {
    "left_knee":   (30, 170),
    "right_knee":  (30, 170),
    "left_elbow":  (30, 180),
    "right_elbow": (30, 180),
    "left_hip":    (140, 180),
    "right_hip":   (140, 180),
}

# Risk category thresholds
RISK_CATEGORIES = {
    (0, 30):   "Low Risk",
    (31, 60):  "Moderate Risk",
    (61, 80):  "High Risk",
    (81, 100): "Critical Risk"
}

def assess_joint_risk(angle, joint_name):
    """
    Checks one joint angle against its safe range.
    Returns risk level and recommendation message.
    """
    if angle is None or joint_name not in SAFE_RANGES:
        return "unknown", "No data available"

    min_safe, max_safe = SAFE_RANGES[joint_name]

    if angle < min_safe - 10 or angle > max_safe + 10:
        return "critical", f"{joint_name.replace('_', ' ').title()} angle {angle}° is critically outside safe range ({min_safe}°-{max_safe}°). Immediate attention needed."
    elif angle < min_safe or angle > max_safe:
        return "high", f"{joint_name.replace('_', ' ').title()} angle {angle}° is outside safe range ({min_safe}°-{max_safe}°). High injury risk detected."
    elif angle < min_safe + 10 or angle > max_safe - 10:
        return "moderate", f"{joint_name.replace('_', ' ').title()} angle {angle}° is near boundary of safe range. Monitor closely."
    else:
        return "low", f"{joint_name.replace('_', ' ').title()} angle {angle}° is within safe range. Movement looks good."


def calculate_symmetry_score(df):
    """
    Compares left side angles to right side angles.
    A big difference between left and right means
    the athlete is compensating for something — which is a risk.
    Returns a symmetry score from 0 (worst) to 100 (perfect symmetry).
    """
    symmetry_scores = []

    pairs = [
        ("left_knee", "right_knee"),
        ("left_elbow", "right_elbow"),
        ("left_hip", "right_hip")
    ]

    for left_joint, right_joint in pairs:
        if left_joint in df.columns and right_joint in df.columns:
            left_avg  = df[left_joint].dropna().mean()
            right_avg = df[right_joint].dropna().mean()

            if not np.isnan(left_avg) and not np.isnan(right_avg):
                # Difference between left and right
                difference = abs(left_avg - right_avg)
                # Convert to score — 0 difference = 100 score
                score = max(0, 100 - (difference * 2))
                symmetry_scores.append(score)

    if symmetry_scores:
        return round(np.mean(symmetry_scores), 2)
    return 50  # Default if no data


def analyze_risk(df, athlete_profile=None):
    """
    Takes the DataFrame of all frame angles.
    Analyzes risk for every joint.
    Calculates overall risk score.
    Returns complete risk report.
    """
    report = {
        "total_frames_analyzed": len(df),
        "frames_with_person_detected": int(df["landmarks_detected"].sum()),
        "joint_risk_summary": {},
        "symmetry_score": 0,
        "overall_risk_score": 0,
        "risk_category": "",
        "recommendations": []
    }

    # Analyze each joint
    joints = ["left_knee", "right_knee", "left_elbow",
              "right_elbow", "left_hip", "right_hip"]

    high_risk_count = 0
    total_risk_score = 0

    for joint in joints:
        if joint not in df.columns:
            continue

        joint_angles = df[joint].dropna()

        if len(joint_angles) == 0:
            continue

        avg_angle = round(joint_angles.mean(), 2)
        min_angle = round(joint_angles.min(), 2)
        max_angle = round(joint_angles.max(), 2)

        # Check the most extreme angle for this joint
        # (worst case scenario in the video)
        min_safe, max_safe = SAFE_RANGES.get(joint, (0, 180))

        deviation_below = max(0, min_safe - min_angle)
        deviation_above = max(0, max_angle - max_safe)
        max_deviation = max(deviation_below, deviation_above)

        risk_level, recommendation = assess_joint_risk(min_angle if deviation_below > deviation_above else max_angle, joint)

        report["joint_risk_summary"][joint] = {
            "average_angle": avg_angle,
            "minimum_angle": min_angle,
            "maximum_angle": max_angle,
            "risk_level": risk_level,
            "recommendation": recommendation
        }

        if risk_level in ["high", "critical"]:
            high_risk_count += 1
            report["recommendations"].append(recommendation)

        # Add to total risk score
        total_risk_score += max_deviation

    # Calculate symmetry
    report["symmetry_score"] = calculate_symmetry_score(df)
    symmetry_risk = (100 - report["symmetry_score"]) * 0.2

    # Calculate overall risk score using document formula
    biomechanical_score = min(100, total_risk_score * 2) * 0.35
    symmetry_component  = symmetry_risk
    detection_rate      = report["frames_with_person_detected"] / max(report["total_frames_analyzed"], 1)
    movement_component  = (1 - detection_rate) * 100 * 0.10

    # Add historical injury factor if athlete profile provided
    historical_component = 0
    training_component   = 0
    if athlete_profile:
        if athlete_profile.get("injury_history", "none").lower() != "none":
            historical_component = 15
        training_load = athlete_profile.get("training_load", "moderate").lower()
        if training_load == "high":
            training_component = 10
        elif training_load == "moderate":
            training_component = 5

    overall_score = (
        biomechanical_score +
        historical_component * 0.20 +
        symmetry_component +
        training_component * 0.15 +
        movement_component
    )

    report["overall_risk_score"] = round(min(100, overall_score), 2)

    # Assign risk category
    score = report["overall_risk_score"]
    if score <= 30:
        report["risk_category"] = "Low Risk"
    elif score <= 60:
        report["risk_category"] = "Moderate Risk"
    elif score <= 80:
        report["risk_category"] = "High Risk"
    else:
        report["risk_category"] = "Critical Risk"

    # Add general recommendations if none found
    if not report["recommendations"]:
        report["recommendations"].append(
            "Movement patterns look generally safe. Continue monitoring regularly."
        )

    return report