import math
import os
import time
import shutil

term_size = shutil.get_terminal_size()
WIDTH, HEIGHT = min(160, term_size.columns), min(44, term_size.lines)
zbuffer = [0.0] * (WIDTH * HEIGHT)
buffer = [' '] * (WIDTH * HEIGHT)

A = B = C = 0.0

distanceFromCam = 100
K1 = 20
incrementSpeed = 0.6
horizontalOffset = 0.0

def calculateX(i, j, k):
    return j*math.sin(A)*math.sin(B)*math.cos(C) - k*math.cos(A)*math.sin(B)*math.cos(C) + j*math.cos(A)*math.sin(C) + k*math.sin(A)*math.sin(C) + i*math.cos(B)*math.cos(C)

def calculateY(i, j, k):
    return j*math.cos(A)*math.cos(C) + k*math.sin(A)*math.cos(C) - j*math.sin(A)*math.sin(B)*math.sin(C) + k*math.cos(A)*math.sin(B)*math.sin(C) - i*math.cos(B)*math.sin(C)

def calculateZ(i, j, k):
    return k*math.cos(A)*math.cos(B) - j*math.sin(A)*math.cos(B) + i*math.sin(B)

def calculateForSurface(cubeX, cubeY, cubeZ, ch):
    global buffer, zbuffer
    x = calculateX(cubeX, cubeY, cubeZ)
    y = calculateY(cubeX, cubeY, cubeZ)
    z = calculateZ(cubeX, cubeY, cubeZ) + distanceFromCam
    ooz = 1 / z
    xp = int(WIDTH / 2 + horizontalOffset + K1 * ooz * x * 2)
    yp = int(HEIGHT / 2 + K1 * ooz * y)
    idx = xp + yp * WIDTH

    if 0 <= idx < WIDTH * HEIGHT:
        if ooz > zbuffer[idx]:
            zbuffer[idx] = ooz
            buffer[idx] = ch

def draw_cube(cubeWidth, offset):
    global horizontalOffset
    horizontalOffset = offset
    for cubeX in frange(-cubeWidth, cubeWidth, incrementSpeed):
        for cubeY in frange(-cubeWidth, cubeWidth, incrementSpeed):
            calculateForSurface(cubeX, cubeY, -cubeWidth, '@')
            calculateForSurface(cubeWidth, cubeY, cubeX, '$')
            calculateForSurface(-cubeWidth, cubeY, -cubeX, '~')
            calculateForSurface(-cubeX, cubeY, cubeWidth, '#')
            calculateForSurface(cubeX, -cubeWidth, -cubeY, ';')
            calculateForSurface(cubeX, cubeWidth, cubeY, '+')

def frange(start, end, step):
    while start < end:
        yield start
        start += step

def main():
    global A, B, C, buffer, zbuffer
    cubeSize = float(input("Cube size: "))

    try:
        while True:
            buffer = [' '] * (WIDTH * HEIGHT)
            zbuffer = [0.0] * (WIDTH * HEIGHT)
            draw_cube(cubeSize, 0)
            os.system('cls' if os.name == 'nt' else 'clear')
            for i in range(HEIGHT):
                print("".join(buffer[i*WIDTH:(i+1)*WIDTH]))

            A += 0.05
            B += 0.05
            C += 0.01

            time.sleep(0.016)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()