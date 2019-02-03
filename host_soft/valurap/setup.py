from setuptools import setup, find_packages

setup(
    name = 'valurap',
    version = '0.0.1',
    url = 'https://github.com/sevikkk/valurap.git',
    author = 'Vsevolod Lobko',
    author_email = 'seva@sevik.org',
    description = 'Valurap host software',
    packages = find_packages(),    
    install_requires = [
        'aiohttp==3.5.4',
        'aiomonitor==0.4.3',
        'luma.oled==3.1.0',
        'pyserial==3.4',
        'pyserial-asyncio==0.4',
        'smbus2==0.2.3',
        'spidev==3.2',
    ],
    entry_points = {
        'console_scripts': [
            'home=valurap.scripts.home:main',
            'talk=valurap.scripts.talk:main',
            'printer=valurap.printer:main',
        ]
    }
)
