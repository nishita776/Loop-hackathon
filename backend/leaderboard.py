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
