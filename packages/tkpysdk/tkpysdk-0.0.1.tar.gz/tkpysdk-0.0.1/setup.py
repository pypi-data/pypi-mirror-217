import setuptools

setuptools.setup(
    name="tkpysdk",
    version="0.0.1",
    description="300k sdk for python",
    author="Hao W",
    license="Copyright 2023, 300k ltd, All rights reserved",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ]

)
