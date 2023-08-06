import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openioe", # Replace with your own username
    version="1.0.0",
    author="Venkataswamy R",
	scripts=['openioe\openioe_apis.py'] ,
    author_email="opensourceioe@gmail.com",
    description="Open IoE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://openioe.gnanodaya.org/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)