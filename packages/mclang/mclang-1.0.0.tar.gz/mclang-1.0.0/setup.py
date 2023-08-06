import setuptools

with open('README.md') as f:
    long_description = f.read()

required_modules = []

setuptools.setup(
    name='mclang',
    version='1.0.0',
    author='Legopitstop',
    description='Read and write to .lang files.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/legopitstop/mclang',
    packages=setuptools.find_packages(),
    install_requires=required_modules,
    license='MIT',
    keywords=['Minecraft: Bedrock Edition', 'lang', 'language', 'translate'],
    author_email='officiallegopitstop@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6'
)