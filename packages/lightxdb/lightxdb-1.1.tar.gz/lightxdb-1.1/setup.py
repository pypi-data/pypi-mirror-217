from distutils.core import setup
setup(
  name = 'lightxdb',         # How you named your package folder (MyLib)
  packages = ['lightxdb'],   # Chose the same as "name"
  version = '1.1',      # Start with a small number and increase it with every change you make
  license='GNU',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Command-line tool for interacting with the LightXDB environment',   # Give a short description about your library
  author = 'Hadi Jaffrey',                   # Type in your name
  author_email = 'plixinofficial@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Lightspace-Official/lightX-DevBox',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Lightspace-Official/lightX-DevBox/archive/refs/tags/v2.0-beta.tar.gz',    # I explain this later on
  keywords = ['lightx', 'devbox', 'lightx-devbox'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'certifi',
          'charset-normalizer',
          'idna',
          'requests',
          'urllib3',
          'wincertstore',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.9',
  ],
)