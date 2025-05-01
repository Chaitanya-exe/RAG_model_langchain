import ollama 
import os

model = "llama3.2"

input_file = "./data/list.txt"
output_file = "./data/sorted_items.txt"

if not os.path.exists(input_file):
    print(f"Input file {input_file} not found")
    exit(1)

with open(input_file, "r") as f:
    items = f.read().strip()

prompt = f"""
You are an assistant that categorizes a sorts list of grocery items.

Here is the list of grocery:
{items}

Please:
1. categorize items into appropriate categories such dairy, vegetables, meat etc.
2. Sort items in a alphabetically order
3. Present the categroized list in clear and organized manner.
"""

try:
    response = ollama.generate(model=model, prompt=prompt)
    generated_text: str = response.get("response", "")

    print("=========Categorized list===========\n")
    print(generated_text, end=" ", flush=True)

    with open(output_file, "w") as f:
        f.write(generated_text.strip())

    print(f"output has been saved to {output_file}")
    
except Exception as e:
    print(f"an error occured : {e}")
    exit(1)