from setuptools import setup, find_packages
import subprocess
import os

cf_remote_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)
assert "." in cf_remote_version

assert os.path.isfile("cf_remote/version.py")
with open("cf_remote/VERSION", "w", encoding="utf-8") as fh:
    fh.write(f"{cf_remote_version}\n")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='b4t-python-telegram-bot',
    version=cf_remote_version,
    description='Simple and lightweight Telegram Bot',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brain4tech\b4t-python-telegram-bot",
    author='Brain4Tech',
    author_email='brain4techyt@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='telegram, bot, api',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests']
)
