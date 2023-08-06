import category_encoders as ce
import numpy as np
from scipy.spatial.distance import cdist


class Similarity:
    def __init__(self, data, encode_cat, global_sim, local_sim):
        self.data = data
        self.encoder = None  # to be set later
        self.encode_cat = encode_cat
        self.global_sim = global_sim
        self.local_sim = local_sim

        self.set_encoder()
        self.set_local_sim()
        self.set_global_sim()

    def set_encoder(self):
        categorical = self.data.categorical_names

        encoders = {'BackwardDifferenceEncoder': ce.BackwardDifferenceEncoder(categorical),
                    'BaseNEncoder': ce.BaseNEncoder(categorical),
                    'BinaryEncoder': ce.BinaryEncoder(categorical),
                    'CatBoostEncoder': ce.CatBoostEncoder(categorical),
                    'CountEncoder': ce.CountEncoder(categorical),
                    'GLMMEncoder': ce.GLMMEncoder(categorical),
                    'GrayEncoder': ce.GrayEncoder(categorical),
                    'HelmertEncoder': ce.HelmertEncoder(categorical),
                    'JamesSteinEncoder': ce.JamesSteinEncoder(categorical),
                    'LeaveOneOutEncoder': ce.LeaveOneOutEncoder(categorical),
                    'MEstimateEncoder': ce.MEstimateEncoder(categorical),
                    'OneHotEncoder': ce.OneHotEncoder(categorical),
                    'OrdinalEncoder': ce.OrdinalEncoder(categorical),
                    'PolynomialEncoder': ce.PolynomialEncoder(categorical),
                    'QuantileEncoder': ce.QuantileEncoder(categorical),
                    'RankHotEncoder': ce.RankHotEncoder(categorical),
                    'SumEncoder': ce.SumEncoder(categorical),
                    'TargetEncoder': ce.TargetEncoder(categorical),
                    'WOEEncoder': ce.WOEEncoder(categorical)}

        # Todo: implement 'auto', 'manual' and 'else'
        if self.encode_cat in encoders.keys():
            self.encoder = encoders[self.encode_cat].fit(self.data.X, self.data.y)

        elif self.encode_cat == 'auto':
            self.encoder = None  # pick the most performing encoder
        elif self.encode_cat == 'manual':
            self.encoder = None
        else:  # Todo: raise an exception that returns a list of options
            raise Exception('Not found:' + str(self.encode_cat) + ' is not found in encoders. \nEncoders: ' + str(
                list(encoders.keys())))

    def set_local_sim(self):
        if self.local_sim == 'manual':
            pass
        elif self.local_sim == 'auto':
            pass
        else:
            pass

    def set_global_sim(self):
        metrics = {'braycurtis', 'canberra', 'chebyshev',
                   'jaccard', 'hamming', 'cosine', 'sqeuclidean',
                   'cityblock', 'minkowski', 'euclidean'}
        if self.global_sim in metrics:
            self.dist_func = self.__dist_func__
        elif self.global_sim == 'ShapEuclidean':
            self.dist_func = self.__ShapEuclidean_func__
        elif self.global_sim == 'ManualEuclidean':
            self.dist_func = self.__ManualEuclidean_func__
        else:
            pass

    # Returns distance cdist() result for pre-defined metrics
    # p1 ve p2 [[]] 2d list
    def __dist_func__(self, p1, p2):
        return cdist(np.array(p1).astype('float64'), np.array(p2).astype('float64'), metric=self.global_sim)[0][0]

    # Todo: implement a weighted Euclidean
    def __ShapEuclidean_func__(self, p1, p2):
        return cdist(p1, p2, metric='euclidean')[0][0]

    # Todo: implement a weighted Euclidean
    def __ManualEuclidean_func__(self, p1, p2):
        return cdist(p1, p2, metric='euclidean')[0][0]

    def calculate_distance(self, p1, p2):
        self.dist_func(p1, p2)

    def encode(self, x):
        encoded = self.encoder.transform(x)
        if 'intercept' in encoded.columns:
            return encoded.drop(['intercept'], axis=1)
        else:
            return encoded
