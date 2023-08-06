from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='re_it',
    version='1.0.0.1',
    author='SuiBo',
    author_email='534047068@qq.com',
    description='中文的python网络请求库！',
    install_requires=[

    ],
    py_modules=["re_it"],
    packages=find_packages(),
    url="https://pypi.org/user/SuiBo/",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
