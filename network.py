# encoding=utf-8
# created by wz in 2016.12.27
import random, time, json, sys
import numpy as np


# sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# derivative of sigmoid
def sigmoid_prime(x):
    return sigmoid(x) * (1 - sigmoid(x))


# cross-entropy cost function
class CrossEntropyCost():
    @staticmethod
    def delta(a, y, z):
        return a - y

    @staticmethod
    def calCost(a, y):
        return sum(np.sum(np.nan_to_num(-y * np.log(a) - (1 - y) * np.log(1 - a)), axis=1))


# quadratic cost function
class QuadraticCost():
    @staticmethod
    def delta(a, y, z):
        return (a - y) * sigmoid_prime(z)

    @staticmethod
    def calCost(a, y):
        return sum((np.linalg.norm(a - y, ord=2, axis=1) ** 2) / 2)  # 2 order norm


class Network:
    def __init__(self, sizes=None, cost=QuadraticCost):
        self.sizes = sizes
        self.layers = len(sizes)
        self.weights = [np.random.randn(b, a) / np.sqrt(a) for a, b in zip(sizes[:-1], sizes[1:])]
        self.biases = [np.random.randn(a, 1) for a in sizes[1:]]
        self.cost = cost

    def evaluate(self, test_data):
        res = [(self.feedforward(x[0]).argmax(), x[1].argmax()) for x in test_data]
        return sum(int(a == b) for a, b in res)

    def feedforward(self, x):
        for w, b in zip(self.weights, self.biases):
            x = sigmoid(np.dot(w, x) + b)
        return x

    def SGD(self, training_data, epochs, batch_size, eta, lmbda=1.0, test_data=None,
            train_cost=False,
            train_accuracy=False,
            test_cost=False,
            test_accuracy=False):
        l_train = len(training_data)
        l_test = len(test_data) if test_data else 0

        train_costs = []
        train_accuracys = []
        test_costs = []
        test_accuracys = []

        st = time.clock()
        st1 = st
        print "start training at {0:.2f}S".format(st)
        for i in xrange(epochs):
            random.shuffle(training_data)  # stochastic
            batchs = [training_data[pos:pos + batch_size] for pos in xrange(0, l_train, batch_size)]
            for batch in batchs:
                self.process_one_batch(batch, eta, lmbda, l_train)
            print "Epoch {0}:".format(i + 1)
            t = time.clock()
            print "completed in {0:.2f}S".format(float(t - st))
            st = t

            if train_cost:
                cost = self.calCost(training_data, lmbda)
                print "train cost:{0:.4f}".format(1.0*cost)
                train_costs.append(cost)
            if train_accuracy:
                accuracy = self.evaluate(training_data) / l_train
                print "train accuracy:{0}".format(accuracy)
                train_accuracys.append(1.0 * accuracy / l_train)

            if test_data:
                if test_cost:
                    cost = self.calCost(test_data, lmbda)
                    print "test cost:{0:.4f}".format(1.0*cost)
                    test_costs.append(cost)
                if test_accuracy:
                    corrects = self.evaluate(test_data)
                    accuracy = 1.0 * corrects / l_test
                    test_accuracys.append(accuracy)
                    print "test accuracy: {0}/{1}={2:.3}".format(corrects, l_test, accuracy)

        print "{0} Epochs ended in {1:.2f}S".format(epochs, t - st1)
        self.save_param()
        return train_costs, train_accuracys, test_costs, test_accuracys

    def process_one_batch(self, batch, eta, lmbda, l_train):
        batch_size = len(batch)
        x = [i[0] for i in batch]
        y = [i[1] for i in batch]
        nabla_w, nabla_b = self.back_propagate(x, y)

        nabla_w = map(lambda x: np.sum(x, axis=0), nabla_w)
        nabla_b = map(lambda x: np.sum(x, axis=0), nabla_b)
        self.weights = [(1 - lmbda * eta / l_train) * w - eta * ww / batch_size for w, ww in zip(self.weights, nabla_w)]
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
        delta = self.cost.delta(a, y, z)
        nabla_b[-1] = delta
        nabla_w[-1] = map(np.dot, delta, alist[-2].transpose(0, 2, 1))
        for l in xrange(2, self.layers):
            sp = sigmoid_prime(zlist[-l])
            delta = np.dot(self.weights[-l + 1].transpose(), delta).transpose(1, 0, 2) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = map(np.dot, delta, alist[-l - 1].transpose(0, 2, 1))

        return nabla_w, nabla_b

    def calCost(self, data, lmbda):
        c0 = sum(self.cost.calCost(self.feedforward(a[0]), a[1]) for a in data)/len(data)
        c1 = sum((np.linalg.norm(w)) ** 2 for w in self.weights) * lmbda / len(data) / 2
        return c0 + c1

    def save_param(self):
        data = {"sizes": self.sizes,
                "weights": [a.tolist() for a in self.weights],
                "biases": [a.tolist() for a in self.biases],
                "cost": str(self.cost.__name__)}
        with open("data/network.json", "wb") as f:
            json.dump(data, f)


def load_network():
    with open("data/network.json", "rb") as f:
        data = json.load(f)
    sizes = data["sizes"]
    cost = getattr(sys.modules[__name__], data["cost"])
    net = Network(sizes, cost=cost)
    net.weights = data["weights"]
    net.biases = data["biases"]
    return net


def train(size=None, epochs=40, batch_size=50, eta=0.5, lmbda=2.0):
    import data_loader
    a, b, c = data_loader.load_data_raw()
    if size:
        net = Network(size)
    else:
        net = Network([17 * 17, 20, 26])
    net.SGD(a, epochs, batch_size, eta, lmbda, c,test_accuracy=True)


def recognize(x):
    net = load_network()
    res = net.feedforward(x)
    return chr(res.argmax() + ord('A'))


if __name__ == '__main__':
    train()
