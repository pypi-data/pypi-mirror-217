from setuptools import setup, find_packages

setup(
    name='single-linked-list',
    version='0.0.2',
    author='Ahmed K. Madani',
    author_email='ahmedk.madani@outlook.com',
    description='A Python implementation of a singly linked list',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ahmedkmadani/single-linked-list',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
