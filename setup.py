from distutils.core import setup

import setuptools

setup(name='ambrtop',
      version=f'0.0.3',
      description='An Asynchronous API Wrapper for the AmbrTop API',
      author='Furiã',
      packages=['aiohttp_client_cache', 'aiohttps', 'aiosqlite', 'beautifulsoup4'],
      package_dir={'': 'ambrtop_py'},
)