import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='auto_behave',
    version='0.0.7',
    packages=find_packages(
        include=['auto_behave']
    ),
    include_package_data=True,
    license='MIT License',
    long_description=README,
    description=(
        'A sphinx extension for behave to auto document'
    ),
    install_requires=[
        'sphinx',
        'docutils',
        'jinja2',
    ],
    url='https://github.com/publons/auto_behave',
    author='Brandon Scott-Hill',
    author_email='brandon.scotthill@publons.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Documentation :: Sphinx'
    ],
    python_requires='>=3.6',
)
