from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='discord-ansi',
      version='0.1',
      description='Discord coloured messages!',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['discord_ansi'],
      author_email='geoegii200155@gmail.com',
      zip_safe=False,
      install_requires=[
            "setuptools"
      ]
)
