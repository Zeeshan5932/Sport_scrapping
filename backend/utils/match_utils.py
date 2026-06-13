def is_match_live(status: str) -> bool:
    """Status se pata karo match live hai ya nahi."""
    if not status:
        return False

    s = status.lower().strip()

    ended_keywords = ["ended", "finished", "complete", "abandoned", "no result"]

    for kw in ended_keywords:
        if kw in s:
            return False

    return True  # INN 1, INN 2, Live, In Progress etc. = live


def is_match_ended(status: str) -> bool:
    """Status se pata karo match ended hai ya nahi."""
    return not is_match_live(status)


def build_match_key(tournament_name: str, home_team: str, away_team: str) -> str:
    return f"{tournament_name}|{home_team}|{away_team}"