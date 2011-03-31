from setuptools import setup, find_packages

setup(
    name='Djinja',
    version=".".join(map(str, __import__("djinja").__version__)),
    description='A package that makes possible the integration of Jinja2 in Django, in a clean way.',
    long_description=open('README.rst').read(),
    author='Syrus Akbary Nieto',
    author_email='dimension.net@gmail.com',
    url='http://github.com/syrusakbary/djinja',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
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