import base64
import re
import plistlib
import sys

def convert_uids(obj):
    """
    Recursively convert plistlib.UID objects to a representable format.
    """
    if isinstance(obj, plistlib.UID):
        # Convert UID objects to a string representation
        return f"UID:{obj.data}"
    elif isinstance(obj, dict):
        return {k: convert_uids(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_uids(x) for x in obj]
    return obj

def decode_and_convert_base64_in_xml(file_path):
    with open(file_path, 'r') as file:
        xml_content = file.read()

    base64_strings = re.findall(r'<data>\s*(.*?)\s*</data>', xml_content, re.DOTALL)

    for b64_string in base64_strings:
        decoded_data = base64.b64decode(b64_string)

        try:
            plist_data = plistlib.loads(decoded_data)
            # Convert UIDs and other objects in the plist
            converted_plist = convert_uids(plist_data)
            xml_plist = plistlib.dumps(converted_plist, fmt=plistlib.FMT_XML).decode('utf-8')
            print("Converted Data:", xml_plist)
        except Exception as e:
            print("Error converting data:", e)

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    decode_and_convert_base64_in_xml(file_name)
else:
    print("No file specified. Please provide the file name as an argument.")

