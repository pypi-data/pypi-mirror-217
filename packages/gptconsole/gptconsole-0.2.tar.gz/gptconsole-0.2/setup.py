from setuptools import setup

setup(
    name='gptconsole',
    version='0.2',
    py_modules=['gptconsole'],
    entry_points={
        'console_scripts': [
            'gpt = gptconsole.main:__main__',
        ]
    },
    author='John Vouvakis Manousakis',
    author_email='ioannis_vm@berkeley.edu',
    description='One of many command line interfaces to OpenAI\'s GPT models.',
    url='',
)
