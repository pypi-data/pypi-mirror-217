from setuptools import setup, find_packages

setup(
    name='demo-csv-linter-leandro',
    description='demo python CLI tool to lint csv files',
    long_description="Hola",
    packages=find_packages(),
    author='Alfredo Deza',
    entry_points="""
    [console_scripts]
    csv-linter=csv_linter.main:main
    """,
    install_requires=['click==7.1.2', 'pandas==1.2.0'],
    version='0.0.1',
    url='https://github.com/alfredodeza/python-cli',
)
