def generate_alerts(user, behavior, task):
    """
    Generates alerts based on behavior signals and task state.
    This function is PURE and standalone.
    """

    alerts = []

    # 1. Inactivity alert
    if behavior["staleness_hours"] > 12:
        alerts.append({
            "user": user,
            "type": "INACTIVITY",
            "severity": "HIGH",
            "reason": f"No Git activity in last {behavior['staleness_hours']} hours"
        })

    # 2. Deadline risk alert
    if task["deadline_hours"] < 24 and behavior["activity"] < 1:
        alerts.append({
            "user": user,
            "type": "DEADLINE_RISK",
            "severity": "HIGH",
            "reason": "Deadline approaching with low activity"
        })

    # 3. Progress mismatch alert
    if task["status"] == "in-progress" and behavior["mismatch"]:
        alerts.append({
            "user": user,
            "type": "PROGRESS_MISMATCH",
            "severity": "MEDIUM",
            "reason": "Task marked in-progress but Git shows inactivity"
        })

    return alerts


# 🔹 local test (optional but recommended)
if __name__ == "__main__":
    behavior = {
        "activity": 0.6,
        "staleness_hours": 14,
        "speed": 0.3,
        "consistency": 0.5,
        "mismatch": True
    }

    task = {
        "task_id": "T101",
        "assignee": "alice",
        "deadline_hours": 10,
        "status": "in-progress"
    }

    alerts = generate_alerts("alice", behavior, task)
    for alert in alerts:
        print(alert)
