import collections.abc


def _generate_instructions_recursive(data, path, instructions):
    """
    Recursive helper function to traverse the data structure and generate form-filling instructions.
    Designed to be generic and independent of specific form data structures.
    """
    # Base Case: Leaf node (scalar value or string)
    if not isinstance(
        data, (collections.abc.Mapping, collections.abc.Sequence)
    ) or isinstance(data, str):
        if not path:
            return

        # Extract the last key for the field name
        field_name = str(path[-1])
        # Create a display name by replacing underscores and title-casing
        field_name_display = field_name.replace("_", " ").title()
        # Convert the value to a string
        value_str = str(data)

        # Build the location string from the path (excluding the last element)
        location_parts = path[:-1]
        if location_parts:
            # Clean up path parts for readability
            readable_parts = []
            for part in location_parts:
                # If the part looks like an index (e.g., "Item 0"), make it more readable
                if part.startswith("Item "):
                    try:
                        index = (
                            int(part.split(" ")[1]) + 1
                        )  # Convert to 1-based indexing
                        readable_parts.append(f"Entry {index}")
                    except (IndexError, ValueError):
                        readable_parts.append(part)
                else:
                    readable_parts.append(part.replace("_", " ").title())

        # Generate the instruction
        instruction = f'Enter "{value_str}" into the field "{field_name_display}"'
        # instruction = f'Locate the field "{field_name_display}"{location_str} and fill in the value "{value_str}"'
        instructions.append(instruction)
        return

    # Recursive Step: Dictionary
    if isinstance(data, collections.abc.Mapping):
        for key, value in data.items():
            _generate_instructions_recursive(value, path + [str(key)], instructions)

    # Recursive Step: List/Tuple (but not string)
    elif isinstance(data, collections.abc.Sequence) and not isinstance(data, str):
        for index, item in enumerate(data):
            # Use a generic identifier for list items
            list_item_identifier = f"Item {index}"
            _generate_instructions_recursive(
                item, path + [list_item_identifier], instructions
            )


def get_form_instructions(form_data: dict) -> list[str]:
    """
    Generate form filling instructions for an LLM agent from JSON structured form data.
    """
    if not isinstance(form_data, collections.abc.Mapping):
        raise TypeError("Input form_data must be a dictionary.")
    all_instructions = []
    for key, value in form_data.items():
        _generate_instructions_recursive(value, [str(key)], all_instructions)
    return all_instructions


# --- Main execution block with added second entry for testing ---
if __name__ == "__main__":
    from data import MOCK_DATA

    # Need to add 'collections' import
    import collections.abc

    instructions = get_form_instructions(MOCK_DATA)
    for instruction in instructions:
        print(instruction)
