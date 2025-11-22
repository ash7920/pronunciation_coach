import difflib

def compare_text(expected: str, actual: str):
    expected_words = expected.lower().split()
    actual_words = actual.lower().split()

    matcher = difflib.SequenceMatcher(None, expected_words, actual_words)

    matches = []
    missing = []
    incorrect = []

    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == "equal":
            matches.extend(expected_words[a0:a1])
        elif opcode == "delete":
            missing.extend(expected_words[a0:a1])
        elif opcode == "replace":
            incorrect.extend(expected_words[a0:a1])

    return {
        "matches": matches,
        "missing": missing,
        "incorrect": incorrect
    }


def score_pronunciation(comparison):
    total_words = len(comparison["matches"]) + len(comparison["missing"]) + len(comparison["incorrect"])

    if total_words == 0:
        return 0

    match_score = len(comparison["matches"]) / total_words
    error_penalty = (len(comparison["missing"]) + len(comparison["incorrect"])) / total_words

    final_score = (match_score * 0.7) + ((1 - error_penalty) * 0.3)
    return round(final_score * 100, 2)


def generate_feedback(comparison):
    feedback = []

    if comparison["incorrect"]:
        feedback.append(f"You mispronounced: {', '.join(comparison['incorrect'])}. Try speaking slowly.")

    if comparison["missing"]:
        feedback.append(f"You missed: {', '.join(comparison['missing'])}. Focus on clarity.")

    if not feedback:
        feedback.append("Great job! Your pronunciation was clear and accurate 🎉")

    return " ".join(feedback)
