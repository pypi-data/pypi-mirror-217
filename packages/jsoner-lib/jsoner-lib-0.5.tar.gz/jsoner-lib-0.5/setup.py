from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='jsoner-lib',
    version='0.5',
    license='MIT',
    author="kradt",
    author_email='sidorenkoarem950@gmail.com',
    packages=find_packages(),
    url='https://github.com/kradt/jsoner',
    keywords='jsoner',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
          'pydantic',
      ],
    python_requires='>=3.11'

)
