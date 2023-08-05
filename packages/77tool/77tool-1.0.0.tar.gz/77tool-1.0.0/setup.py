import setuptools
setuptools.setup(
    name="77tool",
    version="1.0.0",
    author="linrol",
    author_email="linrolmail@gmail.com",
    description="77 branch tool",
    install_requires=['click', 'setuptools'],
    long_description=open("README.md", 'r').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/linrol/77tool",
    entry_points={
        'console_scripts': [
            '77tool = tool:cli'
        ]
    },
    scripts=['tool.py'],
    packages=setuptools.find_namespace_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
