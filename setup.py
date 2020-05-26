'''
@file: setup.py.py
@author: qxliu
@time: 2020/5/25 19:51
'''
import os

import setuptools

MODULE = 'iESBM'
VERSION = '1.0'
PACKAGES = setuptools.find_packages(where='code')
META_PATH = os.path.join('code', MODULE, '__init__.py')
KEYWORDS = ['Knowledge Graph', 'Entity summarization', 'Benchmarking']
INSTALL_REQUIRES = ['numpy', 'scipy']
if __name__ == '__main__':
	setuptools.setup(
		name=MODULE,
		version=VERSION,
		description='A package for embedding-based entity alignment',
		url='https://github.com/nju-websoft/iESBM.git',
		author='Qingxia Liu',
		author_email='qxliu.nju@gmail.com',
		maintainer='Qingxia Liu',
		maintainer_email='qxliu.nju@gmail.com',
		license='ODC Attribution License (ODC-By)',
		keywords=KEYWORDS,
		packages=setuptools.find_packages(where='code'),
		package_dir={'': 'code'},
		include_package_data=True,
		install_requires=INSTALL_REQUIRES,
		zip_safe=False,
	)