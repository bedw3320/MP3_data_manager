import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bedw3320", # Replace with your own username
    version="0.0.1",
    author="William Bédard",
    author_email="bedard.w@gmail.com",
    description="Package for mp3 tagger file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
   'eyed3',
   'spotipy',
   'PIL'
]
)