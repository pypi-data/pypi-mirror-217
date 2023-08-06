from setuptools import setup, find_packages

setup(
    name='yapairwise_testing',
    version='0.1',
    packages=find_packages(),
    description='A library for pairwise testing package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Linha nova    
    url='https://github.com/claytonfraga/yapairwise_testing',
    author='Clayton Vieira Fraga Filho',
    author_email='claytonfraga@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
    
)
