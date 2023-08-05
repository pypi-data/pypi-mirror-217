from setuptools import setup, find_packages

setup(
    name='omneer',
    version='0.1',
    packages=find_packages(include=['omneer', 'omneer.*']),
    url='http://omneer.xyz',
    license='MIT',
    author='William Blair',
    author_email='william.blair0708@gmail.com',
    description='Advanced personalized medicine diagnostics for neurodegenerative disorders',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy>=1.19.0',
        'pandas>=1.2.0',
        'matplotlib>=3.3.0',
        'scipy>=1.6.0',
        'requests>=2.25.0',
        'beautifulsoup4>=4.9.0',
        'pytest>=6.0.0',
        'flake8>=3.9.0',
        'black>=21.6b0',
        'scikit-learn>=0.24.0',
        'torch>=1.9.0',
        'tqdm>=4.62.0',
        'xgboost>=1.4.0',
        'joblib>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'omneer=omneer.lc.main:main',
        ],
    },
)
