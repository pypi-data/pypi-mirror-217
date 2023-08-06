from setuptools import setup, find_packages


VERSION = '2.0.0'
DESCRIPTION = 'Abby integration into python'

setup(
    name="abbyPython",
    version=VERSION,
    description=DESCRIPTION,
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='conversion',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
