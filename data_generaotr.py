import cPickle,gzip,os
from preporcessor import split

def generate():
    training = []
    validate = []
    test = []
    counter = 0
    for j in range(8):
        pardir = '/home/wz/project/swjtuInfo/pic/pic%d/' % j
        filenames = os.listdir(pardir)
        filenames = sorted(filenames)
        for i in filenames:
            ret, chars = split(pardir + i, i.split('_')[-2])
            if not ret:
                continue
            if counter < 1 * 10000:
                training.extend(chars)
            elif counter < 2 * 10000:
                validate.extend(chars)
            elif counter<3*10000:
                test.extend(chars)
            else:
                break
            counter += 1
    data = [training, validate, test]

    # generate light data
    with open("data/swjtu_verif.pkl","wb") as f:
        pickle=cPickle.Pickler(f,protocol=1)
        pickle.dump(data)
    return

    with gzip.open("data/swjtu_verif.pkl.gz", "wb") as f:
        pickle = cPickle.Pickler(f, protocol=1)
        pickle.dump(data)

if __name__=='__main__':
    generate()