from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='universal_framework_vk',
    version='0.23',
    packages=find_packages(),
    description='universal framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Viral Killer',
    author_email='jules3313@gmail.com',
    license='MIT',
    install_requires=[
        # List of your package dependencies
        # For example: 'numpy>=1.18.1'
    ],
)
