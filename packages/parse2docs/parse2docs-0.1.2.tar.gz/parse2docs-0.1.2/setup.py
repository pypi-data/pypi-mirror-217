# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parse2docs']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['parse2docs = parse2docs.app:execute_from_command_line']}

setup_kwargs = {
    'name': 'parse2docs',
    'version': '0.1.2',
    'description': 'Generate usage documentation from Python scripts using the `argparse` module',
    'long_description': "# Parse 2 Docs\n\n`parse2docs` is a Python library that allows you to automatically generate usage documentation in Markdown format from Python scripts using the `argparse` module.\n\n## Features\n\n* Scans the Python script for instances of `argparse.ArgumentParser`.\n* Generates a Markdown file with usage documentation based on the `ArgumentParser` object.\n* The generated documentation includes a table of contents, descriptions of each command line argument, and examples if provided.\n* Works with `ArgumentParser` instances declared at the module level or returned by functions.\n\n## Installation\n\n### Via `pip`\n\n`parse2docs` can be installed via `pip`:\n\n```shell\npip install parse2docs\n```\n\n### Via `poetry`\n\n`parse2docs` can be installed via Poetry. To install the library, clone this repository to your local machine and use Poetry to install:\n\n```shell\ngit clone https://github.com/yourusername/parse2docs.git\ncd parse2docs\npoetry install\n```\n\n## Usage\n\nThere are two ways to use parse2docs, either as a Python module in your script or directly from the command line using the provided command.\n\n### As a Python module\n\n```python\nimport parse2docs\n\n# Path to the Python script\nscript_path = 'path_to_your_python_script.py'\n\n# Generate markdown documentation\nmarkdown = parse2docs.generate_md_from_py_script(script_path)\n\n# Save the markdown to a .md file\nwith open('output.md', 'w') as f:\n    f.write(markdown)\n```\n\nThis will generate a `output.md` file with the usage documentation in Markdown format.\n\n### From the command line\n\n#### Description\n\nThe following usage section was generated using `parse2docs` 😉:\n\n```md\n## Overall Usage Example\n\n`example.py <file_path>`\n\n## Table of Contents\n\n* [file_path](#file_path)\n\n## Options\n\n### file_path\n\nPath to the Python script file containing the ArgumentParser.\n\n**Type**: `Path`\n\n**Required**: Yes\n```\n\nThis will print the usage documentation in Markdown format to the console.\n\n## Testing\n\nWe use `pytest` for testing. Run the tests with the following command:\n\n```bash\npython -m pytest tests/\n```\n\n## Contributing\n\nContributions to `parse2docs` are welcome and awesome! Please submit a pull request or open an issue to discuss potential changes or improvements.\n",
    'author': 'Fernando Cordeiro',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
