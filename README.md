##基于BP神经网络的swjtu教务网登录验证码识别系统
![](bp.png)  

参照[mnielsen](https://github.com/mnielsen)的[教程](http://neuralnetworksanddeeplearning.com/)实现的一个简单BP神经网络，在此向mnielsen表示感谢！

目前，字母分割准确率不高为主要问题，分割错误率大于5%  
分割后的单个字母识别错误率大概小于2%  
后期考虑在字母分割阶段加入神经网络识别过程，提高分割正确率  

###主要源文件

|源文件               |功能                |
|:--------------------|:-----------------|
|pic_graber.py       |验证码训练数据爬取    |
|data_generator.py   |生成训练/验证/测试数据 |
|preprocessor.py     |输入数据预处理        |
|data_loader.py      |从pickle中加载训练数据|
|network.py          |BP神经网络           |
|dean_login.py       |登录测试             |


`data`目录下的`swjtu_verif.pkl.gz`为处理好的训练数据，包含200k张训练图片(单个字符)以及验证和测试图片，`network.pkl`为已经训练好的网络参数
 
###示例：

1.作为api调用
```python
from dean_login import login
res,session=login('教务账号','密码')  #res:登录是否成功，session:登录成功后获取的requests session对象
if res:
    response=session.get('http://jiaowu.swjtu.edu.cn/student/score/ScoreNew.jsp')
    print response.text
```
2.训练  
```python
from data_loader import load_data
from network import Network
training,validate,test=load_data() #将训练数据解压后使用load_data_raw函数速度更快
net=Network([17*17,20,26]) #也可不带参数，默认参数为[17*17,20,26]
net.SGD(training,40,50,3.0,test) #随机梯度下降算法，也可不带参数
```

代码目前还很buggy

