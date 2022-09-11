from setuptools import setup, find_namespace_packages

setup(name='assistant',
      version='0.0.1',
      description='assistant',
      url='https://github.com/PavelStelmakhV/personal-assistant-with-cli',
      author='Stelmakh Pavel',
      author_email='stelmahpv13@ukr.net',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['assistant=assistant.main:main']},
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ]
)