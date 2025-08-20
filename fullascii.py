import math
import time
import os

W, H = 80, 25
CX, CY = W // 2, H // 2

def rotate(p, ax, ay, az):
    x, y, z = p
    # X
    cy, sy = math.cos(ax), math.sin(ax)
    y, z = y*cy - z*sy, y*sy + z*cy
    # Y
    cy, sy = math.cos(ay), math.sin(ay)
    x, z = x*cy + z*sy, -x*sy + z*cy
    # Z
    cz, sz = math.cos(az), math.sin(az)
    x, y = x*cz - y*sz, x*sz + y*cz
    return (x, y, z)

def project(p, scale=15, dist=6):
    x, y, z = p
    f = scale / (z + dist)
    return (int(x * f + CX), int(y * f + CY))

def poly_center(pts3D, face):
    cx = sum(pts3D[i][0] for i in face) / 4.0
    cy = sum(pts3D[i][1] for i in face) / 4.0
    cz = sum(pts3D[i][2] for i in face) / 4.0
    return (cx, cy, cz)

def raster_poly(canvas, poly, ch):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    min_x, max_x = max(min(xs), 0), min(max(xs), W-1)
    min_y, max_y = max(min(ys), 0), min(max(ys), H-1)
    for y in range(min_y, max_y+1):
        xints = []
        j = len(poly) - 1
        for i in range(len(poly)):
            xi, yi = poly[i]
            xj, yj = poly[j]
            if (yi > y) != (yj > y):
                x_cross = (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi
                xints.append(x_cross)
            j = i
        xints.sort()
        for k in range(0, len(xints), 2):
            if k+1 >= len(xints): break
            x_start = int(math.ceil(max(min(xints[k], xints[k+1]), min_x)))
            x_end   = int(math.floor(min(max(xints[k], xints[k+1]), max_x)))
            for x in range(x_start, x_end+1):
                if 0 <= x < W and 0 <= y < H:
                    canvas[y][x] = ch

def draw(size, ax, ay, az):
    half = size/2.0
    verts = [(x, y, z) for x in (-half, half)
                        for y in (-half, half)
                        for z in (-half, half)]

    faces = {
        'Z': [('back',  [0,1,3,2]), ('front', [4,5,7,6])],
        'Y': [('bottom',[0,1,5,4]), ('top',   [2,3,7,6])],
        'X': [('left',  [0,2,6,4]), ('right', [1,3,7,5])],
    }
    face_char = {'Z': '#', 'X': '+', 'Y': '.'}

    pts3D = [rotate(v, ax, ay, az) for v in verts]
    pts2D = [project(p) for p in pts3D]

    cam = (0, 0, 1)  # la caméra regarde vers +Z
    chosen = []

    # Pour chaque axe, choisir la face la plus proche de la caméra
    for axis, pair in faces.items():
        best = None
        best_z = -1e9
        for name, idxs in pair:
            cz = poly_center(pts3D, idxs)[2]
            if cz > best_z:
                best = (idxs, axis, cz)
                best_z = cz
        chosen.append(best)

    # trier par profondeur du fond vers l’avant
    ordered = sorted(chosen, key=lambda x: x[2])

    canvas = [[' ' for _ in range(W)] for _ in range(H)]
    for idxs, axis, _ in ordered:
        poly2D = [pts2D[i] for i in idxs]
        raster_poly(canvas, poly2D, face_char[axis])

    os.system("cls" if os.name == "nt" else "clear")
    print("\n".join("".join(row) for row in canvas))

def main():
    size = int(input("Size of cube: "))
    ax = ay = az = 0.0
    while True:
        draw(size, ax, ay, az)
        ax += 0.05
        ay += 0.03
        az += 0.02
        time.sleep(0.05)

if __name__ == "__main__":
    main()
