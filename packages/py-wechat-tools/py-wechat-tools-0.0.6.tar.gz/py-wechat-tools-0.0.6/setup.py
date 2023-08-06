import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-wechat-tools",
    version="0.0.6",
    author="mjinnn",
    author_email="932288652@qq.com",
    description="微信小程序/公众号服务端接口集成SDK（非所有接口，持续更新中）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/mjinnn/py-wechat-tools.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests >= 2.20.1",
        "cacheout >= 0.13.1",
        "pycrypto >= 2.6.1",
    ]
)
