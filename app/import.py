import h5py
import json
import base64
import numpy as np

def convert_group_to_dict(group):
    """Recursively convert a HDF5 `Group` object to a dictionary."""
    result = {}

    for name, obj in group.items():
        if isinstance(obj, h5py.Group):
            result[name] = convert_group_to_dict(obj)
        else:
            result[name] = obj

    return result

def convert_dataset_to_list(dataset):
    """Convert a HDF5 `Dataset` object to a list of arrays."""
    data = dataset[:]
    return list(data)

def convert_dataset_bytes_to_json(dataset):
    """Convert a HDF5 `Dataset` object containing bytes to a JSON string."""
    data = dataset[:]
    encoded_data = base64.b64encode(data)
    base64_str = f'data:application/octet-stream;base64,{encoded_data.decode("utf-8")}'
    return base64_str

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        """Custom JSON encoder to handle bytes objects."""
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return super().default(obj)

def convert_h5_to_json(h5file_path, json_file_path):
    """Convert a HDF5 file to a JSON file."""
    with h5py.File(h5file_path, 'r') as f:
        data = f['data']

        json_data = {}

        # Convert group attributes to a dictionary
        group_attributes = {}
        for attr_name, attr_value in data.attrs.items():
            if isinstance(attr_value, np.ndarray):
                attr_value = attr_value.tolist()
            group_attributes[attr_name] = attr_value

        json_data['attributes'] = group_attributes

        # Convert datasets to JSON-compatible format
        for name, obj in data.items():
            if isinstance(obj, h5py.Dataset) and obj.dtype.char == 'b':
                json_data[name] = convert_dataset_bytes_to_json(obj)
            else:
                json_data[name] = convert_dataset_to_list(obj)

        # Write JSON data to file
        with open(json_file_path, 'w') as f:
            json.dump(json_data, f, cls=CustomEncoder)

h5file_path = "/Users/t.lukacs/Downloads/dataset/1df7eacb-e083-45c3-baf1-d941440ce60d.h5"
json_file_path = '/Users/t.lukacs/Downloads/data2.json'

convert_h5_to_json(h5file_path, json_file_path)
