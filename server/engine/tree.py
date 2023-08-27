import os
from urllib.parse import quote

from setting import setting


def generate_folder_tree(path, output_file):
    def generate_directory_structure(current_path, indent=""):
        result = ""
        items = sorted(os.listdir(current_path))

        for idx, item in enumerate(items):
            item_path = os.path.join(current_path, item)
            is_last_item = idx == len(items) - 1

            if os.path.isdir(item_path):
                result += indent + "├── " + item + "\n"
                if is_last_item:
                    new_indent = indent + "    "
                else:
                    new_indent = indent + "│   "
                result += generate_directory_structure(item_path, new_indent)
            else:
                if is_last_item:
                    result += indent + "└── " + item + "\n"
                else:
                    result += indent + "├── " + item + "\n"

        return result

    directory_structure = generate_directory_structure(path)
    # with open(f"data/tree/{output_file}.md", "w") as f:
    #     f.write(directory_structure)

    return f"""```
        {directory_structure}
        ```"""


def generate_folder_tree_link_p(path, output_file, title):
    def generate_directory_structure(current_path, indent=0):
        result = ""
        items = os.listdir(current_path)

        for item in items:
            item_path = os.path.join(current_path, item)
            link = f"{setting.PUBLIC_HOSTNAME}?chat=true&type=repository&title={title}&question=explain {item_path}"
            link = quote(link)
            if os.path.isdir(item_path):
                result += "  " * indent + "- " + f"[{item}]({link})" + "\n"
                result += generate_directory_structure(item_path, indent + 1)
            else:
                result += "  " * indent + "- " + f"[{item}]({link})" + "\n"

        return result

    directory_structure = generate_directory_structure(path)
    # with open(f"data/tree/{output_file}.md", "w") as f:
    #     f.write(directory_structure)

    return f"""
        {directory_structure}
        """


def generate_folder_tree_link(path, output_file, title):
    def generate_directory_structure(current_path, indent=0):
        result = ""
        items = os.listdir(current_path)

        for item in items:
            item_path = os.path.join(current_path, item)
            link_params = {
                "chat": "true",
                "type": "repository",
                "title": title,
                "question": f"show & explain {item_path}",
            }
            encoded_params = "&".join(
                [f"{key}={quote(value)}" for key, value in link_params.items()]
            )
            link = f"{setting.PUBLIC_HOSTNAME}?{encoded_params}"
            if os.path.isdir(item_path):
                result += "  " * indent + "- " + f"[{item}]({link})" + "\n"
                result += generate_directory_structure(item_path, indent + 1)
            else:
                result += "  " * indent + "- " + f"[{item}]({link})" + "\n"

        return result

    directory_structure = generate_directory_structure(path)
    return f"""
{directory_structure}
"""
