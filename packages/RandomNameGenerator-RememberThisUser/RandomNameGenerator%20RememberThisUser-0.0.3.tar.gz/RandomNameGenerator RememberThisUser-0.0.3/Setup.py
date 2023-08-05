from setuptools import setup,find_packages

setup(
    name='RandomNameGenerator RememberThisUser',
    version='0.0.3',
    author='RememberThisUser',
    author_email='tatelkirkmatthew@gmail.com',
    description='Creates a random name that you can customize with functions.',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'random',
        'inspect',
    ],
    entry_points={
        'console_scripts': [
            'my_project=my_project.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
