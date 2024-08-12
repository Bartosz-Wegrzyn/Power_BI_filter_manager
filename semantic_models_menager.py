import os
import json

def list_semantic_models(base_directory):
    """
    List all semantic models in the base directory by checking for folders 
    containing 'definition.pbir' and return folder names (without '.Report') 
    along with the 'path' value from the definition.pbir file.
    
    Parameters:
    - base_directory: The base directory to search for folders containing 'definition.pbir'.
    
    Returns:
    - A list of tuples where each tuple contains the 'path' value and the folder name without '.Report'.
    """
    results = []

    # Walk through the base directory
    for root, dirs, files in os.walk(base_directory):
        # Check if 'definition.pbir' is in the current folder
        if "definition.pbir" in files:
            definition_path = os.path.join(root, "definition.pbir")
            # Read the definition.pbir file
            with open(definition_path, 'r', encoding='utf-8') as file:
                definition = json.load(file)
                # Get the value of 'path'
                path_value = definition.get("datasetReference", {}).get("byPath", {}).get("path", "Path not found")
                # Extract the folder name and remove '.Report'
                folder_name = os.path.basename(root)
                name_only = folder_name.replace(".Report", "")
                # Append the result to the list
                results.append((path_value, name_only))
    
    return results

# Define the base directory (one folder up from the current working directory)
base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))








from collections import defaultdict

def format_semantic_models(semantic_models):
    """
    Format semantic models by grouping them based on their 'path' value.
    
    Parameters:
    - semantic_models: A list of tuples where each tuple contains the 'path' value 
      and the folder name without '.Report'.
    
    Returns:
    - A formatted string where each path is followed by its associated folder names,
      grouped by the path value.
    """
    grouped_models = defaultdict(list)
    
    # Group the semantic models by their path value
    for path, name in semantic_models:
        grouped_models[path].append(name)
    
    # Build the formatted output string
    formatted_output = []
    for path, names in grouped_models.items():
        formatted_output.append(path)
        for name in names:
            formatted_output.append(f"    {name}")
        formatted_output.append("")  # Add a blank line after each group
    
    return "\n".join(formatted_output)

semantic_models = list_semantic_models(base_directory)
# print(semantic_models)


print(format_semantic_models(semantic_models))
