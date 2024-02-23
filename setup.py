import setuptools

setuptools.setup(
        name="SongHarmony",
        version="0.1",
        author="Narcis Palomeras",
        description="SongHarmony.",
        long_description="SongHarmony is an API for describing the harmony of a song and render it in SVG.",
        long_description_content_type="text/markdown",
        url="https://github.com/narcispr/SongHarmony",
        classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
        ],
        packages=["SongHarmony"],
        install_requires=[
          'drawsvg',
      ]
)

