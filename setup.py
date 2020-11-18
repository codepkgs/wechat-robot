
from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='wechatrobot',
    version='1.0.2',
    keywords='wechat, robot, wechatrobot, wechat-robot, wechat-webhook',
    description='send message to wechat robot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='zhanghe',
    author_email='x_hezhang@126.com',
    url='https://github.com/x-hezhang/wechat-robot',
    license='GNU GPLv3',
    packages=find_packages(),
    install_requires=['requests']
)
