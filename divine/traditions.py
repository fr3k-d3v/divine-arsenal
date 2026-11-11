"""Mathematical kamea and cautiously labelled traditional correspondences."""
from __future__ import annotations
from .astro import CHALDEAN

PLANETARY = {
    "Sun": {"day": "Sunday", "metal": "Gold", "topic": "leadership and illumination", "arbatel": "Och"},
    "Moon": {"day": "Monday", "metal": "Silver", "topic": "reflection and cycles", "arbatel": "Phul"},
    "Mercury": {"day": "Wednesday", "metal": "Mercury", "topic": "language and learning", "arbatel": "Ophiel"},
    "Venus": {"day": "Friday", "metal": "Copper", "topic": "harmony and aesthetics", "arbatel": "Hagith"},
    "Mars": {"day": "Tuesday", "metal": "Iron", "topic": "courage and effort", "arbatel": "Phaleg"},
    "Jupiter": {"day": "Thursday", "metal": "Tin", "topic": "justice and growth", "arbatel": "Bethor"},
    "Saturn": {"day": "Saturday", "metal": "Lead", "topic": "time and structure", "arbatel": "Aratron"},
}
SIZE = {"Saturn": 3, "Jupiter": 4, "Mars": 5, "Sun": 6,
        "Venus": 7, "Mercury": 8, "Moon": 9}


def magic_square(n: int) -> list[list[int]]:
    """Construct a normal magic square for any order n>=3 except n=2.

    The normal square has rows/columns and both main diagonals summing to
    n(n²+1)/2. This is an original mathematical implementation, not a claim
    of reproducing a particular historical Agrippa diagram's orientation.
    """
    if n < 3:
        raise ValueError("Order must be >= 3")
    if n % 2:
        a = [[0] * n for _ in range(n)]
        row, col = 0, n // 2
        for val in range(1, n*n + 1):
            a[row][col] = val
            rr, cc = (row - 1) % n, (col + 1) % n
            if a[rr][cc]:
                row = (row + 1) % n
            else:
                row, col = rr, cc
        return a
    if n % 4 == 0:
        a = [[r*n + c + 1 for c in range(n)] for r in range(n)]
        for r in range(n):
            for c in range(n):
                if r % 4 == c % 4 or r % 4 + c % 4 == 3:
                    a[r][c] = n*n + 1 - a[r][c]
        return a

    # Strachey method for singly even orders (n = 4k + 2).
    m = n // 2
    base = magic_square(m)
    a = [[0] * n for _ in range(n)]
    for r in range(m):
        for c in range(m):
            b = base[r][c]
            a[r][c] = b
            a[r][c + m] = b + 2*m*m
            a[r + m][c] = b + 3*m*m
            a[r + m][c + m] = b + m*m
    k = (m - 1) // 2
    for r in range(m):
        for c in range(k):
            a[r][c], a[r + m][c] = a[r + m][c], a[r][c]
        for c in range(n - k + 1, n):
            a[r][c], a[r + m][c] = a[r + m][c], a[r][c]
    a[k][0], a[k+m][0] = a[k+m][0], a[k][0]
    a[k][k], a[k+m][k] = a[k+m][k], a[k][k]
    return a


def verify_magic(a: list[list[int]]) -> bool:
    n = len(a)
    if n < 3 or any(len(row) != n for row in a):
        return False
    goal = n * (n*n + 1) // 2
    return (sorted(v for row in a for v in row) == list(range(1, n*n+1))
            and all(sum(row) == goal for row in a)
            and all(sum(a[r][c] for r in range(n)) == goal for c in range(n))
            and sum(a[i][i] for i in range(n)) == goal
            and sum(a[i][n-1-i] for i in range(n)) == goal)


def planetary_kamea(planet: str) -> dict:
    planet = planet.title()
    if planet not in SIZE:
        raise ValueError("Unrecognized traditional planet")
    n = SIZE[planet]
    grid = magic_square(n)
    if not verify_magic(grid):
        raise ArithmeticError("Magic-square invariant failed")
    return {"planet": planet, "order": n, "constant": n * (n*n+1) // 2,
            "grid": grid, "validated": True,
            "provenance": "Normal mathematical magic square; historical orientations may differ",
            "meaning": "Symbolic/traditional, not a scientifically validated effect"}
