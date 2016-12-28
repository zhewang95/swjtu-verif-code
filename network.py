# created by wz in 2016.12.27
# encoding=utf-8
import random, time, cPickle
import numpy as np


# sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# derivative of sigmoid
def sigmoid_prime(x):
    return sigmoid(x) * (1 - sigmoid(x))


# partial derivatives of C a
def cost_derivative(a, y):
    return a - y


class Network():
    def __init__(self, sizes=None):
        self.retrain = True
        if sizes == None:
            self.load_param()
            self.retrain = False
            return
        self.sizes = sizes
        self.layers = len(sizes)
        self.weights = [np.random.randn(b, a) for a, b in zip(sizes[:-1], sizes[1:])]
        self.biases = [np.random.randn(a, 1) for a in sizes[1:]]

    def evaluate(self, test_data):
        res = [(self.feedforward(x[0]).argmax(), x[1].argmax()) for x in test_data]
        return sum(int(a == b) for a, b in res)

    def feedforward(self, x):
        for w, b in zip(self.weights, self.biases):
            x = sigmoid(np.dot(w, x) + b)
        return x

    def SGD(self, training_data, epochs, batch_size, eta, test_data=None):
        l = len(training_data)
        st = time.clock()
        st1 = st
        print "start training at {0}".format(st)
        for i in xrange(epochs):
            random.shuffle(training_data)
            batchs = [training_data[pos:pos + batch_size] for pos in xrange(0, l, batch_size)]
            for batch in batchs:
                self.process_one_batch(batch, eta)
            print "Epoch {0}:".format(i + 1)
            t = time.clock()
            print "completed in {0}".format(t - st)
            st = t
            if test_data:
                print "test result: {0}/{1}".format(self.evaluate(test_data), len(test_data))
        print "{0} Epoches ended in {1}".format(epochs, t - st1)
        if self.retrain:
            self.save_param()

    def process_one_batch(self, batch, eta):
        batch_size = len(batch)
        x = [i[0] for i in batch]
        y = [i[1] for i in batch]
        nabla_w, nabla_b = self.back_propagate(x, y)

        nabla_w = map(lambda x: np.sum(x, axis=0), nabla_w)
        nabla_b = map(lambda x: np.sum(x, axis=0), nabla_b)
        self.weights = [w - eta * ww / batch_size for w, ww in zip(self.weights, nabla_w)]
        self.biases = [b - eta * bb / batch_size for b, bb in zip(self.biases, nabla_b)]

    def back_propagate(self, x, y):
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        nabla_b = [np.zeros(b.shape) for b in self.biases]

        # feedforward
        a = np.array(x)
        alist = [a]
        z = None
        zlist = []
        for w, b in zip(self.weights, self.biases):
            z = np.dot(w, a).transpose(1, 0, 2) + b
            a = sigmoid(z)
            zlist.append(z)
            alist.append(a)

        # backpropagate
        delta = cost_derivative(a, y) * sigmoid_prime(z)
        nabla_b[-1] = delta
        nabla_w[-1] = map(np.dot, delta, alist[-2].transpose(0, 2, 1))
        for l in xrange(2, self.layers):
            sp = sigmoid_prime(zlist[-l])
            delta = np.dot(self.weights[-l + 1].transpose(), delta).transpose(1, 0, 2) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = map(np.dot, delta, alist[-l - 1].transpose(0, 2, 1))

        return nabla_w, nabla_b

    def save_param(self):
        with open("data/network.pkl", "wb") as f:
            pickle = cPickle.Pickler(f)
            pickle.dump([self.sizes, self.layers, self.weights, self.biases])

    def load_param(self):
        with open("data/network.pkl", "rb") as f:
            self.sizes, self.layers, self.weights, self.biases = cPickle.load(f)


def train(size=None, epochs=40, batch_size=50, eta=3.0):
    import data_loader
    a, b, c = data_loader.load_data()
    if size:
        net = Network(size)
    else:
        net = Network([17 * 17, 20, 26])
    net.SGD(a, epochs, batch_size, eta, c)


def recognize(x):
    net = Network()
    res = net.feedforward(x)
    return chr(res.argmax() + ord('A'))


if __name__ == '__main__':
    train()
