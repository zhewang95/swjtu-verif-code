# encoding=utf-8
from PIL import Image
import numpy as np


def noise_detect(ima, x, y, h, w):  # 检测一个点是不是噪点(True)
    vecotr = [(0, -1), (0, 1), (1, -1), (1, 1), (-1, -1), (-1, 1), (1, 0), (-1, 0)]
    all = 0
    if ima.getpixel((x, y)) == 1:
        return False
    for item in vecotr:
        xx = x + item[0]
        yy = y + item[1]
        if xx >= 0 and xx < h and yy >= 0 and yy < w:
            if ima.getpixel((xx, yy)) == 0:
                all += 1
    if all <= 1:
        return True
    else:
        return False


def remove_noise(img):
    image = img.copy()
    w, h = image.size
    for t in range(h):
        for j in range(w):
            rr, gg, bb = image.getpixel((j, t))
            if rr + gg + bb <= 340 and not (rr == gg == bb) and (rr <= 150 or gg <= 150 or bb <= 150):
                image.putpixel((j, t), (0, 0, 0))
            else:
                image.putpixel((j, t), (255, 255, 255))

    image = image.convert('L')  # 清除噪点
    todo = []
    for i in range(w):
        for j in range(h):
            if noise_detect(image, i, j, w, h):
                todo.append((i, j))
            if i == 0 or j == 0:
                todo.append((i, j))
    for item in todo:
        image.putpixel((item[0], item[1]), 255)

    return image


def split(name, chars, img1=None):
    if img1 == None:
        img1 = Image.open(name).convert("1")
    else:
        img1 = img1.convert("1")
    img = (np.array(img1) != True)

    # 清除上下空白区域的噪点
    row = img.sum(axis=1)
    r0, r1 = 0, 21
    rthreshold = 17  # 行比列更容易控制
    for i in range(11, -1, -1):
        if row[i] < 2:
            r0 = i + 1
            break
    for i in range(11, 22, 1):
        if (row[i] < 2):
            r1 = i - 1
            break
    r = r1 - r0 + 1
    if r > rthreshold:
        r1 -= (r - rthreshold) / 2
        r0 += (r - rthreshold) - (r - rthreshold) / 2
    img[:r0] = False
    img[r1 + 1:] = False

    # 清除左右空白区域的噪点
    col = img.sum(axis=0)
    c0, c1 = 0, 54
    cthreshold = 17
    for i in range(0, 27):
        if col[i] > 0:
            c0 = i
            break

    for i in range(54, 27, -1):
        if col[i] > 0:
            c1 = i
            break
    c = c1 - c0 + 1
    img[:, :c0] = False
    img[:, c1 + 1:] = False

    # 字符切割 to be improved
    pixsum = img.sum(axis=0)
    pos = []
    front = c0
    for i in range(c0 + 1, c1 + 1):
        if i <= front:
            continue
        if col[i] != 0 and i - front > 16:
            p = col[front + 5:i].argmin() + front + 5
            pos.append([front, p])
            front = p
        if col[i] == 0 or i == c1:
            if i - front <= 3 and pixsum[front:i].sum() < 10:
                pass
            elif i - front <= 16:
                pos.append([front, i - 1])
            elif i - front > 16:
                p = col[front + 5:i - 5].argmin() + front + 5
                pos.append([front, p])
                pos.append([p, i - 1])
            front = i + 1
            while front <= c1 and col[front] == 0:
                front += 1

    if len(pos) != 4:
        print len(pos), pos
        print "字符分割错误"
        return False, None

    ret = []
    for i in range(4):
        a = pos[i]
        char = img[r0:r1 + 1, a[0]:a[1] + 1]
        char = np.vstack((char, np.zeros((rthreshold - (r1 - r0 + 1), a[1] - a[0] + 1))))
        char = np.hstack((char, np.zeros((rthreshold, cthreshold - (a[1] - a[0] + 1)))))
        y = np.zeros((26, 1))
        if img1 == None:
            b = chars[i]
            y[ord(b.upper()) - ord('A'), 0] = 1
            item = [char.reshape(rthreshold * cthreshold, 1), y]
        else:
            item = char.reshape(rthreshold * cthreshold, 1)
        ret.append(item)
    return True, ret

    # 辅助显示处理后的图片
    '''
    if len(pos)==4:
        for a in pos:
            for i in range(22):
                for j in range(55):
                    if(j>=a[0] and j<=a[1]):
                        img1.putpixel((j, i), 0 if img[i, j] else 255)
                    else:
                        img1.putpixel((j,i),255)

            img1.show()
    return'''
