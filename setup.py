from setuptools import setup, find_packages

setup(
    name="jeu_math",
    version="0.1.0",
    description="Un jeu de questions mathématiques",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Votre Nom",
    author_email="votre.email@example.com",
    url="https://github.com/votrecompte/jeu_math",  # Remplacez par l'URL de votre projet
    packages=find_packages(),
    install_requires=[
        "Pillow"
    ],
    entry_points={
        "console_scripts": [
            "jeu_math=jeu_math.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
