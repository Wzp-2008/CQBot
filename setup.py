import os
from setuptools import setup, find_packages

path = os.path.abspath(os.path.dirname(__file__))

setup(
    name="cqbot-sdk",
    version="0.1.0",
    keywords=["cqbot","go-cqhttp"],
    description="a bot sdk of cq-http",
    long_description="just a bot sdk",
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license="MIT Licence",
    author="wzp",
    author_email="minecraftwzpmc@163.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests", "websocket-client"],
    platforms="any",
    scripts=[],
)
