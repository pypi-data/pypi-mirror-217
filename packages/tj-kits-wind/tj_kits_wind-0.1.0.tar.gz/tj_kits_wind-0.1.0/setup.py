from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = "some kits"
long_description = "some kits"

# with open("README.md", "r+") as r:
#     long_description = r.read()

setup(
    name="tj_kits_wind",
    version=VERSION,
    author="tjno-1",
    author_email="tjno-1@qq.com",

    # 描述相关
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['python', 'build-in-module kits'],
    license="MIT",
    url="https://github.com/TJNo-1/tj_kits_wind.git",

    # 自动找到项目中 导入的模块
    packages=find_packages(),
    requires=[
        "pydantic"
    ],
    python_requires=">=3.8",

    # 项目元信息
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
