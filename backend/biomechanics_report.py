import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

def generate_angle_chart(df):
    """
    Creates a line chart showing how knee angles
    changed across the entire video over time.
    This helps visualize exactly when risky moments occurred.
    """
    fig = go.Figure()

    if "left_knee" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["timestamp_seconds"],
            y=df["left_knee"],
            mode='lines',
            name='Left Knee Angle',
            line=dict(color='blue', width=2)
        ))

    if "right_knee" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["timestamp_seconds"],
            y=df["right_knee"],
            mode='lines',
            name='Right Knee Angle',
            line=dict(color='red', width=2)
        ))

    # Add safe range lines
    fig.add_hline(y=30,  line_dash="dash", line_color="orange",
                  annotation_text="Minimum Safe Angle (30°)")
    fig.add_hline(y=170, line_dash="dash", line_color="green",
                  annotation_text="Maximum Safe Angle (170°)")

    fig.update_layout(
        title='Knee Angle Over Time',
        xaxis_title='Time (seconds)',
        yaxis_title='Angle (degrees)',
        hovermode='x unified'
    )

    return fig.to_json()


def generate_risk_bar_chart(risk_report):
    """
    Creates a bar chart showing risk level for each joint.
    Makes it easy to see at a glance which joints are most at risk.
    """
    joints = []
    risk_levels = []
    colors = []

    color_map = {
        "low":      "green",
        "moderate": "orange",
        "high":     "red",
        "critical": "darkred",
        "unknown":  "gray"
    }

    for joint, data in risk_report["joint_risk_summary"].items():
        joints.append(joint.replace("_", " ").title())
        risk_level = data["risk_level"]
        risk_levels.append(risk_level)
        colors.append(color_map.get(risk_level, "gray"))

    fig = go.Figure(go.Bar(
        x=joints,
        y=[{"low": 25, "moderate": 50, "high": 75, "critical": 100}.get(r, 0) for r in risk_levels],
        marker_color=colors,
        text=risk_levels,
        textposition='auto'
    ))

    fig.update_layout(
        title='Joint Risk Assessment',
        xaxis_title='Body Joint',
        yaxis_title='Risk Level',
        yaxis=dict(tickvals=[25, 50, 75, 100],
                   ticktext=['Low', 'Moderate', 'High', 'Critical'])
    )

    return fig.to_json()


def generate_full_report(df, risk_report, athlete_name="Athlete"):
    """
    Combines everything into one final report dictionary.
    This is what gets sent back to the frontend to display.
    """
    angle_chart = generate_angle_chart(df)
    risk_chart  = generate_risk_bar_chart(risk_report)

    full_report = {
        "athlete_name": athlete_name,
        "summary": {
            "overall_risk_score":    risk_report["overall_risk_score"],
            "risk_category":         risk_report["risk_category"],
            "symmetry_score":        risk_report["symmetry_score"],
            "total_frames_analyzed": risk_report["total_frames_analyzed"],
            "detection_rate":        round(
                risk_report["frames_with_person_detected"] /
                max(risk_report["total_frames_analyzed"], 1) * 100, 1
            )
        },
        "joint_details":     risk_report["joint_risk_summary"],
        "recommendations":   risk_report["recommendations"],
        "charts": {
            "angle_over_time": angle_chart,
            "risk_by_joint":   risk_chart
        }
    }

    return full_report