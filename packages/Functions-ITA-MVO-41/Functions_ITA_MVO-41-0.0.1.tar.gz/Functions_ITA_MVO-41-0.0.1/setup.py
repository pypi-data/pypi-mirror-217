from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='Functions_ITA_MVO-41',
    version='0.0.1',
    license='MIT License',
    author='Mahmud',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mahmud.alineto@gmail.com',
    keywords='ITA MVO-41',
    description=u'Functions of MVO-41 from T24',
    packages=['functions'],
    install_requires=['numpy'],)