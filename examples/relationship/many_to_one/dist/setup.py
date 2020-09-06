import setuptools

setuptools.setup(
    name="open_alchemy_relationship_many_to_one_models",
    version="0.1",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "OpenAlchemy",
    ],
    include_package_data=True,
)
