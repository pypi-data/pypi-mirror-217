import math

from typing import Iterable

from .utils import T


__all__ = [
    "jaccard_sim",
    "cos_sim",
    "angular_dist",
    "angular_sim",
]


def jaccard_sim(a: set, b: Iterable) -> float:
    intersection = a.intersection(b)
    union = a.union(b)
    return len(intersection) / len(union)


def cos_sim(a: Iterable[T], b: Iterable[T]) -> T:
    it = zip(a, b)
    x, y = next(it)
    left = x * x
    right = y * y
    ab = x * y
    for x, y in it:
        left += x * x
        right += y * y
        ab += x * y
    return ab / (left * right) ** 0.5


def angular_dist(a: Iterable[float], b: Iterable[float]) -> float:
    cos = cos_sim(a, b)
    cos = min(1.0, max(-1.0, cos))
    return math.acos(cos) / math.pi


def angular_sim(a: Iterable[float], b: Iterable[float]) -> float:
    return 1 - angular_dist(a, b)
