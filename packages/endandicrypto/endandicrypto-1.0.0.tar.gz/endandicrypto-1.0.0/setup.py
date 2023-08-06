from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='endandicrypto',
  version='1.0.0',
  description='Send and receive cryptocurrency in a simple and intuitive way',
  long_description=open('README.md').read(),
  url='',  
  author='Riccardo Verardi',
  author_email='endandito@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='endandicrypto', 
  packages=find_packages(),
  install_requires=[''] 
)