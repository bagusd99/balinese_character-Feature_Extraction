import cv2
import numpy as np
import sys
import os
import glob
import csv


def hitung_diagonal(res_akhir):  # Proses ekstraksi fitur diagonal
    img_data = res_akhir
    x, y = img_data.shape[:2]
    # data = np.zeros((70))
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print(data)
    len_data = (len(data))
    len_x = x
    len_y = y
    # print(len_data)
    area = -1
    m = 0
    while m < len_x:  # lebar smua
        n = 0
        while n < len_y:  # panjang smua
            area = area + 1
            batas_x = n + 10
            batas_y = m + 10
            i = n

            while i < batas_x:  # 10x10
                y = m
                x = i
                pembagi = 0
                # print("loop i ke-", i)
                while (x >= n) and (y < batas_y):  # 10x10
                    if(img_data[y][x] == 1):
                        data[area] = data[area]+1
                    x = x-1
                    y = y+1
                    pembagi = pembagi+1
                    # print("pembagi", pembagi)
                # print("area",area)
                data[area] = data[area]
                # print("data area", data[area])
                i = i+1
            # print("data", data)
            i = m+1
            while i < batas_y:
                y = i
                x = batas_x-1
                pembagi = 0
                while (x >= n) and (y < batas_y):
                    if(img_data[y][x] == 1):
                        data[area] = data[area]+1
                    x = x-1
                    y = y+1
                    pembagi = pembagi+1
                data[area] = data[area]
                i = i+1
            data[area] = round(data[area]/19, 3)
            # print(data)
            n = n+10
        m = m+10

    i = 0
    while i < 54:
        area = area+1
        j = 0
        while j < 9:
            data[area] = data[i] + data[j]
            j = j+1
        data[area] = round(data[area]/9, 3)
        i = i+9

    i = 0
    while i < 9:
        area = area+1
        j = 0
        while j < 54:
            data[area] = data[i] + data[j]
            j = j+9
        data[area] = round(data[area]/6, 3)
        i = i+1
    print(data)
    return data


# Membaca File dalam folder testdata
folders = glob.glob('testdata/*')
imagenames_list = []
for folder in folders:
    for f in glob.glob(folder+'/*.jpg'):
        imagenames_list.append(f)
# print(imagenames_list)


fitur = []
for image in imagenames_list:
    img = cv2.imread(image)

    # proses grayscaling
    H, W = img.shape[:2]
    gray = np.zeros((H, W), np.uint8)
    for i in range(H):
        for j in range(W):
            gray[i, j] = np.clip(0.07 * img[i, j, 0] + 0.72 *
                                 img[i, j, 1] + 0.21 * img[i, j, 2], 0, 255)
    # print("gray = ", gray)

    # proses binerisasi
    threshold = 125
    X, Y = gray.shape[:2]
    biner = np.zeros((X, Y), np.uint8)
    for i in range(X):
        for j in range(Y):
            if gray[i, j] > threshold:
                biner[i, j] = 0
            else:
                biner[i, j] = 1
    # print("biner = ", biner)

    # crop and resize
    collect = np.argwhere(biner)
    y1, x1 = collect.min(axis=0)
    y2, x2 = collect.max(axis=0)
    res_awal = biner[y1:y2, x1:x2]
    res_akhir = cv2.resize(res_awal, (90, 60))
    fitur1 = hitung_diagonal(res_akhir)
    fitur.append(fitur1)

#  Save hasil Ekstraksi Fitur
f = open('Diagonal-Feature.csv', 'w')
w = csv.writer(f)
for index, data in enumerate(fitur):
    rows = data
    w.writerow(rows)
f.close()
