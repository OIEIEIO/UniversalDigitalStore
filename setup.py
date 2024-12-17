from setuptools import setup, find_packages

setup(
    name="UniversalDigitalStore",
    version="1.0.0",
    description="A Flask-based digital store with Monero payment integration.",
    author="Jorge Alonso",
    author_email="support@oieieio.net",
    url="https://github.com/OIEIEIO/UniversalDigitalStore",
    packages=find_packages(),  # Automatically finds all Python packages in the project
    include_package_data=True,  # Includes non-code files like templates and static
    install_requires=[
        "flask",
        "flask_sqlalchemy",
        "requests",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "universal_store=UniversalDigitalStore.api.app:create_app",  # Optional: Create CLI entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
