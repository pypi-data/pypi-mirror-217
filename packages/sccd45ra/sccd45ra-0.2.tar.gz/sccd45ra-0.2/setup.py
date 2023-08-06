from setuptools import setup, find_packages

setup(
    name="sccd45ra",
    version="0.2",
    packages=find_packages(),
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    package_data={
        'sccd45ra': ['model/*.h5ad', 'model/*.joblib','feature/*.xlsx'],
    },
)