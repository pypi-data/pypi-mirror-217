from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='ITAfunctionsMVO41',
    version='0.0.1',
    license='MIT License',
    author='Mahmud',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mahmud.alineto@gmail.com',
    keywords='IITAFunctionsMVO41',
    description=u'Functions of MVO-41 from T24',
    packages=['functions_mvo-41'],
    install_requires=['numpy'],)