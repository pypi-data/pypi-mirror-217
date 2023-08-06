import codecs
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(name='polybius_square_pro',
      version='1.0.0',
      description='An improved encryption and decryption tool from the Polybius Square.',
      long_description_content_type="text/markdown",
      long_description=long_description,
      classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Topic :: Security :: Cryptography',
      ],
      url='https://github.com/wzyskq/polybius_square_pro',
      author='Foces Becken',
      author_email='',
      license='MIT',
      packages=['polybius_square_pro'],
      install_requires=[],
      keywords=['python', 'polybius', 'cipher', 'encode'],
      zip_safe=False
      )
