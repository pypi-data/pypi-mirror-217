from setuptools import setup, find_packages


setup(
    name='jsoner-lib',
    version='0.1',
    license='MIT',
    author="kradt",
    author_email='sidorenkoarem950@gmail.com',
    packages=find_packages('jsoner'),
    package_dir={'': 'jsoner'},
    url='https://github.com/kradt/jsoner',
    keywords='jsoner',
    install_requires=[
          'pydantic',
      ],

)
