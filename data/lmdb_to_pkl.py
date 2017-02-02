# Created by wz on 17-1-15.
# encoding=utf-8
import lmdb,cPickle,caffe
import numpy as np

def main():
    env=lmdb.open('/home/wz/project/caffe/examples/mnist/mnist_train_lmdb',readonly=True)
    #env=lmdb.open('swjtu_verif_test_lmdb',readonly=True)
    with env.begin() as txn:
        raw_datum=txn.get(b'00000000')

    datum=caffe.proto.caffe_pb2.Datum()
    datum.ParseFromString(raw_datum)

    flat_x=np.fromstring(datum.data,dtype=np.uint8)
    x=flat_x.reshape(datum.channels,datum.height,datum.width)
    y=datum.label
    print x,y


if __name__=='__main__':
    main()