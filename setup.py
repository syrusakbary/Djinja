from setuptools import setup, find_packages

version = ".".join(map(str, __import__("djinja").__version__))

setup(name='Djinja',
    version=version,
    description='A package that makes possible the integration of Jinja2 in Django, in a clean way.',
    long_description=open('README.rst').read(),
    author='Syrus Akbary Nieto',
    author_email='dimension.net@gmail.com',
    url='http://github.com/syrusakbary/djinja',
    license='BSD',
    packages=find_packages(),
    install_requires=['Jinja2', 'django>=1.2'],
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)