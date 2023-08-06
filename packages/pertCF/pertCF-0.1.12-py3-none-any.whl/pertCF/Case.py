import pandas as pd
import logging


class Case:
    # x: a data sample <a_1, a_2, a_3, ..., a_n> (Series)
    # y: label of x (ground truth) (int,str)
    # case: combination of x,y (series)
    def __init__(self, case, data):
        self.case = case
        self.data = data
        self.x = self.case.drop(self.data.label)
        self.y = self.case[self.data.label]

        self.explanation = None

    def represent_explanation(self, explainer_name, type='instance-based'):
        if type == 'instance-based':
            logging.basicConfig(level=logging.INFO)

            text = 'Explanation from' + str(explainer_name)
            logging.log(level=20, msg=text)
            res = pd.concat([self.case, self.explanation], axis=1).T
            res['ind'] = ['case', 'explanation']
            res = res.set_index('ind', drop=True)
            logging.log(level=20, msg=res)

            logging.basicConfig(level=logging.debug)

            return res
