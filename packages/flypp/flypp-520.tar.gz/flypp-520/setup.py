from distutils.core import setup
from setuptools import find_packages
with open("README.rst", "r") as f:
  long_description = f.read()
setup(name='flypp',  # 包名
      version='520',  # 版本号
      description='fast fetch',
      long_description=long_description,
      author='flypp',
      author_email='flypp@noexists.com',
      include_package_data=True,
      url='',
      install_requires=["pygame", "pyautogui"],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Topic :: Software Development :: Libraries'
      ],
  entry_points = {
    'console_scripts': ['flypp=flypp.main:main', 'ppegg=flypp.egg:run_egg'],
  },
)