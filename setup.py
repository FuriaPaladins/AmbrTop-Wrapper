from distutils.core import setup

import setuptools

setup(name='ambrtop',
      version=f'0.0.1',
      description='Python Distribution Utilities',
      author='Furiã',
      packages=['aiohttp_client_cache', 'aiohttps', 'aiosqlite'],
      package_dir={'': 'ambrtop_py'},
)