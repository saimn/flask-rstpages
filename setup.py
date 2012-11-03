from setuptools import setup, find_packages

setup(
    name='Flask-RSTPages',
    version='0.1',
    url='http://flask-rstpages.rtfd.org/',
    license='BSD',
    author='Simon Conseil',
    author_email='simon.conseil@gmail.com',
    description='Adds support for reStructuredText to a Flask application',
    long_description=open('README').read(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['Flask', 'Pygments', 'docutils'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
