# Python Report Filter Processing

This script processes JSON files related to report filters based on certain criteria. It performs filtering, updating, appending, deleting, and counting operations on `report.json` files found in directories based on a dataset reference path.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Functions](#functions)
  - [filter_files_based_on_definition](#filter_files_based_on_definition)
  - [read_json_file](#read_json_file)
  - [write_json_file](#write_json_file)
  - [read_filters_from_file](#read_filters_from_file)
  - [update_report_json_files](#update_report_json_files)
  - [append_report_json_files](#append_report_json_files)
  - [delete_inactive_filters](#delete_inactive_filters)
  - [count_report_json_files](#count_report_json_files)
  - [count_active_report_json_files](#count_active_report_json_files)
  - [count_inactive_report_json_files](#count_inactive_report_json_files)
  - [process_filters](#process_filters)
- [Configuration](#configuration)
- [Example Usage](#example-usage)
- [Error Handling](#error-handling)

## Prerequisites

- Python 3.x
- JSON files (`definition.pbir`, `report.json`, `filters.json`)

## Usage

1. **Setup**: Define the `SemanticModel` path and the starting directory for the search.
2. **Functions**: Use the provided functions to manage report filters as needed.
3. **Example Usage**: Uncomment the example usage section in the script to perform operations like updating, deleting, appending filters, and counting them.

## Functions

### `filter_files_based_on_definition(starting_directory)`

Filters the `report.json` files based on the dataset reference path in `definition.pbir` files found in the specified starting directory.

**Parameters:**
- `starting_directory` (str): The root directory to start the search.

**Returns:**
- List of file paths to `report.json` files that match the dataset reference.

### `read_json_file(filepath, encoding='utf-8')`

Reads and returns the content of a JSON file.

**Parameters:**
- `filepath` (str): The path to the JSON file.
- `encoding` (str): The encoding of the file (default is 'utf-8').

**Returns:**
- Dictionary containing the JSON content.

### `write_json_file(filepath, data, encoding='utf-8')`

Writes JSON data to a file with indentation.

**Parameters:**
- `filepath` (str): The path to the JSON file.
- `data` (dict): The data to write to the file.
- `encoding` (str): The encoding of the file (default is 'utf-8').

### `read_filters_from_file(filters_file)`

Reads and returns the content of the filters JSON file.

**Parameters:**
- `filters_file` (str): The path to the filters JSON file.

**Returns:**
- List of filters.

### `update_report_json_files(filtered_files, new_value)`

Updates the `filters` field in each `report.json` file with the provided `new_value`.

**Parameters:**
- `filtered_files` (list of str): List of paths to `report.json` files.
- `new_value` (list of dict): New filters to set.

### `append_report_json_files(filtered_files, new_filters)`

Appends new filters to existing filters in each `report.json` file without duplication.

**Parameters:**
- `filtered_files` (list of str): List of paths to `report.json` files.
- `new_filters` (list of dict): Filters to append.

### `delete_inactive_filters(filtered_files)`

Removes inactive filters (those without a `"filter"` key) from each `report.json` file.

**Parameters:**
- `filtered_files` (list of str): List of paths to `report.json` files.

### `count_report_json_files(filtered_files)`

Counts and prints the number of filters in each `report.json` file.

**Parameters:**
- `filtered_files` (list of str): List of paths to `report.json` files.

### `count_active_report_json_files(filtered_files)`

Counts and prints the number of active filters (those with the `"filter"` key) in each `report.json` file.

**Parameters:**
- `filtered_files` (list of str): List of paths to `report.json` files.

### `count_inactive_report_json_files(filtered_files)`

Counts and prints the number of inactive filters (those without the `"filter"` key) in each `report.json` file.

**Parameters:**
- `filtered_files` (list of str): List of paths to `report.json` files.

### `process_filters(json_file_name, output_file_name, save_to_file=False)`

Processes a JSON file containing filter mappings, aggregates the data by entity, and formats it with aligned columns. Optionally, saves the formatted data to a file.

**Parameters:**
- `json_file_name` (str): The name of the input JSON file.
- `output_file_name` (str): The name of the output text file.
- `save_to_file` (bool): Flag indicating whether to save the output to a file (default is `False`).

## Configuration

- **SemanticModel**: Path to the dataset reference used for filtering.
- **starting_directory**: Directory to start searching for `definition.pbir` and `report.json` files.
- **filters_file**: Path to the filters JSON file.

## Example Usage

```python
# Define the starting directory (one folder up from the current working directory)
starting_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filters_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "filters.json")

# Find the filtered files
filtered_files = filter_files_based_on_definition(starting_directory)

# Read new filters from filters.json
new_filters = read_filters_from_file(filters_file)

# Example Usage
update_report_json_files(filtered_files, new_filters)  # Update the filters
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
```

## Error Handling

- **File Read/Write Errors**: Handled using try-except blocks for file I/O operations.
- **JSON Decoding Errors**: Ensures that errors during JSON parsing are caught and reported.
