def classify_counts(counts, n):
    all_zero = "0" * n
    if len(counts) == 1 and all_zero in counts:
        return "constant"
    return "balanced"