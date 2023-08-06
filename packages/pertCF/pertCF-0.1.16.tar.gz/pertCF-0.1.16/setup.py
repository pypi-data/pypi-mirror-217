from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()
#
setup_args = dict(
    name='pertCF',
    version='0.1.16',
    description='PertCF explainer is a counterfactual based XAI technique.',
    # long_description_content_type="text/markdown",
    # long_description=README + '\n\n' + HISTORY,
    license='MIT',
    # packages=find_packages(),
    scripts = ['./pertCF/Case.py', './pertCF/Data.py', './pertCF/Similarity.py', './pertCF/PertCF.py'],
    author='Betül Bayrak',
    author_email='betul.bayrak@ntnu.no',
    keywords=['pertCF', 'XAI', 'Explanation', 'Counterfactual'],
    # url='https://github.com/ncthuc/elastictools',
    download_url='https://pypi.org/project/pertCF/'
)

install_requires = [
    'numpy',
    'shap',
    'pandas',
    'scipy',
    'category_encoders'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)