import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cryptlex.lexfloatclient",
    version="4.7.0",
    author="Cryptlex, LLC",
    author_email="support@cryptlex.com",
    description="LexFloatClient API wrapper for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cryptlex/lexfloatclient-python",
    packages=setuptools.find_packages(),
    package_data={'cryptlex': ['lexfloatclient/libs/win32/**/*.dll', 'lexfloatclient/libs/linux/**/**/*.so', 'lexfloatclient/libs/macos/**/*.dylib']},
    keywords='cryptlex lexfloatclient licensing',
    classifiers=[
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
    ]
)