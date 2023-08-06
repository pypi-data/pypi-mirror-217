from setuptools import setup, find_packages

setup(
    name='django-genius',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'django = starts.starts:create_folder'
        ]
    },
    install_requires=[
        'django','APScheduler'
    ],
    author='Santhosh Parthiban',
    author_email='santhoshparthiban2002@gmail.com',
    description='A package to create a folder via command line',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
