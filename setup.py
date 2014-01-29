from setuptools import setup, find_packages

setup(
    name = "Tapi",
    version = "0.1.7",
    packages = find_packages(),
    scripts = ['tapi.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['requests', 'jsonpath_rw'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },

    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Testing'
        ],

    # metadata for upload to PyPI
    author = "Jimmy John",
    author_email = "jimmyislive@gmail.com",
    description = "Framework for testing APIs",
    license = "MIT",
    keywords = "testing api",
    url = "http://tapi.readthedocs.org/en/latest/index.html",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
