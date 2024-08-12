import os
import json

# Define the SemanticModel path
SemanticModel = "../{Semantic Mocel Name}.Dataset"

def filter_files_based_on_definition(starting_directory):
    """
    Filter files based on the dataset reference path in the definition.pbir file.
    """
    filtered_files = []
    for root, _, files in os.walk(starting_directory):
        if "definition.pbir" in files and "report.json" in files:
            definition_path = os.path.join(root, "definition.pbir")
            try:
                # Load the definition.pbir file
                with open(definition_path, 'r', encoding='utf-8') as file:
                    definition = json.load(file)
                    # Check if the path matches the SemanticModel
                    if definition["datasetReference"]["byPath"]["path"] == SemanticModel:
                        filtered_files.append(os.path.join(root, "report.json"))
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading {definition_path}: {e}")
    return filtered_files

def read_json_file(filepath, encoding='utf-8'):
    """
    Read and return the content of a JSON file.
    """
    try:
        # Read and parse JSON file content
        with open(filepath, 'r', encoding=encoding) as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading {filepath}: {e}")
        return {}

def write_json_file(filepath, data, encoding='utf-8'):
    """
    Write JSON data to a file with indentation.
    """
    try:
        # Write JSON data to the specified file
        with open(filepath, 'w', encoding=encoding) as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error writing {filepath}: {e}")

def read_filters_from_file(filters_file):
    """
    Read and return the content of the filters JSON file.
    """
    return read_json_file(filters_file)

def update_report_json_files(filtered_files, new_value):
    """
    Update the filters field in each report.json file with new_value.
    """
    for file_path in filtered_files:
        report_data = read_json_file(file_path)
        # Set new filters value
        report_data["filters"] = json.dumps(new_value)
        write_json_file(file_path, report_data)

def append_report_json_files(filtered_files, new_filters):
    """
    Append new filters to existing filters in each report.json file without duplication.
    """
    for file_path in filtered_files:
        report_data = read_json_file(file_path)
        existing_filters = json.loads(report_data.get("filters", "[]"))

        # Convert existing filters to a set for quick lookup
        existing_filters_set = set(json.dumps(f) for f in existing_filters)
        # Add new filters if they are not already present
        for new_filter in new_filters:
            if json.dumps(new_filter) not in existing_filters_set:
                existing_filters.append(new_filter)

        report_data["filters"] = json.dumps(existing_filters)
        write_json_file(file_path, report_data)

def delete_inactive_filters(filtered_files):
    """
    Remove inactive filters (those without a "filter" key) from each report.json file.
    """
    for file_path in filtered_files:
        report_data = read_json_file(file_path)
        existing_filters = json.loads(report_data.get("filters", "[]"))

        # Keep only active filters (those with the "filter" key)
        active_filters = [f for f in existing_filters if "filter" in f]
        report_data["filters"] = json.dumps(active_filters)
        write_json_file(file_path, report_data)

def count_report_json_files(filtered_files):
    """
    Count and print the number of filters in each report.json file.
    """
    for file_path in filtered_files:
        report_data = read_json_file(file_path)
        filters_count = len(json.loads(report_data.get("filters", "[]")))
        print(f"{os.path.dirname(file_path)}: {filters_count}")

def count_active_report_json_files(filtered_files):
    """
    Count and print the number of active filters (those with the "filter" key) in each report.json file.
    """
    for file_path in filtered_files:
        report_data = read_json_file(file_path)
        existing_filters = json.loads(report_data.get("filters", "[]"))
        active_filters_count = sum(1 for f in existing_filters if "filter" in f)
        print(f"{os.path.dirname(file_path)}: {active_filters_count}")

def count_inactive_report_json_files(filtered_files):
    """
    Count and print the number of inactive filters (those without the "filter" key) in each report.json file.
    """
    for file_path in filtered_files:
        report_data = read_json_file(file_path)
        existing_filters = json.loads(report_data.get("filters", "[]"))
        inactive_filters_count = sum(1 for f in existing_filters if "filter" not in f)
        print(f"{os.path.dirname(file_path)}: {inactive_filters_count}")

def process_filters(json_file_name, output_file_name, save_to_file=False):
    """
    Processes a JSON file containing filter mappings, aggregates the data by entity,
    formats it with aligned columns, and either prints the result to the console or saves it to a file.
    """
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to the JSON file
    json_file_path = os.path.join(current_dir, json_file_name)
    
    # Read the JSON file
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading {json_file_path}: {e}")
        return
    
    # Dictionary to hold the aggregated data
    aggregated_data = {}
    
    # Aggregate elements by Entity, Property, and displayName
    for item in data:
        if 'Column' in item['expression']:
            entity = item['expression']['Column']['Expression']['SourceRef']['Entity']
            property_value = item['expression']['Column']['Property']
        elif 'HierarchyLevel' in item['expression']:
            entity = item['expression']['HierarchyLevel']['Expression']['Hierarchy']['Expression']['SourceRef']['Entity']
            property_value = item['expression']['HierarchyLevel']['Level']
        else:
            continue
        
        display_name = item['displayName']
        if entity not in aggregated_data:
            aggregated_data[entity] = {}
        aggregated_data[entity][property_value] = display_name
    
    # Function to format and print mappings with aligned columns
    def format_mappings(mappings):
        output_lines = []
        for entity, properties in mappings.items():
            output_lines.append(entity)  # Add the entity as a header
            max_key_length = 60 # max(len(key) for key in properties.keys())  # Find the max key length
            for key, value in properties.items():
                # Format each property with aligned columns
                output_lines.append(f"    {key.ljust(max_key_length)}: {value}")
            output_lines.append("")  # Add a blank line after each category
        return '\n'.join(output_lines)
    
    formatted_output = format_mappings(aggregated_data)
    print(formatted_output)
    
    # Save the formatted data to a text file if save_to_file is True
    if save_to_file:
        output_file_path = os.path.join(current_dir, output_file_name)
        try:
            with open(output_file_path, 'w') as file:
                file.write(formatted_output)
            print(f"Formatted aggregated data saved to {output_file_name}")
        except IOError as e:
            print(f"Error writing {output_file_path}: {e}")

# Define the starting directory (one folder up from the current working directory)
starting_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filters_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "filters.json")

# Find the filtered files
filtered_files = filter_files_based_on_definition(starting_directory)

# Read new filters from filters.json
new_filters = read_filters_from_file(filters_file)

# Example Usage
print("All:")
count_report_json_files(filtered_files)  # Count and print the number of filters in each report.json file
print()
print("Active:")
count_active_report_json_files(filtered_files)  # Count and print the number of active filters in each report.json file
print()
print("Inactive:")
count_inactive_report_json_files(filtered_files)  # Count and print the number of inactive filters in each report.json file
print()




delete_inactive_filters(filtered_files)  # Delete inactive filters
append_report_json_files(filtered_files, new_filters)  # Append new filters without duplication

print("All:")
count_report_json_files(filtered_files)  # Count and print the number of filters in each report.json file
print()
print("Active:")
count_active_report_json_files(filtered_files)  # Count and print the number of active filters in each report.json file
print()
print("Inactive:")
count_inactive_report_json_files(filtered_files)  # Count and print the number of inactive filters in each report.json file

process_filters("filters.json", "aggregated_filters.txt", save_to_file=False)
