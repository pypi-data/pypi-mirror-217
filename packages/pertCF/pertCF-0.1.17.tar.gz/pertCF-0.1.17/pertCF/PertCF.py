import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.special import softmax
from .Case import Case
from .Data import Data
from .Similarity import Similarity
import shap


class PertCF:
    def __init__(self,
                 dataset,
                 label,
                 model=None,
                 feature_names={'categorical': None, 'numeric': None, 'ordinal': None},
                 encode_cat='auto',
                 global_sim='euclidean',
                 local_sim='auto',
                 shap_param={'sample': 300, 'Visualize': False, 'Normalize': False},
                 candidate_param={'thresh': 0.5, 'max_iter': 10}
                 ):
        self.data = Data(dataset, label, feature_names)
        self.model = model
        self.similarity = Similarity(self.data, encode_cat, global_sim, local_sim)
        self.encoded_data = self.similarity.encode(self.data.data.drop([self.data.label], axis=1))

        self.__calculate_shap__(sample=shap_param['sample'], vis=shap_param['Visualize'],
                                normalize=shap_param['Normalize'])

        self.cand_thresh = candidate_param['thresh']
        self.cand_max_iter = candidate_param['max_iter']

    def explain(self, c):
        case = Case(c, self.data)
        case.explanation = self.generateCF(case)
        return case.represent_explanation('PertCF', type='instance-based')

    def generateCF(self, case):
        # Todo: try this approach with different encodings, because there might be different number of features and
        #  the method might not be applicable to all
        count = 0
        nun = self.find_NUN(case)

        features = self.data.names.to_list()
        features.remove(self.data.label)

        candidate_df = pd.DataFrame([nun], columns=self.data.names)
        step_size, candidate_encoded, prev_candidate_encoded = None, None, None
        prev_candidate = pd.Series(data=None, index=features)
        candidate = nun.drop(self.data.label)  # pd.Series(data=None, index=features)
        candidate_y = nun[self.data.label]

        def __candidate_generator__():

            nonlocal count, case, candidate_df, prev_candidate, candidate, features, candidate_y, \
                source, target, candidate_encoded, prev_candidate_encoded, step_size

            prev_candidate = candidate.copy()
            if count:
                prev_candidate_encoded = candidate_encoded
            source_encoded = self.similarity.encode([source.drop(self.data.label)]).iloc[0]
            target_encoded = self.similarity.encode([target.drop(self.data.label)]).iloc[0]

            # Todo: calculate candidates from encoded versions and try to decode candidate
            difference = pd.Series(target_encoded.values[0] - source_encoded.values[0], index=target_encoded.index)

            for f in features:
                if f in self.data.categorical_names:
                    if (1 - difference[f]) > 0.5:
                        f_val = target[f]
                    else:
                        f_val = source[f]
                else:
                    diff = target[f] - source[f]
                    f_val = source[f] + self.shap_df.loc[target[self.data.label]][f] * diff

                candidate[f] = f_val

            candidate_encoded = self.similarity.encode([candidate]).values[0]
            candidate_y = self.model.predict([candidate_encoded])[0]

            # if candidate_y is not from case's class add it to the CF cand list as a valid candidate
            if candidate_y != case.y:
                cnd = candidate.copy()
                cnd[self.data.label] = candidate_y
                candidate_df.loc[len(candidate_df)] = cnd
                if count:
                    step_size = self.similarity.dist_func([candidate_encoded], [prev_candidate_encoded])
            count += 1

        while True:
            if count >= self.cand_max_iter:
                # Nun considered as the 1st candidate so cand list never will be empty
                return candidate_df.iloc[-1]  # return latest generated valid candidate
            elif count == 0:  # start
                source = case.case
                target = nun


            else:  # elif count < self.cand_max_iter:
                if candidate_y == case.y:  # if cnd and case is from same class
                    source = pd.concat([candidate, pd.Series(
                        {self.data.label: candidate_y})])  # a new cf candidate between 'candidate' and 'source'
                else:
                    if count == 1 or step_size < self.cand_thresh:
                        target = source.copy()
                        source = candidate.copy()
                        source[self.data.label] = candidate_y
                    else:
                        return candidate_df.iloc[-1]  # return latest generated valid candidate

            __candidate_generator__()  # just call candidate generator

    def find_NUN(self, case):
        if self.data is not None:
            # filter df to select instances from all classes except case.y
            nun_data = self.data.data.loc[self.data.data[self.data.label] != case.y].dropna()  # .reset_index(drop=True)

            # Encode case TODO: I might need to send encode_cat as param
            case_x_encoded = self.similarity.encode(case.case.to_frame().T.drop([self.data.label], axis=1)).values[0]

            # Encode dataset (X)
            nun_data_encoded = self.similarity.encode(nun_data.drop([self.data.label], axis=1))

            # Measure the distance between
            nun_id = nun_data_encoded.apply(lambda row: self.similarity.dist_func([case_x_encoded], [row.values.T]),
                                            axis=1).idxmin()
            return nun_data.loc[nun_id]

        else:
            raise Exception('Not found: provide the background \'dataset\' to calculate Nearest Unlike Neighbour')

    # SHAP value calculation for each class
    # 'vis' (bool): visualize calculated shap values with a bar plot
    def __calculate_shap__(self, vis, sample, normalize):
        df = self.encoded_data.sample(sample) if len(self.encoded_data) > sample else self.encoded_data.copy()

        # Create shap kernel explainer using model and training data
        shap_explainer = shap.KernelExplainer(self.model.predict_proba, df)

        # Shap values calculated by explainer
        self.shap_values = shap_explainer.shap_values(df)

        # Bar plot of calculated shap values (Each color implies a class)
        if vis:
            shap.summary_plot(shap_values=self.shap_values, features=self.encoded_data,
                              class_inds="original", plot_type='bar',
                              class_names=self.data.range[self.data.label]['categories'])
            plt.show()

        # Create df from mean of shap values (map the order of features and classes)
        importance = []
        for i in range(len(self.shap_values)):
            importance.append(np.mean(np.abs(self.shap_values[i]), axis=0))

        if normalize:
            importance = softmax(importance)

        self.shap_df = pd.DataFrame(importance, index=self.model.classes_, columns=self.model.feature_names_in_)
