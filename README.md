# ShapeNet Rendering Toolkit

Welcome to the ShapeNet Preprocessing and Rendering Toolkit! This repository contains a suite of Python scripts designed to enhance the usability of the ShapeNet dataset. Our tools make it easy to adjust texture references within OBJ files and render multiple views of each model using Blender, making this toolkit ideal for researchers and developers working in computer vision, machine learning, and 3D graphics.

## Features

- **Texture Adjustment**: Automatically update OBJ files with correct texture references using `adjust_shapenet_textures.py`.
- **Automated Rendering**: Render multiple views of 3D models programmatically with `render_dataset.py`, leveraging Blender's powerful rendering capabilities.

## Getting Started

### Prerequisites
Tested with the following versions:
- Blender 4.2
- Python 3.11.5

Ensure Blender and bpy is installed on your system and accessible from the command line.

### Installation

Clone this repository to your local machine using:

```sh
git clone https://github.com/mortorit/ShapeNetRenderer.git
cd ShapeNetRenderer
```

### Build the Blender Environment

To use the Blender Python API, you must build the Blender environment. This can be done by running the following command:

```sh
docker build -t blender .
```

### Adjusting Textures

Before rendering, ensure each OBJ file in your dataset references its textures correctly. Run the adjust_shapenet_textures.py script as follows:

```sh
python adjust_shapenet_textures.py --dataset_directory /path/to/shapenet
```

Replace /path/to/shapenet with the path to your ShapeNet dataset.

### Rendering Dataset

To render the dataset, use the render_dataset.py script. This requires specifying the input dataset path, output path for renders, and the number of views:

```sh
python render_dataset.py --dataset_directory /path/to/shapenet --output_directory /path/to/output --blender_path /path/to/blender
```

## Contributing

Contributions to the ShapeNet Preprocessing and Rendering Toolkit are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Thanks to the ShapeNet team for providing an invaluable resource to the community.
This toolkit is not officially associated with the ShapeNet project.