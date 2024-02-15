import sys
from openai import OpenAI

client = OpenAI()

def organize_text(input_text):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Organize the following pharmacy notes into a structured table format with sections, medications, and swap/note information."},
        {"role": "user", "content": input_text}
    ])
    return response.choices[0].message.content


def parse_and_output_table(organized_text):
    sections = organized_text.split("*****")[1:]  # Split and remove the first empty element
    for section in sections:
        title, *items = section.strip().split("\n")
        print(f"Section: {title}")
        print(f"{'Medication':<30} | {'Swap/Note'}")
        print("-" * 60)
        for item in items:
            if item:
                print(f"{item}")
        print("\n")

def main(input_file_path):
    try:
        with open(input_file_path, 'r') as file:
            input_text = file.read()
        
        # Assuming you have a function to properly instruct GPT to organize the text
        organized_text = organize_text(input_text)
        
        parse_and_output_table(organized_text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_path>")
    else:
        main(sys.argv[1])
