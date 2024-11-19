from setuptools import setup, find_packages

setup(
    name="aenzbi_project",
    version="1.0.0",
    description="A Django project with REST API and real-time functionality using Django Channels.",
    author="Ally Elvis Nzeyimana",
    author_email="naelvis6569@gmail.com",
    url="https://github.com/AllyElvis/aenz.git",
    packages=find_packages(exclude=["tests", "docs"]),
    include_package_data=True,
    install_requires=[
        "django>=4.0,<5.0",
        "djangorestframework>=3.12.0,<4.0",
        "channels>=4.0,<5.0",
    ],
    entry_points={
        "console_scripts": [
            "aenzbi_project=manage:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
)
