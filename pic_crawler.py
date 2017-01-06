# encoding=utf-8
import requests
from multiprocessing import Process, Lock, Value
from PIL import Image
from StringIO import StringIO
from pytesseract import image_to_string
from preporcessor import remove_noise

index = Value('i', 0)
locknum = Lock()
lockTesser = Lock()


def getImg(session):
    imgurl = 'http://jiaowu.swjtu.edu.cn/servlet/GetRandomNumberToJPEG'
    headers = {
        'Host': 'jiaowu.swjtu.edu.cn',
        'Referer': "http://jiaowu.swjtu.edu.cn/service/login.jsp?user_type=student"
    }
    response = session.get(imgurl, headers=headers, timeout=5)
    img = Image.open(StringIO(response.content))

    image = remove_noise(img)

    global lockTesser
    lockTesser.acquire()
    code = image_to_string(image).strip()
    lockTesser.release()
    valid = filter(lambda a: a.isalpha(), code)
    text = valid.upper()
    return [text, img, image] if len(valid) == 4 else [False, False, False]


def login(username, password, session, text):
    url = 'http://jiaowu.swjtu.edu.cn/servlet/UserLoginSQLAction'
    form = {
        'url': "../usersys/index.jsp",
        'OperatingSystem': "",
        "Browser": "",
        "user_id": str(username),
        "password": str(password),
        "set_language": "cn",
        "user_type": "student",
        "btn1": "",
        "ranstring": text
    }
    headers = {
        'Host': 'jiaowu.swjtu.edu.cn',
        'Referer': "http://jiaowu.swjtu.edu.cn/service/login.jsp?user_type=student",
    }
    response = session.post(url, headers=headers, data=form, timeout=5)
    if u'登录成功' in response.text:
        return True
    return False


def logout(session):
    url = 'http://jiaowu.swjtu.edu.cn/servlet/UserLogoutAction?'
    response = session.get(url)


def getOne(username, password):
    session = requests.Session()
    text, img, image = getImg(session)
    if not text:
        return
    res = login(username, password, session, text)
    if (res):
        global locknum
        with locknum:
            global index
            tempindex = index.value
            index.value += 1

        print tempindex, index, text
        img.save("pic/%s_%s_0.jpg" % (tempindex, text), 'JPEG')
        image.save("pic/%s_%s_1.jpg" % (tempindex, text), 'JPEG')
        logout(session)
    else:
        print 'oops', text


def labor(username, password, times):
    for i in range(times):
        try:
            getOne(username, password)
        except Exception, e:
            pass


def main(start=0, times=1000):
    global index
    index.value = start
    pool = []
    for i in range(4):
        pool.append(Process(target=labor, args=('', '', times)))  # 教务账号

    for p in pool:
        p.start()

    for p in pool:
        p.join()


if __name__ == '__main__':
    main(0, 1)
