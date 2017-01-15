# Created by wz on 17-1-12.
# encoding=utf-8
import cPickle
import lmdb,caffe
import numpy as np

def main():
    with open('swjtu_verif.pkl') as f:
        training,validate,test=cPickle.load(f)

    l=len(training)
    print l
    print training[0][0].dtype
    map_size=training[0][0].nbytes+training[0][1].nbytes
    env=lmdb.open('swjtu_verif_train_lmdb',map_size=map_size*l*10)
    with env.begin(write=True) as txn:
        for i in xrange(l):
            datum=caffe.proto.caffe_pb2.Datum()
            datum.channels=1
            datum.height=17
            datum.width=17
            datum.data=training[i][0].tobytes()
            datum.label=np.argmax(training[i][1])
            str_id="{:08}".format(i)
            txn.put(str_id,datum.SerializeToString())

    l=len(validate)
    print l
    map_size=validate[0][0].nbytes+validate[0][1].nbytes
    env=lmdb.open('swjtu_verif_test_lmdb',map_size=map_size*l*10)
    with env.begin(write=True) as txn:
        for i in xrange(l):
            datum=caffe.proto.caffe_pb2.Datum()
            datum.channels=1
            datum.height=17
            datum.width=17
            datum.data=validate[i][0].tobytes()
            datum.label=np.argmax(validate[i][1])
            str_id="{:08}".format(i)
            txn.put(str_id,datum.SerializeToString())

if __name__=='__main__':
    main()

