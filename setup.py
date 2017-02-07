import os

from setuptools import setup

mydir = os.path.dirname(__file__)
if mydir:
    os.chdir(mydir)

version = '0.4'
base_url = 'https://github.com/ShapeCompletion3D/hausdorff_distance'
setup(name='hausdorff_distance',
      author='Jake Varley',
      author_email='jakevarley@gmail.com',
      version=version,
      install_requires=['numpy>=1.8'],
      description='Compute Hausdorff Distance between two meshes',
      long_description='(see project homepage)',
      url=base_url,
      download_url=('%s/archive/v%s.tar.gz' % (base_url, version)),
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: OS Independent',
          'Development Status :: 4 - Beta',
          'Topic :: Scientific/Engineering'
      ],
      py_modules=['hausdorff_distance'],
keywords=['hausdorff', 'numpy'])
