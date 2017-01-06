# encoding=utf-8
import requests
from PIL import Image
from StringIO import StringIO
from pic_crawler import login as _login
from network import recognize
from preporcessor import remove_noise, split


def get_verif_img(session):
    imgurl = 'http://jiaowu.swjtu.edu.cn/servlet/GetRandomNumberToJPEG'
    headers = {
        'Host': 'jiaowu.swjtu.edu.cn',
        'Referer': "http://jiaowu.swjtu.edu.cn/service/login.jsp?user_type=student"
    }
    response = session.get(imgurl, headers=headers, timeout=5)
    img = Image.open(StringIO(response.content))
    image = remove_noise(img)
    return image


def login(username, password):
    session = requests.session()
    verif_img = get_verif_img(session)
    res, chars = split(None, None, verif_img)
    if res is False:
        return False, False
    verif_code = []
    for i in chars:
        verif_code.append(recognize(i))
    verif_code = ''.join(verif_code)

    if _login(username, password, session, verif_code):
        return True, session
    else:
        return False, None


def benchmark():
    count = 0
    for i in range(1000):
        res, session = login('20132185', 'w1995119100')  # 教务账号
        if res:
            print "登录成功"
            count += 1
        else:
            print "失败"
    print count


if __name__ == '__main__':
    benchmark()
