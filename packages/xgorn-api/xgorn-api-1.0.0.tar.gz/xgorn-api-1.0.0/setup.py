import re
from setuptools import setup, find_packages


with open('xgorn_api/__init__.py', encoding='utf-8') as f:
    version = re.findall(r'__version__ = \'(.+)\'', f.read())[0]


with open('xgorn_api/api.py', encoding='utf-8') as f:
    base_url = re.findall(r'self\.base_url = \'(.+)\'', f.read())[0]


with open('README.md', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='xgorn-api',
    version=version,
    description=f'API Interface for {base_url}',
    long_description=readme,
    long_description_content_type='text/markdown',
    url=base_url,
    author='xgorn',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='api scraper bypasser translator client library python',
    project_urls={
        'Web': base_url,
        'Documentation': base_url+'/docs'
    },
    python_requires='~=3.7',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)