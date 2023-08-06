from setuptools import setup

setup(
    name='browser_driver_manager',
    version='1.0.4',
    description='用于管理浏览器驱动程序的下载和安装',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='刘泉',
    author_email='soundless2023@gmail.com',
    url='https://github.com/weqq2019/browser_driver_manager',
    packages=['browser_driver_manager'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        
    ],
)
