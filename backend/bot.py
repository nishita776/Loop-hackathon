vague_words = [
    "almost", "soon", "trying", "working",
    "maybe", "nearly"
]

commitment_words = [
    "today", "by eod", "tonight",
    "tomorrow", "will finish", "done by"
]

def classify_message(text):
    t = text.lower()
    for w in vague_words:
        if w in t:
            return "vague"
    for w in commitment_words:
        if w in t:
            return "commitment"
    return "normal"

def bot_reply(msg_type):
    if msg_type == "vague":
        return "🤖 That sounds unclear. Any blockers or ETA?"
    if msg_type == "commitment":
        return "🤖 Noted 👍 I’ll check if progress stalls."
    return None
