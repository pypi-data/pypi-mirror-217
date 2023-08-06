from setuptools import setup, find_packages

with open("README.md", encoding="UTF-8") as file:
    long_description = file.read()

setup(
    name="whatsapp-api-client-python",
    version="0.0.38",
    description=(
        "This library helps you easily create"
        " a Python application with WhatsApp API."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="GREEN API",
    author_email="support@green-api.com",
    url="https://github.com/green-api/whatsapp-api-client-python",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    license=(
        "Creative Commons Attribution-NoDerivatives 4.0 International"
        " (CC BY-ND 4.0)"
    ),
    install_requires=["requests==2.31.0"],
    python_requires=">=3.8"
)
