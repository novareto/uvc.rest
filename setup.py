from setuptools import setup, find_packages
import os

version = '1.0'


tests_require = [
    'grokcore.content',
    'grokcore.view [security_publication]',
    'grokcore.view [test]',
    'zope.app.appsetup',
    'zope.app.wsgi',
    'zope.errorview',
    'zope.testing',
    ]


setup(name='uvc.rest',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['uvc'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      install_requires=[
          'setuptools',
          'grok',
          'zope.component',
          'zope.interface',
          'zope.publisher >= 4.2.2',
          'zope.app.publication',
          'gocept.webtoken'
      ],
      )
