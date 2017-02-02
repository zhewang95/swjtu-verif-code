##基于神经网络的swjtu教务网登录验证码识别系统
###说明
参照[mnielsen](https://github.com/mnielsen)的[教程](http://neuralnetworksanddeeplearning.com/)实现的一个简单BP神经网络，在此向mnielsen表示感谢！  

使用caffe深度学习框架实现的分支

###源文件&文件夹

|名字　　　　                 |功能   　　             |
|:--------------------------|:----------------------|
|solver.prototxt            |model solver定义文件    |
|network_layers.prototxt    |model网络各层定义文件　　 |
|data/                      |train/test lmdb文件夹   |
|snapshot/                  |存储训练过程快照　　　　　|

 
###示例：
训练
```shell
caffe train -solver solver.prototxt
```
