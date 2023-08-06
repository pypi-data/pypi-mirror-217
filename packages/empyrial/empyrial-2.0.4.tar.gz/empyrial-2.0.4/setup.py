from setuptools import setup

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='empyrial',
    version='2.0.4',
    description='An Open Source Portfolio Management Framework for Everyone 投资组合管理',
    py_modules=['src/empyrial'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ssantoshp/Empyrial',
    author="Santosh Passoubady",
    author_email="santoshpassoubady@gmail.com",
    license='MIT',
    install_requires=[
        'numpy',
        'matplotlib',
        'datetime',
        'empyrical',
        'quantstats',
        'yfinance',
        'ipython',
        'fpdf',
        'pyportfolioopt'

    ],
)
