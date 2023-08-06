from setuptools import setup, find_packages

setup(
    name='bilibili_up',
    version='0.2.1.1',
    author='SuiBo',
    author_email='534047068@qq.com',
    description='bilibili_up',
    install_requires=[
        'requests',
    ],
    py_modules=["bilibili_up"],
    packages=find_packages(),
)
