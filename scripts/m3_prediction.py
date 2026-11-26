"""Conditional author scoring for the registered nested discovery models."""
from collections import Counter
from math import exp, inf, log

DAY_SECONDS = 86400


def author_distributions(risk, global_counts, context_counts, history, groups,
                         sharer, action_second, context_mass, dyad_mass, half_life, beta):
    """Return normalized scores on one shared author risk set.

    History contains (author, second) pairs for this sharer in the training prefix.
    An external category can be supplied as a risk-set member with zero counts.
    """
    risk = set(risk) - {sharer}
    if not risk:
        raise ValueError("Author risk set is empty")
    uniform = 1 / len(risk)
    global_total = sum(global_counts.get(author, 0) for author in risk)
    context_total = sum(context_counts.get(author, 0) for author in risk)
    dyads = Counter()
    for author, second in history:
        if second > action_second:
            raise ValueError("Training history contains a future action")
        if author in risk:
            dyads[author] += 2 ** (-(action_second - second) / (half_life * DAY_SECONDS))
    dyad_total = dyads.total()
    global_probs = {}
    context_probs = {}
    history_probs = {}
    group_probs = {}
    sharer_group = groups.get(sharer)
    for author in risk:
        global_probs[author] = (global_counts.get(author, 0) + uniform) / (global_total + 1)
        context_probs[author] = (
            context_counts.get(author, 0) + context_mass * global_probs[author]
        ) / (context_total + context_mass)
        history_probs[author] = (
            dyads[author] + dyad_mass * context_probs[author]
        ) / (dyad_total + dyad_mass)
        same_group = sharer_group is not None and groups.get(author) == sharer_group
        group_probs[author] = history_probs[author] * exp(beta * same_group)
    normalizer = sum(group_probs.values())
    group_probs = {author: score / normalizer for author, score in group_probs.items()}
    return global_probs, context_probs, history_probs, group_probs


def verify_prediction():
    inputs = ([1, 2, 3, 4], {1: 999, 2: 8, 3: 2}, {2: 1, 3: 3},
              [(2, 0), (3, DAY_SECONDS)],
              {1: 0, 2: 0, 3: 1}, 1, DAY_SECONDS, 10, 1)
    global_probs, context_probs, history_probs, group_probs = author_distributions(
        *inputs, half_life=1, beta=log(2),
    )
    for distribution in (global_probs, context_probs, history_probs, group_probs):
        assert distribution.keys() == {2, 3, 4}
        assert abs(sum(distribution.values()) - 1) < 1e-12
        assert distribution[4] > 0
    assert abs(global_probs[2] - (8 + 1 / 3) / 11) < 1e-12
    assert abs(context_probs[3] - (3 + 10 * global_probs[3]) / 14) < 1e-12
    assert abs(history_probs[2] - (0.5 + context_probs[2]) / 2.5) < 1e-12
    assert abs(group_probs[2] / group_probs[3] - 2 * history_probs[2] / history_probs[3]) < 1e-12
    _, _, unadjusted, neutral = author_distributions(*inputs, half_life=inf, beta=0)
    assert abs(unadjusted[2] - (1 + context_probs[2]) / 3) < 1e-12
    assert all(abs(neutral[author] - score) < 1e-12 for author, score in unadjusted.items())
    return True


if __name__ == "__main__":
    verify_prediction()
    print("Verified author scoring on a synthetic risk set")
