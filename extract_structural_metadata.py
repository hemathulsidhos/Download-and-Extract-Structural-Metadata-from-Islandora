import os
import csv
import xml.etree.ElementTree as ET

# rename FOLDERNAME to match your folder name 

# Specify the folder containing XML files
folder_path = 'C:/Users/hemat/Documents/Notepad++/FOLDERNAME'

# Define namespaces
namespaces = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'fedora': 'info:fedora/fedora-system:def/relations-external#',
    'fedora-model': 'info:fedora/fedora-system:def/model#',
    'islandora': 'http://islandora.ca/ontology/relsext#',
}

# Function to extract rdf:resource values for specific elements
def extract_rdf_resource_values(element):
    rdf_resource_values = {}
    for child in element:
        tag_namespace = child.tag.split('}')[-1]
        if tag_namespace == 'hasModel' or tag_namespace == 'isConstituentOf' or tag_namespace == 'isMemberOfCollection' or tag_namespace == 'isMemberOf':
            rdf_resource_values[child.tag] = child.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
    return rdf_resource_values

# Create a CSV file to write the results
# Create a CSV file to write the results
csv_file_path = os.path.join(folder_path, 'output_SM.csv')

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['File', 'rdf:about', 'fedora-model:hasModel', 'fedora:isMemberOfCollection', 'fedora:isConstituentOf', 'fedora:isMemberOf', 'islandora:isPageOf', 'islandora:isSequenceNumber', 'islandora:isPageNumber', 'islandora:isSection']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header to CSV file
    writer.writeheader()

    # Iterate over XML files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)

            # Parse the XML content
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Find rdf:Description element with the correct namespace
            rdf_description_element = root.find('.//rdf:Description', namespaces=namespaces)

            if rdf_description_element is not None:
                # Extract rdf:about value
                rdf_about_value = rdf_description_element.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')

                # Extract rdf:resource values for specific elements
                rdf_resource_values = extract_rdf_resource_values(rdf_description_element)

                # Extract additional values with error handling
                isPageOf_element = rdf_description_element.find('.//islandora:isPageOf', namespaces=namespaces)
                isPageOf_value = isPageOf_element.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', '') if isPageOf_element is not None else ''

                isSequenceNumber_element = rdf_description_element.find('.//islandora:isSequenceNumber', namespaces=namespaces)
                isSequenceNumber_value = isSequenceNumber_element.text if isSequenceNumber_element is not None else ''

                isPageNumber_element = rdf_description_element.find('.//islandora:isPageNumber', namespaces=namespaces)
                isPageNumber_value = isPageNumber_element.text if isPageNumber_element is not None else ''

                isSection_element = rdf_description_element.find('.//islandora:isSection', namespaces=namespaces)
                isSection_value = isSection_element.text if isSection_element is not None else ''

                # Write row to CSV file
                writer.writerow({
                    'File': filename,
                    'rdf:about': rdf_about_value,
                    'fedora-model:hasModel': rdf_resource_values.get('{info:fedora/fedora-system:def/model#}hasModel', ''),
                    'fedora:isMemberOfCollection': rdf_resource_values.get('{info:fedora/fedora-system:def/relations-external#}isMemberOfCollection', ''),
                    'fedora:isConstituentOf': rdf_resource_values.get('{info:fedora/fedora-system:def/relations-external#}isConstituentOf', ''),
                    'fedora:isMemberOf': rdf_resource_values.get('{info:fedora/fedora-system:def/relations-external#}isMemberOf', ''),
                    'islandora:isPageOf': isPageOf_value,
                    'islandora:isSequenceNumber': isSequenceNumber_value,
                    'islandora:isPageNumber': isPageNumber_value,
                    'islandora:isSection': isSection_value,
                })
