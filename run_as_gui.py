import tkinter as tk
from tkinter import messagebox
import pandas as pd
import yaml
import layman_summaries

def generate_summaries():
    # Load the config.yaml file
    config = layman_summaries.load_config()

    # Get the variables from the config.yaml file
    config['aimodel'] = aimodel_var.get()
    config['max_tokens'] = int(max_tokens_var.get())
    config['data_url'] = data_url_var.get()

    # Call the main function in layman_summaries.py and get the DataFrame
    df = layman_summaries.main(config)

    # Print the DataFrame in the GUI
    text.delete(1.0, tk.END)
    text.insert(tk.END, df)

root = tk.Tk()

aimodel_var = tk.StringVar()
max_tokens_var = tk.StringVar()
data_url_var = tk.StringVar()

# Create the GUI elements
aimodel_label = tk.Label(root, text="AI Model:")
aimodel_entry = tk.Entry(root, textvariable=aimodel_var)

max_tokens_label = tk.Label(root, text="Max Tokens:")
max_tokens_entry = tk.Entry(root, textvariable=max_tokens_var)

data_url_label = tk.Label(root, text="Data URL:")
data_url_entry = tk.Entry(root, textvariable=data_url_var)

generate_button = tk.Button(root, text="Generate Summaries", command=generate_summaries)

text = tk.Text(root)

# Pack the GUI elements
aimodel_label.pack()
aimodel_entry.pack()
max_tokens_label.pack()
max_tokens_entry.pack()
data_url_label.pack()
data_url_entry.pack()
generate_button.pack()
text.pack()

# Load the default values from the config.yaml file
config = layman_summaries.load_config()
aimodel_var.set(config['aimodel'])
max_tokens_var.set(config['max_tokens'])
data_url_var.set(config['data_url'])

root.mainloop()
