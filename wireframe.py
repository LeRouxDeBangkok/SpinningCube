import math
import time
import os

def rotate(point, ax, ay, az):
    x, y, z = point
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    x, y = x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az)
    return x, y, z


def project(point, scale=15, dist=5):
    x, y, z = point
    factor = scale / (z + dist)
    return int(x * factor + 40), int(y * factor + 12)


def draw_line(canvas, x1, y1, x2, y2, char="#"):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        if 0 <= x1 < 80 and 0 <= y1 < 25:
            canvas[y1][x1] = char
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def draw_cube(size, ax, ay, az):
    half = size / 2
    vertices = [(x, y, z) for x in (-half, half)
                for y in (-half, half)
                for z in (-half, half)]
    edges = [(0, 1), (0, 2), (0, 4),
             (1, 3), (1, 5),
             (2, 3), (2, 6),
             (3, 7),
             (4, 5), (4, 6),
             (5, 7),
             (6, 7)]

    points = [project(rotate(v, ax, ay, az)) for v in vertices]
    canvas = [[" " for _ in range(80)] for _ in range(25)]

    for e in edges:
        x1, y1 = points[e[0]]
        x2, y2 = points[e[1]]
        draw_line(canvas, x1, y1, x2, y2, "#")

    os.system("cls" if os.name == "nt" else "clear")
    print("\n".join("".join(row) for row in canvas))


def main():
    size = int(input("Cube size: "))
    ax = ay = az = 0.0
    while True:
        draw_cube(size, ax, ay, az)
        ax += 0.05
        ay += 0.03
        az += 0.02
        time.sleep(0.05)


if __name__ == "__main__":
    main()
