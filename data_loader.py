import gzip,cPickle

def load_data():
    with gzip.open("data/swjtu_verif.pkl.gz", "rb") as f:
        data = cPickle.load(f)
        return data


def load_data_raw():
    with open("data/swjtu_verif.pkl", "rb") as f:
        data = cPickle.load(f)
        return data
