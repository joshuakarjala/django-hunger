from setuptools import setup
import hunger

DESCRIPTION = "A Django app to manage a private beta phase."

try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

version_str = '%d.%d.%d' % (hunger.VERSION[0], hunger.VERSION[1], hunger.VERSION[2])

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django',
]

INSTALL_REQUIRES = ['']
try:
    import importlib
except ImportError:
    INSTALL_REQUIRES.append('importlib')

tests_require = [
    'Django>=1.3',
]

setup(
    name='django-hunger',
    version=version_str,
    packages=[
        'hunger',
        'hunger.contrib',
    ],
    author='Joshua Karjala-Svenden',
    author_email='joshua@fluxuries.com',
    url='https://github.com/joshuakarjala/django-hunger/',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    include_package_data=True,
    package_data={'hunger': ['templates/hunger/*',
                             'templates/templated_email/hunger/*',]},
    )
