class DifficultyEstimator:
    async def estimate(self, word: str, context_count: int) -> float:
        # v1 heuristic
        base = 0.7 if len(word) > 6 else 0.4
        penalty = min(context_count * 0.05, 0.3)
        return min(base + penalty, 1.0)
