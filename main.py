import math
import time
import os

def rotate(point, ax, ay):
    x, y, z = point
    y, z = y*math.cos(ax) - z*math.sin(ax), y*math.sin(ax) + z*math.cos(ax)
    x, z = x*math.cos(ay) + z*math.sin(ay), -x*math.sin(ay) + z*math.cos(ay)
    return x, y, z

def project(point, scale=20, dist=5):
    x, y, z = point
    factor = scale / (z + dist)
    return int(x * factor + 40), int(y * factor + 12)

def fill_face(canvas, points, char = '#'):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = max(min(xs), 0), min(max(xs), 79)
    min_y, max_y = max(min(ys), 0), min(max(ys), 24)
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            canvas[y][x] = char

def draw_cube(size, ax, ay):
    half = size / 2
    vertices = [(x, y, z) for x in (-half, half)
                          for y in (-half, half)
                          for z in (-half, half)]
    faces = [
        [0,1,3,2],
        [4,5,7,6],
        [0,1,5,4],
        [2,3,7,6],
        [0,2,6,4],
        [1,3,7,5]
    ]
    points3D = [rotate(v, ax, ay) for v in vertices]
    points2D = [project(p) for p in points3D]

    canvas = [[" " for _ in range(80)] for _ in range(25)]
    for f in faces:
        fill_face(canvas, [points2D[i] for i in f], char="#")

    os.system("cls" if os.name == "nt" else "clear")
    print("\n".join("".join(row) for row in canvas))

def main():
    size = int(input("Size of the cube: "))
    ax, ay = 0.0, 0.0
    while True:
        draw_cube(size, ax, ay)
        ax += 0.05
        ay += 0.03
        time.sleep(0.05)

if __name__ == "__main__":
    main()