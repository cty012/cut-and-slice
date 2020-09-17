import math


# return the top-left corner of the rectangle
def top_left(pos, size, *, align=(0, 0)):
    return pos[0] - align[0] * (size[0] // 2), pos[1] - align[1] * (size[1] // 2)


# return the distance between two positions
def get_dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# return the blocks between two positions
def get_between(pos1, pos2):
    orig_pos1 = pos1
    if pos1[0] == pos2[0]:
        ans = vertical(pos1, pos2)
        ans.remove(pos1)
        return ans
    elif pos1[0] > pos2[0]:
        pos1, pos2 = pos2, pos1
    diff, x = (pos2[0] - pos1[0], abs(pos2[1] - pos1[1])), 0.5
    pre_ans, start = [], 0
    while x < diff[0]:
        intersect = x * diff[1] / diff[0] + 0.5
        pre_ans += vertical(
            (math.floor(x), start),
            (math.floor(x), math.floor(intersect) - (1 if intersect.is_integer() else 0))
        )
        start = math.floor(intersect)
        x += 1.0
    pre_ans += vertical((math.floor(x), start), (math.floor(x), diff[1]))
    ans = [(pos1[0] + a[0], pos1[1] + a[1] * (1 if pos2[1] >= pos1[1] else -1)) for a in pre_ans]
    ans.remove(orig_pos1)
    return ans


def vertical(pos1, pos2):
    assert pos1[0] == pos2[0]
    return [(pos1[0], j) for j in range(min(pos1[1], pos2[1]), max(pos1[1], pos2[1]) + 1)]


# get next side, friendly, opponents
def get_next(all_sides, side, friendly):
    n_side = all_sides[(all_sides.index(side) + 1) % len(all_sides)]
    n_friendly = [f for f in friendly if f != n_side] + [side]
    n_opponents = [s for s in all_sides if s != n_side and s not in n_friendly]
    if n_side not in friendly:
        n_friendly, n_opponents = n_opponents, n_friendly
    return n_side, n_friendly, n_opponents
