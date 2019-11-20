from setuptools import setup, find_packages

with open('requirements-dev.txt') as fp:
    extras_require = fp.read()

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='priority_queue',
    version='1.0.0',
    python_requires='>=3.6',
    description='Thread-safe priority queue',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JakubTesarek/priority_queue',
    author='Jakub Tesárek',
    author_email='jakub@tesarek.me',
    license='APACHE LICENSE 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers'
    ],
    keywords='queue thread',
    packages=find_packages(),
    extras_require={'test': extras_require}
)
