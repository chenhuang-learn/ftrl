from math import exp, log, sqrt

class ftrl_proximal(object):
    '''
    this is an adaptive-learning-rate sparse logistic-regression with
    efficient L1-L2-regularization
    '''
    def __init__(self, alpha, beta, L1, L2, num_dim):
        self.alpha = alpha
        self.beta = beta
        self.L1 = L1
        self.L2 = L2
        self.num_dim = num_dim

        self.n = [0.] * num_dim
        self.z = [0.] * num_dim
        self.w = {}

    def predict(self, x):
        '''
        INPUT:
            x: [(index, value), ...]
        OUTPUT:
            probability of p(y=1|x)
        '''
        # build w on the fly using z and n
        z = self.z
        n = self.n
        w = {}

        wTx = 0.
        for f_i, f_v in x:
            if f_i >= self.num_dim or f_i < 0:
                raise ValueError("Wrong Feature Index: " + str(f_i))
            sign = -1. if z[f_i] < 0 else 1.
            if sign * z[f_i] <= self.L1:
                w[f_i] = 0.
            else:
                w[f_i] = (sign * self.L1 - z[f_i]) / (self.L2 +
                        (self.beta + sqrt(n[f_i])) / self.alpha)
            wTx += w[f_i] * f_v

        # cache current w for update stage
        self.w = w
        return 1. / (1. + exp(-max(min(wTx, 35.), -35.)))

    def update(self, x, p, y):
        '''
        INPUT:
            X: [(index, value), ...]
            p: click probability prediction
            y: answer
        MODIFIES:
            self.n
            self.z
        '''
        n = self.n
        z = self.z
        w = self.w

        ans = 1. if y > 0 else 0.

        for f_i, f_v in x:
            g = (p - ans) * f_v
            sigma = (sqrt(n[f_i] + g * g) - sqrt(n[f_i])) / self.alpha
            z[f_i] += g - sigma * w[f_i]
            n[f_i] += g * g

