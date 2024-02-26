import setuptools

setuptools.setup(
        name="ChordProgressions",
        version="0.1",
        author="Narcis Palomeras",
        description="ChordProgressions.",
        long_description="ChordProgressions is an API for describing chord progressions and render it in SVG.",
        long_description_content_type="text/markdown",
        url="https://github.com/narcispr/ChordProgressions",
        classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
        ],
        packages=["ChordProgressions"],
        install_requires=[
          'drawsvg',
      ]
)

