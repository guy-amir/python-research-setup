from setuptools import setup, find_packages

setup(
    name="python-research-setup",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'pyresearch-init=pyresearch_init.init_research:main',  # CLI command
        ],
    },
)
