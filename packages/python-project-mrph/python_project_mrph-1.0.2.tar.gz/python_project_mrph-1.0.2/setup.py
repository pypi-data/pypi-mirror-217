from setuptools import setup


setup(
    name="python_project_mrph",
    version="1.0.2",
    author="MRPH",
    author_email="maggie.hunt@paconsulting.com",
    description="python example package",
    url="https://github.com/maggiehuntpa/python-project-mrph.git",
    download_url='https://github.com/maggiehuntpa/python-project-mrph/archive/refs/tags/Pythonupdate.tar.gz',
    packages=["python_project_mrph"],
    install_requires=[
        "certifi>=2023.5",
        "charset-normalizer>=3.1",
        "idna>=3.4",
        "requests>=2.31",
        "urllib3>=2.0"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',       'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
      ],
)
