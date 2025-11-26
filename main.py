import argparse
import json
import os
import xml.etree.ElementTree as ET


def convert_xml_to_json(xml_file, mapping, json_file):
    """
    Converts an XML file to a JSON file based on a conversion mapping.

    Args:
        xml_file (str): Path to the input XML file.
        mapping (str): Path to the conversion mapping file (JSON).
        json_file (str): Path to the output JSON file.
    """
    try:
        if not os.path.exists(xml_file):
            print("\033[91m", f"Error: XML file not found at '{xml_file}'", "\033[91m")
            exit(1)
        if not os.path.exists(mapping):
            print("\033[91m", f"Error: Conversion mapping file not found at '{mapping}'", "\033[91m")
            exit(2)

        tree = ET.parse(xml_file)
        root = tree.getroot()

        with open(mapping, 'r') as f:
            conversion_map = json.load(f)

        output_data = {}
        for json_path, xml_path in conversion_map.items():
            element = root.find(xml_path)
            keys = json_path.split('.')
            d = output_data
            for key in keys[:-1]:
                d = d.setdefault(key, {})
            if element is not None:
                d[keys[-1]] = element.text.replace('&', '')
            else:
                d[keys[-1]] = ""
                if xml_path:
                    print("\033[93m", f"Warning: XML path not found: {xml_path}", "\033[93m")

        with open(json_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        print("\033[92m", f"Successfully converted {xml_file} to {json_file}", "\033[92m")

    except FileNotFoundError as e:
        print("\033[91m", f"Error: {e}", "\033[91m")
    except ET.ParseError as e:
        print("\033[91m", f"Error parsing XML file: {e}", "\033[91m")
    except json.JSONDecodeError as e:
        print("\033[91m", f"Error parsing conversion file: {e}", "\033[91m")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml', type=str, help='Path to the XML file')
    parser.add_argument('--mapping', '--m', type=str, help='Path to the mapping file')
    parser.add_argument('--json', type=str, help='Path for the output JSON file')
    args = parser.parse_args()
    xml_input = args.xml
    mapping_input = args.mapping
    json_output = args.json
    if json_output is None:
        json_output = "output.json"

    convert_xml_to_json(xml_input, mapping_input, json_output)
