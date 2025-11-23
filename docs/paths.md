# Python pathlib
You can use pathlib for joining and splitting paths with its object-oriented API. Here's how:

## Joining Paths
Use the / operator to join paths:

from pathlib import Path

```
base_path = Path("/c:/Users/LENOVO/OneDrive/Escritorio/diegogo/cautec")
new_path = base_path / "subfolder" / "file.txt"
print(new_path)  # Output: /c:/Users/LENOVO/OneDrive/Escritorio/diegogo/cautec/subfolder/file.txt
```

## Splitting Paths
You can split a path into its components using the .parts attribute or access specific parts like .parent and .name:

```
path = Path("/c:/Users/LENOVO/OneDrive/Escritorio/diegogo/cautec/subfolder/file.txt")

# Get all parts of the path
print(path.parts)  # Output: ('/', 'c:', 'Users', 'LENOVO', 'OneDrive', 'Escritorio', 'diegogo', 'cautec', 'subfolder', 'file.txt')

# Get the parent directory
print(path.parent)  # Output: /c:/Users/LENOVO/OneDrive/Escritorio/diegogo/cautec/subfolder

# Get the file name
print(path.name)  # Output: file.txt

# Get the file stem (name without extension)
print(path.stem)  # Output: file

# Get the file extension
print(path.suffix)  # Output: .txt
```

pathlib makes these operations simple and intuitive without needing to use multiple functions like os.path.join or os.path.split.

# In Flask

## Get flask app instance / blueprint path

`instance.root_path`

# __file__

Get the executing python file path

`__file__`