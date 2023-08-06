from setuptools import setup, find_packages

setup(
    name='Pyneapplee',
    version='0.1',
    url='https://github.com/Yongyi-Liu/Pyneapple',
    author='Author Name',
    author_email='yongyil1998@gmail.com',
    description='Description of my package',
    packages=find_packages(),    
    install_requires=['numpy >=1.11.1', 'matplotlib >=1.5.1'], #dependencies
    classifiers=[
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)