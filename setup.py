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
    install_requires=[''],
    package_data={'hunger': ['templates/hunger/*',
                             'templates/templated_email/hunger/*',]},
)
