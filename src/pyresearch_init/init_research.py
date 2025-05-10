#!/usr/bin/env python3
"""
Python Research Project Setup Script

This script automates the creation of a well-structured Python research project.
It creates the directory structure, initializes git, sets up a virtual environment,
and creates essential files including README.md, .gitignore, and more.
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
import textwrap
from datetime import datetime


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Set up a new Python research project with best practices."
    )
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument(
        "--location", "-l", default=".", help="Parent directory for the project (default: current directory)"
    )
    parser.add_argument(
        "--description", "-d", default="", help="Short description of the project"
    )
    parser.add_argument(
        "--author", "-a", default="", help="Author name"
    )
    parser.add_argument(
        "--email", "-e", default="", help="Author email"
    )
    parser.add_argument(
        "--python-version", default=">=3.8", help="Python version requirement (default: >=3.8)"
    )
    parser.add_argument(
        "--no-venv", action="store_true", help="Skip virtual environment creation"
    )
    parser.add_argument(
        "--no-git", action="store_true", help="Skip git initialization"
    )
    parser.add_argument(
        "--license", default="MIT", choices=["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "None"], 
        help="License to use (default: MIT)"
    )
    parser.add_argument(
        "--deps", nargs="+", default=["numpy", "pandas", "matplotlib", "pytest"],
        help="Initial Python dependencies (default: numpy pandas matplotlib pytest)"
    )
    
    return parser.parse_args()


def create_directory_structure(project_path):
    """Create the project directory structure."""
    directories = [
        "src",
        f"src/{args.project_name}",
        "notebooks",
        "tests",
        "data/raw",
        "data/processed",
        "results/figures",
        "results/models",
        "docs"
    ]
    
    for directory in directories:
        os.makedirs(os.path.join(project_path, directory), exist_ok=True)
        
    # Create __init__.py files
    Path(project_path / "src" / args.project_name / "__init__.py").touch()
    Path(project_path / "tests" / "__init__.py").touch()
    
    print(f"✅ Created directory structure")


def create_readme(project_path, args):
    """Create README.md with project information."""
    readme_content = f"""# {args.project_name}

{args.description}

## Overview

*Add a more detailed description of your research project here.*

## Setup

```bash
# Clone the repository
git clone <repository-url>
cd {args.project_name}

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
{args.project_name}/
├── README.md              # Project overview, setup instructions
├── LICENSE                # License information
├── .gitignore             # Files to exclude from version control
├── pyproject.toml         # Modern dependency management
├── requirements.txt       # Package dependencies
├── setup.py               # Package installation
├── src/                   # Source code
│   └── {args.project_name}/  # Main package
├── notebooks/             # Research notebooks
├── tests/                 # Unit and integration tests
├── data/                  # Data files
│   ├── raw/               # Original data
│   └── processed/         # Processed data
├── results/               # Output from experiments
│   ├── figures/           # Generated visualizations
│   └── models/            # Trained models
└── docs/                  # Documentation
```

## Usage

*Add basic usage examples here.*

## Contact

{args.author if args.author else 'Your Name'} - {args.email if args.email else 'your.email@example.com'}

"""
    
    with open(project_path / "README.md", "w") as f:
        f.write(readme_content)
    
    print(f"✅ Created README.md")


def create_license(project_path, license_type, author):
    """Create license file based on the chosen license type."""
    if license_type == "None":
        return
    
    current_year = datetime.now().year
    author_name = author if author else "Your Name"
    
    if license_type == "MIT":
        license_content = f"""MIT License

Copyright (c) {current_year} {author_name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    elif license_type == "Apache-2.0":
        license_content = f"""Copyright {current_year} {author_name}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
    elif license_type == "GPL-3.0":
        license_content = f"""Copyright (C) {current_year} {author_name}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
    else:  # BSD-3-Clause
        license_content = f"""Copyright {current_year} {author_name}

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

    with open(project_path / "LICENSE", "w") as f:
        f.write(license_content)
    
    print(f"✅ Created {license_type} LICENSE file")


def create_gitignore(project_path):
    """Create .gitignore file with common Python ignores."""
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE settings
.idea/
.vscode/
*.swp
*.swo

# Project specific
data/raw/*
!data/raw/.gitkeep
data/processed/*
!data/processed/.gitkeep
results/figures/*
!results/figures/.gitkeep
results/models/*
!results/models/.gitkeep

# OS specific
.DS_Store
Thumbs.db
"""
    
    with open(project_path / ".gitignore", "w") as f:
        f.write(gitignore_content)
    
    # Create .gitkeep files to preserve empty directories
    for dir_path in ["data/raw", "data/processed", "results/figures", "results/models"]:
        with open(project_path / dir_path / ".gitkeep", "w") as f:
            pass
    
    print(f"✅ Created .gitignore and .gitkeep files")


def create_pyproject_toml(project_path, args):
    """Create pyproject.toml for modern Python packaging."""
    pyproject_content = f"""[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{args.project_name}"
version = "0.1.0"
description = "{args.description}"
readme = "README.md"
authors = [
    {{name = "{args.author if args.author else 'Your Name'}", email = "{args.email if args.email else 'your.email@example.com'}"}}
]
requires-python = "{args.python_version}"
license = {{"text" = "{args.license}"}}
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]
dependencies = [
    {', '.join(f'"{dep}"' for dep in args.deps)}
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "pytest-cov>=2.12",
    "black>=21.5b2",
    "flake8>=3.9",
    "mypy>=0.812",
]

[tool.setuptools]
package-dir = {{"" = "src"}}

[tool.black]
line-length = 88
target-version = ["py38"]
include = '\\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
"""
    
    with open(project_path / "pyproject.toml", "w") as f:
        f.write(pyproject_content)
    
    print(f"✅ Created pyproject.toml")


def create_setup_py(project_path, args):
    """Create setup.py for backward compatibility."""
    setup_content = f"""from setuptools import setup, find_packages

setup(
    name="{args.project_name}",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    python_requires="{args.python_version}",
)
"""
    
    with open(project_path / "setup.py", "w") as f:
        f.write(setup_content)
    
    print(f"✅ Created setup.py")


def create_requirements_txt(project_path, deps):
    """Create requirements.txt with specified dependencies."""
    with open(project_path / "requirements.txt", "w") as f:
        f.write("\n".join(deps))
    
    print(f"✅ Created requirements.txt with dependencies: {', '.join(deps)}")


def create_sample_code(project_path, project_name):
    """Create sample code files."""
    # Create core.py
    core_content = f"""\"\"\"
Core functionality for the {project_name} project.
\"\"\"

def hello_world():
    \"\"\"Return a greeting message.
    
    Returns:
        str: A greeting message
    \"\"\"
    return f"Hello from {project_name}!"
"""
    
    with open(project_path / "src" / project_name / "core.py", "w") as f:
        f.write(core_content)
    
    # Create utils.py
    utils_content = f"""\"\"\"
Utility functions for the {project_name} project.
\"\"\"

def sample_utility_function(value):
    \"\"\"A sample utility function.
    
    Args:
        value: Input value
        
    Returns:
        The processed value
    \"\"\"
    return value
"""
    
    with open(project_path / "src" / project_name / "utils.py", "w") as f:
        f.write(utils_content)
    
    # Create a sample test
    test_content = f"""\"\"\"
Test cases for {project_name} core functionality.
\"\"\"
import pytest
from {project_name}.core import hello_world


def test_hello_world():
    \"\"\"Test that hello_world returns the expected greeting.\"\"\"
    result = hello_world()
    assert f"Hello from {project_name}!" in result
"""
    
    with open(project_path / "tests" / f"test_core.py", "w") as f:
        f.write(test_content)
    
    # Create a sample Jupyter notebook
    notebook_content = """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# {project_name} Research Notebook\\n",
    "\\n",
    "This is a sample Jupyter notebook for your research project.\\n",
    "\\n",
    "## Setup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "import sys\\n",
    "import os\\n",
    "\\n",
    "# Add the src directory to the path so we can import our package\\n",
    "sys.path.append('../')\\n",
    "\\n",
    "import numpy as np\\n",
    "import pandas as pd\\n",
    "import matplotlib.pyplot as plt\\n",
    "\\n",
    "# Import your package\\n",
    "from src.{project_name} import core\\n",
    "\\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Test Your Package"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Test your package\\n",
    "print(core.hello_world())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Research Notes\\n",
    "\\n",
    "Add your research notes, experiments, and findings here."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
""".replace("{project_name}", project_name)
    
    with open(project_path / "notebooks" / "sample_notebook.ipynb", "w") as f:
        f.write(notebook_content)
    
    print(f"✅ Created sample code and notebook files")


def initialize_git(project_path):
    """Initialize git repository."""
    try:
        subprocess.run(["git", "init"], cwd=project_path, check=True)
        # Create .gitkeep files to track empty directories
        print(f"✅ Initialized git repository")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print(f"❌ Failed to initialize git repository. Is git installed?")
        return False


def create_virtual_environment(project_path, project_name):
    """Create and initialize virtual environment."""
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=project_path, check=True)
        print(f"✅ Created virtual environment")
        
        # Create activation instructions
        if os.name == 'nt':  # Windows
            activate_script = os.path.join(project_path, "venv", "Scripts", "activate.bat")
            activate_cmd = f"venv\\Scripts\\activate"
        else:  # Unix/Linux/Mac
            activate_script = os.path.join(project_path, "venv", "bin", "activate")
            activate_cmd = f"source venv/bin/activate"
        
        # Try to install packages
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(
                    f"venv\\Scripts\\pip install -r requirements.txt", 
                    cwd=project_path, 
                    shell=True, 
                    check=True
                )
            else:
                subprocess.run(
                    f"venv/bin/pip install -r requirements.txt", 
                    cwd=project_path, 
                    shell=True, 
                    check=True
                )
            print(f"✅ Installed dependencies in virtual environment")
        except subprocess.SubprocessError:
            print(f"⚠️ Failed to install dependencies. You can install them manually.")
        
        return activate_cmd
    except subprocess.SubprocessError:
        print(f"❌ Failed to create virtual environment")
        return None


def create_readme_docs(project_path, project_name):
    """Create a simple README in the docs directory."""
    docs_readme = f"""# {project_name} Documentation

This directory contains documentation for the {project_name} project.

## Contents

- Project overview
- API reference
- Usage examples
- Development guidelines

## Building Documentation

To build the documentation locally, you can use Sphinx:

```bash
cd docs
pip install sphinx sphinx_rtd_theme
sphinx-quickstart  # Follow the prompts to set up Sphinx
make html
```

Then open `_build/html/index.html` in your browser.
"""
    
    with open(project_path / "docs" / "README.md", "w") as f:
        f.write(docs_readme)


def main():
    """Main function to set up the project."""
    global args
    args = parse_arguments()
    
    # Normalize project path
    parent_path = Path(args.location).resolve()
    project_path = parent_path / args.project_name
    
    # Check if project directory already exists
    if project_path.exists():
        print(f"⚠️ Directory {project_path} already exists.")
        overwrite = input("Do you want to overwrite it? (yes/no): ").lower().strip()
        if overwrite not in ["yes", "y"]:
            print("Aborting setup.")
            sys.exit(1)
        shutil.rmtree(project_path)
    
    # Create project directory
    os.makedirs(project_path, exist_ok=True)
    print(f"Creating Python research project: {args.project_name}")
    print(f"Location: {project_path}")
    
    # Create directory structure
    create_directory_structure(project_path)
    
    # Create files
    create_readme(project_path, args)
    create_gitignore(project_path)
    create_pyproject_toml(project_path, args)
    create_setup_py(project_path, args)
    create_requirements_txt(project_path, args.deps)
    create_sample_code(project_path, args.project_name)
    create_readme_docs(project_path, args.project_name)
    
    if args.license != "None":
        create_license(project_path, args.license, args.author)
    
    # Initialize git if requested
    git_initialized = False
    if not args.no_git:
        git_initialized = initialize_git(project_path)
    
    # Create virtual environment if requested
    venv_activate_cmd = None
    if not args.no_venv:
        venv_activate_cmd = create_virtual_environment(project_path, args.project_name)
    
    # Print success message
    print("\n" + "=" * 80)
    print(f"🎉 Project {args.project_name} successfully created at {project_path}")
    print("=" * 80)
    
    # Print next steps
    print("\nNext steps:")
    print(f"1. cd {args.project_name}")
    
    if venv_activate_cmd:
        print(f"2. {venv_activate_cmd}")
        print(f"3. Start coding! Check the src/{args.project_name} directory and notebooks/")
    else:
        print(f"2. Create and activate a virtual environment")
        print(f"3. pip install -r requirements.txt")
        print(f"4. Start coding! Check the src/{args.project_name} directory and notebooks/")
    
    if git_initialized:
        print("\nGit repository is initialized. Make your first commit with:")
        print("git add .")
        print('git commit -m "Initial commit"')
    
    print("\nHappy researching! 🚀")


if __name__ == "__main__":
    main()
