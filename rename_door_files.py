import os
import shutil


def rename_files(directory_path):
    # List all files in the directory
    for filename in os.listdir(directory_path):
        # Construct the full file path
        old_file_path = os.path.join(directory_path, filename)
        
        # Check if it's a file and not a directory
        if os.path.isfile(old_file_path):
            # Split the filename from its extension
            name_part, extension = os.path.splitext(filename)
            
            # Find the first dot where the hash starts
            dot_index = name_part.find('.')
            
            # If a dot was found, and it is not the first character
            if dot_index > 0:
                # Remove the hash part
                new_name = name_part[:dot_index]
            else:
                # No dot found, use the name as is
                new_name = name_part
            
            # Append the extension back if it exists
            new_file_path = os.path.join(directory_path, new_name + extension)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{filename}' to '{new_name + extension}'")



def organize_files(directory_path):
    # Create paths for the destination folders
    door_path = os.path.join(directory_path, 'door')
    frame_path = os.path.join(directory_path, 'Frame')
    combined_path = os.path.join(directory_path, 'combined')
    others_path = os.path.join(directory_path, 'others')

    # Ensure the folders exist, or create them
    os.makedirs(door_path, exist_ok=True)
    os.makedirs(frame_path, exist_ok=True)
    os.makedirs(combined_path, exist_ok=True)
    os.makedirs(others_path, exist_ok=True)

    # List all files in the directory
    for filename in os.listdir(directory_path):
        # Construct the full file path
        file_path = os.path.join(directory_path, filename)

        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            # Get the file extension
            _, ext = os.path.splitext(filename)

            # Check if the file is a PNG file
            if ext.lower() != '.png':
                # If not a PNG, remove the file
                os.remove(file_path)
                print(f"Removed non-PNG file '{filename}'")
                continue

            # Decide the destination based on the prefix
            if 'door' in filename and 'Frame' in filename:
                dest_folder = combined_path

            elif filename.startswith('door'):
                dest_folder = door_path
            elif filename.startswith('Frame'):
                dest_folder = frame_path

            else:
                dest_folder = others_path
            
            # Move the file to the appropriate folder
            shutil.move(file_path, os.path.join(dest_folder, filename))
            print(f"Moved '{filename}' to '{dest_folder}'")



def organize_by_color(base_directory):
    # List all subdirectories in the base directory
        files = os.listdir(base_directory)

        # Process each file in the subdirectory
        for file in files:
            file_path = os.path.join(base_directory, file)
            
            # Check if it is a file and not a directory
            if os.path.isfile(file_path):
                # Assuming the color is after the last hyphen before the extension
                name_part, extension = os.path.splitext(file)
                parts = name_part.split('-')
                
                if len(parts) > 1:
                    color = parts[-1]  # Color is the last part after the last hyphen
                    color_directory = os.path.join(base_directory, color)
                    
                    # Ensure the color directory exists
                    os.makedirs(color_directory, exist_ok=True)
                    
                    # Move the file to the color directory
                    new_file_path = os.path.join(color_directory, file)
                    shutil.move(file_path, new_file_path)
                    print(f"Moved '{file}' to '{color_directory}'")
                else:
                    print(f"No color found in filename '{file}'")




# Example usage:
directory_path = 'C:\\Users\\kunga\\anywheredoorcollectionnew-main (1)\\anywheredoorcollectionnew-main\\static\\img'
# rename_files(directory_path)
# organize_files(directory_path)


organize_by_color(directory_path + "\\Frame")