# Layman Summary Generator for Abstracts of Research Papers

This script generates layman summaries from scientific abstracts using a large language model from OpenAI's GPT-4. As input, the script uses the API from OpenAIRE to get content from the Netherlands Research Portal.

Authors: Maurice Vanderfeesten, assisted by OpenAI's GPT-4 model code generator.
[Coding conversation with ChatGTP](https://chat.openai.com/share/5334616a-e47f-4da9-b3d9-c6f989ff3adf)

## Purpose

The purpose of this script is to make complex scientific abstracts understandable to a broader audience. It generates summaries tailored for four specific audiences: children, journalists, politicians, and teachers. The script uses OpenAI's GPT-4 language model to generate these summaries.

The summaries are then saved in both CSV and Excel formats, making them easy to share and analyze.

## Getting Started

### Requirements
Before you begin, you'll need to have the following:

1. Git installed on your machine. You can download it from the [official Git website](https://git-scm.com/downloads).

2. Python installed on your computer. You can download it from the [official Python website](https://www.python.org/downloads/). This script requires Python 3.6 or later.

#### Copy this code

Once you have Git and Python installed, clone the project's repository from GitHub using the following command in your terminal:

```bash
git clone https://github.com/ubvu/Layman_Summaries.git
```

Then navigate into the project's directory:

```bash
cd Layman_Summaries
```

#### Create a Virtual Python Environment

It's recommended to use a virtual environment for running this script to avoid conflicts with your system's Python packages.

1. Create a virtual environment:

   If you're using Unix or MacOS, run:
   
   ```bash
   python3 -m venv env
   ```

   If you're using Windows, run:

   ```bash
   py -m venv env
   ```

2. Activate the virtual environment:

   If you're using Unix or MacOS, run:

   ```bash
   source env/bin/activate
   ```

   If you're using Windows, run:

   ```bash
   .\env\Scripts\activate
   ```

3. After activating the virtual environment, install the necessary Python packages using pip and the provided requirements.txt file:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

The script uses a YAML configuration file, `config.yaml`, which should be in the same directory as the script. This configuration file contains several parameters:

- `openai_api_key`: Your OpenAI API key. You can find your API key in your OpenAI account at [https://platform.openai.com/account/api-keys].

- `aimodel`: The AI model to use. Options include `gpt-3.5-turbo` and `gpt-4`. For more Chat Completion models, check [https://platform.openai.com/docs/models/continuous-model-upgrades].

- `max_tokens`: The maximum number of tokens in the generated summaries. Depending on the complexity of the abstract, you may need to adjust this number. Note that the OpenAI API has a maximum limit.

- `data_url`: The URL from which to fetch data. The provided URL is for the OpenAIRE API, fetching content from the Netherlands Research Portal. For more parameters check the OpenAIRE API documentation [https://graph.openaire.eu/develop/api.html#rproducts]

- `audiences`: A list of audience types and their corresponding system messages. Each audience item has two properties: `name` and `message`. `name` refers to the name of the audience (e.g., "Child", "Journalist"), and `message` contains instructions for the AI on how to create the summary tailored for that audience.

A sample configuration file, `config-example.yaml`, is provided. To use it, rename `config-example.yaml` to `config.yaml` and fill in your OpenAI API key and other preferences.

## Usage
To use the script can by either using the command line or a simple GUI

### Running the Script in the Command Line

To run the script, navigate to the directory containing the script and the configuration file, and then execute the Python script:

```bash
python run_as_cli.py
```

You can also run the script in the command line and pass certain parameters such as `data_url`, `aimodel`, and `max_tokens`. The parameters passed in the command line will override the corresponding values in the `config.yaml` file.

Here is an example of how to run the script in the command line with parameters:

```bash
python run_as_cli.py --data_url https://api.openaire.eu/search/researchProducts?format=json&doi=10.1364/josaa.465900 --aimodel gpt-4 --max_tokens 200
```

The script will fetch the data, generate the summaries, save the files and print the first 10 rows of the DataFrame in the command line.

### Running the Script in the Graphical User Interface (GUI)

The script can also be run using a graphical user interface (GUI). This interface provides a simple way to generate summaries without having to use the command line. 

To run the script in the GUI, navigate to the directory containing the script and the configuration file, and then execute the Python script:

```bash
python run_as_gui.py
```

The GUI will display fields for `AI Model`, `Max Tokens`, and `Data URL`. These fields are pre-filled with the default values from the `config.yaml` file. You can change these values directly in the GUI.

Once you've set the desired parameters, click the `Generate Summaries` button. The script will fetch the data, generate the summaries, safe the fimes and display the summaries in the GUI.

## License

This project is licensed under CC0 1.0 Universal.

## Troubleshooting

### tkinter 
When you receive the error message `ModuleNotFoundError: No module named 'tkinter'` usually indicates that Python can't find the `tkinter` module, which is used for creating graphical user interfaces. This might be because:

1. You're using a version of Python that doesn't include `tkinter`. This is often the case with some minimal installations and certain Linux distributions. You might need to install `tkinter` separately or use a different Python installation that includes `tkinter`.

2. You're using a virtual environment that doesn't have access to `tkinter`. If this is the case, you might need to recreate your virtual environment to include system packages, which should include `tkinter` if it's installed in your system's Python.

3. `tkinter` is installed, but Python is somehow not finding it. This could be due to a problem with your Python installation or a path issue.

Here's what you can do:

- If you're on Linux, you may need to install `tkinter` separately. On Ubuntu, you can use the command `sudo apt-get install python3-tk`.
  
- If you're using a virtual environment, you might need to recreate it to include system packages. If you're using `venv`, you can do this by using the `--system-site-packages` option when creating the virtual environment: `python3 -m venv --system-site-packages venv`.

- Check your Python installation. If you installed Python from the official website or via Anaconda, `tkinter` should be included. Try creating a new Python script with just `import tkinter as tk` to see if the problem is with your overall Python installation or just the specific script you're working on.

- If you're using an IDE, make sure it's configured to use the correct Python interpreter. Some IDEs have settings that determine which Python installation they use, and it's possible that the IDE is using a different installation that doesn't include `tkinter`. 

In general, `tkinter` should be available with a standard Python installation from python.org, so if you continue having issues, you may want to consider reinstalling Python.