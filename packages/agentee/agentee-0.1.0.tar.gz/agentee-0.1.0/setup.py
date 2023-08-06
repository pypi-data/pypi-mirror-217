from setuptools import setup, find_packages

setup(
    name='agentee',
    version='0.1.0',
    description='A framework that builds agents with short-term memory management, longterm management',
    author='Your Name',
    author_email='your-email@example.com',
    packages=find_packages(),
    install_requires=[
        "tiktoken",
        "openai",
        "colorama",
        "jwt",
        "colorlog",
    ],
)
