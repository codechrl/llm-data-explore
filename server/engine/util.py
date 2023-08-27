def save_to_file(responses, output_file):
    with open(output_file, "w") as file:
        for response in responses:
            file.write(response + "\n")
