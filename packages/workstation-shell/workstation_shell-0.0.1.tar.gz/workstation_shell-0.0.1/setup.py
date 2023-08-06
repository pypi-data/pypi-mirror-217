from setuptools import setup, find_packages

setup(
    name='workstation_shell',
    version='0.0.1',
    install_requires=[
        'msgpack',
        'pyzmq',
    ],
    packages=find_packages(),
    author='liutelin',
    author_email='liutelin@cvte.com',
    description='workstation shell command line tools.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={  # Optional
        "console_scripts": [
            "workstation_shell=workstation_shell:main"
        ],
    }

)
