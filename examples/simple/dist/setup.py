import setuptools

setuptools.setup(
    name="open_alchemy_simple_models",
    version="0.1",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "OpenAlchemy",
    ],
    include_package_data=True,
)
