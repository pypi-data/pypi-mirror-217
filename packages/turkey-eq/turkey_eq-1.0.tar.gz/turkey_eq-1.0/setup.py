from setuptools import setup

setup(
   name='turkey_eq',
   version='1.0',
   description='A library for processing Turkey earthquake data',
   license='MIT',
   author='Egor Yarygin',
   author_email='egoryarygin2003@mail.ru',
   url='https://github.com/Egor-Yarygin/turkey-earthquake-lib',
   packages=[''], 
   install_requires=[
        "numpy",
        "matplotlib",
        "requests",
        "h5py",
        "python-dateutil",
        "scipy",
        "pytest"
        ], 
   python_requires='>=3',
)
