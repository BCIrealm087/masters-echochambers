"""Exact matched-post reference for small constrained strata."""
from functools import lru_cache
from fractions import Fraction
from itertools import permutations


def legal_targets(sharers, action_seconds, authors, original_seconds):
    """Each original slot stays distinct, including repeated copies of a post."""
    n = len(sharers)
    if not n == len(action_seconds) == len(authors) == len(original_seconds):
        raise ValueError("Action and original slot columns must have the same length")
    return tuple(
        sum(1 << j for j, (author, published_at) in enumerate(zip(authors, original_seconds))
            if author != sharer and published_at <= action_at)
        for sharer, action_at in zip(sharers, action_seconds)
    )


def exact_distribution(allowed, internal, max_slots=16):
    """Count feasible permutations by internal action total, including immobile strata."""
    size = len(allowed)
    if size > max_slots:
        raise ValueError("Exact reference exceeds the configured slot limit")
    if len(internal) != size:
        raise ValueError("Internal and legality masks must describe the same slots")
    full = (1 << size) - 1
    if any(mask < 0 or mask > full for mask in (*allowed, *internal)):
        raise ValueError("Mask contains an out-of-range slot")
    if any(not mask & (1 << row) for row, mask in enumerate(allowed)):
        raise ValueError("Observed pairing is illegal")

    @lru_cache(maxsize=None)
    def count(remaining):
        if not remaining:
            return (1,)
        row = size - remaining.bit_count()
        distribution = [0] * (remaining.bit_count() + 1)
        choices = remaining & allowed[row]
        while choices:
            slot = choices & -choices
            increment = int(bool(internal[row] & slot))
            for score, weight in enumerate(count(remaining ^ slot)):
                distribution[score + increment] += weight
            choices ^= slot
        return tuple(distribution)

    counts = count(full)
    total = sum(counts)
    return tuple(Fraction(weight, total) for weight in counts)


def verify_reference():
    allowed = legal_targets([1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 1, 1])
    # The observed assignment and a three-cycle are legal. A pair swap cannot
    # reach one from the other because it would introduce a self-repost.
    fixtures = [(allowed, (1, 2, 4)), ((1, 2), (1, 2)),
                ((7, 7, 7), (3, 3, 4))]
    for masks, internal in fixtures:
        counts = [0] * (len(masks) + 1)
        for order in permutations(range(len(masks))):
            if all(mask & (1 << column) for mask, column in zip(masks, order)):
                score = sum(bool(mask & (1 << column)) for mask, column in zip(internal, order))
                counts[score] += 1
        expected = tuple(Fraction(weight, sum(counts)) for weight in counts)
        assert exact_distribution(masks, internal) == expected
    assert exact_distribution(allowed, (1, 2, 4)) == (Fraction(1, 2), 0, 0, Fraction(1, 2))
    assert legal_targets([1, 2], [10, 11], [3, 3], [10, 11]) == (1, 3)
    assert exact_distribution((1, 3), (3, 3)) == (0, 0, 1)
    return len(fixtures) + 1


if __name__ == "__main__":
    print(f"Verified {verify_reference()} exact reference fixtures")
