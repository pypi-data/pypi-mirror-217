from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='bilibili_up',
    version='0.2.1.3',
    author='SuiBo',
    author_email='534047068@qq.com',
    description='bilibili_up获取bilibili视频信息的爬虫！',
    install_requires=[
        'requests',
    ],
    py_modules=["bilibili_up"],
    packages=find_packages(),
    url = "https://pypi.org/user/SuiBo/",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
