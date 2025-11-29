#!/usr/bin/env python3
import sys

# Mathematical chemistry, 2025/26
# October 9, 2025


def minimum_representation(bec):
    """
    Return the minimum representation, i.e. lexiconx.Graphically
    minimal string among all cyclic shifts.
    """
    return min(bec[i:] + bec[:i] for i in range(len(bec)))


def has_reflection(bec):
    """
    Return True if the benzenoid with the given boundary-edges
    code has a mirror plane.
    """
    return minimum_representation(bec) == minimum_representation(bec[::-1])


def order_of_rotation(bec):
    """
    Determine the rotational symmetry order for the
    benzenoid with the given boundary-edges code.
    """
    for order in [6, 3, 2]:
        if len(bec) % order != 0:
            continue
        t = len(bec) // order
        valid = True
        for i in range(1, order):
            if bec[:t] != bec[i * t : (i + 1) * t]:
                valid = False
                break
        if valid:
            return order
    return 1


def point_group(bec):
    """
    Return the symmetry (point group) for the benzenoid with the given
    boundary-edges code.
    """
    group_name = {
        (6, True): "D6h",
        (6, False): "C6h",
        (3, True): "D3h",
        (3, False): "C3h",
        (2, True): "D2h",
        (2, False): "C2h",
        (1, True): "C2v",
        (1, False): "Cs",
    }
    return group_name[order_of_rotation(bec), has_reflection(bec)]


if __name__ == "__main__":
    symmetry = dict()
    freq = dict()
    for line in sys.stdin:
        bec = line.strip()
        sym = point_group(bec)
        if sym not in symmetry:
            symmetry[sym] = []
            freq[sym] = 0
        freq[sym] += 1
        if len(symmetry[sym]) < 5:
            symmetry[sym].append(bec)
    all_groups = ["D6h", "C6h", "D3h", "C3h", "D2h", "C2h", "C2v", "Cs"]
    for sym in all_groups:
        if sym not in symmetry:
            continue
        print(f"Numbers of structures with symmetry {sym}: {freq[sym]}")
        for bec in symmetry[sym]:
            print(bec)
