
# JoltedMod

JoltedMod is a Python package that utilizes OpenAI's chat models to automatically generate Jupyter Notebook or Markdown-based computer science educational materials. This package can be integrated into a frontend application, such as a CLI or API, to serve educational content.

## Features

- Generate Jupyter Notebook or Markdown content based on a given topic
- Highly configurable using tutorial template JSON structure
- Customizable content creator identity and target audience
- Support for GPT-3.5-turbo and other OpenAI models


## Installation

To install JoltedMod, you can use `pip`:

```
pip install jolted_mod
```

## Usage

Here's an example of how to generate a Jupyter Notebook module for a given topic:

```python
import asyncio
from jolted_mod.main import create_notebook_module

topic = "Intro to for loops in Python"
identity = "professor of computer science"
target_audience = "first year computer science students"
is_code = True
model = "gpt-3.5-turbo"

tutorial_content = asyncio.run(create_notebook_module(topic, identity, target_audience, is_code, model))

print(tutorial_content)
```

## Configuration

You can customize the generated content using a JSON template structure that outlines blocks. An example template file can be found in `tutorial_template.json`.

## Development Setup

JoltedMod uses Poetry for project management. To set up a development environment, follow these steps:

1. Install Poetry if you haven't already:

```
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository:

```
git clone https://github.com/yourusername/jolted_mod.git
cd jolted_mod
```

3. Install dependencies using Poetry:

```
poetry install
```

4. Activate the virtual environment:

```
poetry shell
```

Now you're ready to start contributing to JoltedMod!

## Contributing

If you'd like to contribute to JoltedMod, feel free to fork the repository and submit a pull request.

## License

JoltedMod is licensed under the [MIT License](LICENSE).
