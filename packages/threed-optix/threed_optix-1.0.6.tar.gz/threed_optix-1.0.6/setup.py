from setuptools import setup, find_packages


setup(
    name='threed_optix',
    version='1.0.6',
    license='',
    author="Elika Ron",
    author_email='alikaron@3doptix.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://3doptix.com',
    keywords='',
    install_requires=[
        'requests',
        'pandas',
        'matplotlib'
    ]
)
