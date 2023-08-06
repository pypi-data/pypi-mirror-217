import numpy as np


class Data:

    def __init__(self, dataset, label, feature_names):
        self.data = dataset.reset_index(drop=True)
        self.label = label
        self.names = self.data.columns

        self.X = self.data.drop(label, axis=1)
        self.y = self.data[label]

        try:
            # Set feature types, check if columns are numeric or categoric (if it's not given)
            self.set_numeric(feature_names['categorical'])
            self.set_ordinal(feature_names['ordinal'])
            self.set_categorical(feature_names['numeric'])
        except:
            raise TypeError(
                "feature_names argument format should be like: {'categorical':[], 'numeric':[], 'ordinal':[]}")

        self.set_ranges()

    def set_numeric(self, names):
        if names is None:
            self.numeric_names = self.X.select_dtypes(include=np.number).columns.tolist()
        else:
            self.numeric_names = names

    def set_ordinal(self, names):
        if names is None:
            self.ordinal_names = []
        else:
            self.ordinal_names = names

    def set_categorical(self, names):
        if names is None:
            self.categorical_names = self.X.select_dtypes(include=object).columns.tolist()
            self.categorical_names.append(self.label)
        else:
            self.categorical_names = names

    # sets the ranges for numeric features and keeps the unique categories for categoric features
    def set_ranges(self):
        self.range = {}
        for attribute in self.names:
            if attribute in self.numeric_names:
                self.range[attribute] = {'min': self.data[attribute].min(), 'max': self.data[attribute].max()}
            elif attribute in self.categorical_names:
                self.range[attribute] = {'categories': self.data[attribute].unique()}
            elif attribute in self.ordinal_names:
                self.range[attribute] = {'min': self.data[attribute].min(), 'max': self.data[attribute].max(),
                                         'levels': self.data[attribute].unique()}
            else:
                raise Exception('Attribute type error: ', attribute, '. Attribute type is not supported: ',
                                type(attribute))
