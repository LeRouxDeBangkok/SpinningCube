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
    denom = z + dist
    if abs(denom) < 1e-6:
        denom = 1e-6  # évite division par zéro
    factor = scale / denom
    return int(x * factor + 40), int(y * factor + 12)

def polygon_center(points3D, indices):
    cx = sum(points3D[i][0] for i in indices) / len(indices)
    cy = sum(points3D[i][1] for i in indices) / len(indices)
    cz = sum(points3D[i][2] for i in indices) / len(indices)
    return (cx, cy, cz)

def normal(points3D, face):
    p1, p2, p3 = [points3D[i] for i in face[:3]]
    u = (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
    v = (p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2])
    n = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
    return n

def dot (a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def fill_face(canvas, points2D, char):
    xs = [p[0] for p in points2D]
    ys = [p[1] for p in points2D]
    min_x, max_x = max(min(xs), 0), min(max(xs), 79)
    min_y, max_y = max(min(ys), 0), min(max(ys), 24)
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            inside = False
            j = len(points2D) - 1
            for i in range(len(points2D)):
                xi, yi = points2D[i]
                xj, yj = points2D[j]
                if ((yi>y) != (yj>y)) and (x < (xj-xi)*(y-yi)/(yj-yi+1e-6)+xi):
                    inside = not inside
                j = i
            if inside:
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

    face_data = []
    for f in faces:
        n = normal(points3D, f)
        if dot(n, (0,0,1)) < 0:
            cz = polygon_center(points3D, f)[2]
            face_data.append((cz, f))
    face_data.sort()

    chars = "#@%O+=-"
    for i, (_, f) in enumerate(face_data):
        pts2D = [points2D[j] for j in f]
        fill_face(canvas, pts2D, chars[i % len(chars)])

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