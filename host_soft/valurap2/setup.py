from setuptools import setup, find_packages

setup(
    name = 'valurap2',
    version = '0.0.1',
    url = 'https://github.com/sevikkk/valurap.git',
    author = 'Vsevolod Lobko',
    author_email = 'seva@sevik.org',
    description = 'Valurap host software',
    packages = find_packages(),    
    install_requires = [
        'aiohttp',
        'aiomonitor',
        'requests'
    ],
    extras_require = {
        "hw": [
            'luma.oled',
            'pyserial',
            'pyserial-asyncio',
            'smbus2',
            'spidev',
        ]
    } ,
    entry_points = {
        'console_scripts': [
        ]
    }
)
