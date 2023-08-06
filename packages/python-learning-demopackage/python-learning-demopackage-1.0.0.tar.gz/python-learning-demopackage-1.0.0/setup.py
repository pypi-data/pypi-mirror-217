from setuptools import setup


def readme_content():
    with open("README.rst", encoding='utf-8') as rc:
        return rc.read()


setup(name='python-learning-demopackage', version='1.0.0', description='a demo package developed for python study',
      packages=['testsublib'], py_modules=['testmodule'], author='ahoo', author_email='ahoo@gmail.com',
      long_description_content_type='text/x-rst', long_description=readme_content(), license='MIT',
      url="https://www.baidu.com")
