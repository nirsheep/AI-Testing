import sys
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

def organize_text(input_text):
    """
    Sends the input text to the OpenAI API to organize it into a structured format.
    
    :param input_text: The raw text input containing pharmacy notes.
    :return: The organized text returned by the OpenAI API.
    """
    # Use the OpenAI API to process the input text, instructing it to organize the text
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Organize the following pharmacy notes into a structured table format with sections, medications, and swap/note information."},
        {"role": "user", "content": input_text}
    ])
    # Return the organized text from the API's response
    return response.choices[0].message.content

def parse_and_output_table(organized_text, output_file_path):
    """
    Parses the organized text into sections and writes the output to a text file.
    
    :param organized_text: The text organized into sections by the OpenAI API.
    :param output_file_path: The path to the output text file.
    """
    # Open or create the output file for writing
    with open(output_file_path, 'w') as output_file:
        # Split the organized text into sections based on the "*****" delimiter
        sections = organized_text.split("*****")[1:]  # Ignore the first empty element
        for section in sections:
            # Split each section into a title and items
            title, *items = section.strip().split("\n")
            # Write the section title and table headers to the output file
            output_file.write(f"Section: {title}\n")
            output_file.write(f"{'Medication':<30} | {'Swap/Note'}\n")
            output_file.write("-" * 60 + "\n")
            # Write each item (medication and swap/note information) to the output file
            for item in items:
                if item:  # Ensure the item is not empty
                    output_file.write(f"{item}\n")
            output_file.write("\n")  # Add an empty line for readability between sections

def main(input_file_path, output_file_path):
    """
    The main function of the script. Reads the input file, organizes the text, and outputs to a new file.
    
    :param input_file_path: The path to the input text file containing pharmacy notes.
    :param output_file_path: The path to the output text file where the table will be written.
    """
    try:
        # Read the input text file
        with open(input_file_path, 'r') as file:
            input_text = file.read()
        
        # Organize the text using the OpenAI API
        organized_text = organize_text(input_text)
        
        # Parse the organized text and write the output to a file
        parse_and_output_table(organized_text, output_file_path)
    except Exception as e:
        # Print any errors encountered during execution
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check if the script was called with the correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_path>")
    else:
        # Define the output file path and call the main function with the provided input file path
        output_file_path = "TIA-T.txt"
        main(sys.argv[1], output_file_path)
