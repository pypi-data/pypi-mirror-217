from setuptools import setup

setup(
    name='proxysocksgen',
    version='1.0.0',
    description='Collect socks5 proxies from github repositories and return 1 proxy',
    author='zelt-dev',
    author_email='fgytre14@gmail.com',
    packages=[''],
    install_requires=[
        'aiohttp',
    ],
)
