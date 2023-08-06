from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='jsoner-lib',
    version='0.3',
    license='MIT',
    author="kradt",
    author_email='sidorenkoarem950@gmail.com',
    packages=find_packages('jsoner'),
    package_dir={'': 'jsoner'},
    url='https://github.com/kradt/jsoner',
    keywords='jsoner',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
          'pydantic',
      ],

)
