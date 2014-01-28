from setuptools import setup, find_packages

setup(
    name = "Tapi",
    version = "0.1",
    packages = find_packages(),
    scripts = ['tapi.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3',
                        'requests>=0.13.9',
                        'jsonpath-rw>=1.2.3'
                        ],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },

    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
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
