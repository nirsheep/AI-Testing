import sys
import logging
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Set up basic logging
logging.basicConfig(filename='script.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

def organize_text(input_text):
    """
    Sends the input text to the OpenAI API to organize it into a structured format.
    """
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Organize the following pharmacy notes into a structured table format with sections, medications, and swap/note information."},
            {"role": "user", "content": input_text}
        ])
        organized_text = response.choices[0].message.content
        logging.info("Successfully organized text.")
        return organized_text
    except Exception as e:
        logging.error(f"Error organizing text: {e}")
        return None

def parse_and_output_table(organized_text, output_file_path):
    """
    Parses the organized text into sections and writes the output to a text file.
    """
    if not organized_text:
        logging.error("No organized text to parse.")
        return

    try:
        with open(output_file_path, 'w') as output_file:
            sections = organized_text.split("*****")[1:]  # Ignore the first empty element
            for section in sections:
                title, *items = section.strip().split("\n")
                output_file.write(f"Section: {title}\n")
                output_file.write(f"{'Medication':<30} | {'Swap/Note'}\n")
                output_file.write("-" * 60 + "\n")
                for item in items:
                    if item:
                        output_file.write(f"{item}\n")
                output_file.write("\n")
        logging.info(f"Successfully wrote organized text to {output_file_path}.")
    except Exception as e:
        logging.error(f"Error writing to file {output_file_path}: {e}")

def main(input_file_path, output_file_path):
    """
    The main function of the script. Reads the input file, organizes the text, and outputs to a new file.
    """
    try:
        with open(input_file_path, 'r') as file:
            input_text = file.read()
    except Exception as e:
        logging.error(f"Error reading file {input_file_path}: {e}")
        return

    organized_text = organize_text(input_text)
    parse_and_output_table(organized_text, output_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_path>")
        sys.exit(1)
    
    output_file_path = "TIA-T.txt"
    main(sys.argv[1], output_file_path)
