import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cryptlex.lexfloatclient",
    version="4.15.0",
    author="Cryptlex LLP",
    author_email="support@cryptlex.com",
    description="LexFloatClient API wrapper for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cryptlex/lexfloatclient-python",
    packages=setuptools.find_packages(),
    package_data={'cryptlex': ['lexfloatclient/libs/win32/**/*.dll', 'lexfloatclient/libs/linux/**/**/*.so', 'lexfloatclient/libs/macos/**/*.dylib']},
    keywords='cryptlex lexfloatclient licensing',
    license='Proprietary',
    classifiers=[
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
        "License :: Other/Proprietary License",
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)