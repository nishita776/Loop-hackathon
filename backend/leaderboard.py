def compute_leaderboard(users_behavior):
    """
    Computes leaderboard scores from behavior metrics.
    Input: dict of { user: behavior_dict }
    Output: sorted leaderboard list
    """

    leaderboard = []

    for user, behavior in users_behavior.items():

        # Normalize values
        norm_activity = min(behavior["activity"] / 5, 1)
        norm_speed = min(behavior["speed"] / 1, 1)
        norm_consistency = behavior["consistency"]

        # Final score
        score = (
            0.4 * norm_activity +
            0.3 * norm_consistency +
            0.3 * norm_speed
        )

        leaderboard.append({
            "user": user,
            "score": round(score, 3)
        })

    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return leaderboard


# 🔹 local test
if __name__ == "__main__":
    users_behavior = {
        "alice": {
            "activity": 2.4,
            "staleness_hours": 14,
            "speed": 0.35,
            "consistency": 0.6,
            "mismatch": True
        },
        "bob": {
            "activity": 4.8,
            "staleness_hours": 2,
            "speed": 0.9,
            "consistency": 0.85,
            "mismatch": False
        }
    }

    leaderboard = compute_leaderboard(users_behavior)
    for row in leaderboard:
        print(row)
