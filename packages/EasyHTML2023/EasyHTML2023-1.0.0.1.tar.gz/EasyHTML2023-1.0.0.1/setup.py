from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='EasyHTML2023',
    version='1.0.0.1',
    author='SuiBo',
    author_email='534047068@qq.com',
    description='中文的python HTML解析提取器！',
    install_requires=[

    ],
    py_modules=["EasyHTML2023"],
    packages=find_packages(),
    url="https://pypi.org/user/SuiBo/",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
