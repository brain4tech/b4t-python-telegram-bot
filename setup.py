from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='b4t-python-telegram-bot',
    version='1.0.0',
    description='Simple and lightweight Telegram Bot',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/brain4tech",
    author='Brain4Tech',
    author_email='brain4techyt@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='telegram, bot, api',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests']
)
