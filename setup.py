from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name="gif_pygame",
    version="0.1.0",
    author="Zeperox",
    description="A pygame addon for animated image files",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pygame-ce", "pillow", "warnings"],
    keywords=["python", "pygame", "addon", "image", "animation", "animated images"],
    classifiers=[
        "Development Status :: 6 - Mature",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: pygame",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7"
)