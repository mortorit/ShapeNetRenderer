import os
import argparse


def prepend_usemtl_to_obj(dataset_dir):
    # Walk through the dataset directory
    for root, dirs, files in os.walk(dataset_dir):
        if 'images' in dirs:
            # Construct the path to the images directory
            images_dir = os.path.join(root, 'images')
            # Construct the path to the model_normalized.obj file
            obj_file_path = os.path.join(root, 'models', 'model_normalized.obj')

            if os.path.exists(obj_file_path):
                # Store the lines to be added
                lines_to_prepend = []
                # Iterate through each file in the images directory
                for image_file in os.listdir(images_dir):
                    line = f'usemtl ../images/{image_file}\n'
                    lines_to_prepend.append(line)

                # Read the existing content of the obj file
                with open(obj_file_path, 'r') as obj_file:
                    obj_content = obj_file.readlines()

                # Prepend the new lines to the obj file content
                updated_content = lines_to_prepend + obj_content

                # Write the updated content back to the obj file
                with open(obj_file_path, 'w') as obj_file:
                    obj_file.writelines(updated_content)
                print(f'Updated {obj_file_path} with {len(lines_to_prepend)} "usemtl" lines.')


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description='Prepend OBJ files with usemtl lines for each texture in the images directory.')
    parser.add_argument('--dataset_directory', type=str, help='Path to the dataset directory.')

    # Parse arguments
    args = parser.parse_args()

    # Call the function with the provided dataset directory
    prepend_usemtl_to_obj(args.dataset_directory)

    print('Finished updating OBJ files.')