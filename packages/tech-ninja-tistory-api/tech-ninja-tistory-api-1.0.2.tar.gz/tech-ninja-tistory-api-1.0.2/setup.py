import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tech-ninja-tistory-api",
    version="1.0.2",
    author="yscho03",
    author_email="yscho03.developer@gmail.com",
    description="Tistory API Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yscho03/tech-ninja-tistory-api",
    project_urls={
        "Bug Tracker": "https://github.com/yscho03/tech-ninja-tistory-api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.13, <2.20",
        "urllib3>=1.26",
    ],    
    dist_dir='dist',    
)