from setuptools import setup

LONG_DESCRIPTION = """Transfinite ordinal arithmetic up to epsilon-zero.

Implements ordinal addition, multiplication and factorization, with ordinals
automatically rendered as LaTeX inside Jupyter notebooks and consoles
for easy readability.
"""

setup(
    name="transfinite",
    version="0.5.0",
    description="Transfinite ordinals for Python",
    long_description=LONG_DESCRIPTION,
    author="Alex Riley",
    license="MIT",
    packages=["transfinite"],
    zip_safe=False,
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="set-theory ordinals arithmetic factorization LaTeX",
    python_requires=">=3.6.0",
    project_urls={
        "Source": "https://github.com/ajcr/transfinite/",
        "Tracker": "https://github.com/ajcr/transfinite/issues",
    },
)
