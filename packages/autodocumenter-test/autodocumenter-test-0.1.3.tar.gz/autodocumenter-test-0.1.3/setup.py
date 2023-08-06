import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'autodocumenter-test',   
    packages=find_packages(where='./src'),
    package_dir={'autodocumenter': 'src/autodocumenter'},
    # package_data={'autodocumenter': ['autodocumenter/compile_doc/templates/*.rst', 'autodocumenter/generate_doc/utils/config.yaml']},
    version = "0.1.3",      
    license='MIT',  
    description = ('Generate docstrings using ChatGPT and generate Sphinx documentation from the project structure.'),  
    long_description=read('README.md'),
    author = 'Dusan Grujicic',                  
    author_email = 'dusangr22@gmail.com',  
    keywords = ["documentation", "ChatGPT", "Sphinx"],   
    python_requires='>3.9',
    install_requires=[
        'Sphinx>=6.2.1',
        "sphinx-rtd-theme>=1.2.2",
        "astor>=0.8.1",
        "click>=8.1.3",
        "openai>=0.27.8",
        "aiometer>=0.4.0",
        "aiomisc>=17.3.2",
        "alive_progress>=3.1.4",
        "openlimit>=0.2.7",
        "PyYAML>=6.0"
    ],
    entry_points={
        'console_scripts': ['autodocumenter = autodocumenter.__main__:main']
    }
)