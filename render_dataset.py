import argparse
import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from render_rgb import main

def process_dataset(input_dataset_path, output_path, views):
    for category_name in os.listdir(input_dataset_path):
        category_path = os.path.join(input_dataset_path, category_name)
        if os.path.isdir(category_path):
            for sample_name in os.listdir(category_path):
                sample_path = os.path.join(category_path, sample_name)
                model_path = os.path.join(sample_path, "models", "model_normalized.obj")
                if os.path.exists(model_path):
                    output_sample_path = os.path.join(output_path, category_name, sample_name)
                    os.makedirs(output_sample_path, exist_ok=True)
                    print(f"Processing {model_path}...")
                    main(views, model_path, output_sample_path, 1, True, True, '8', "PNG", 600, "BLENDER_EEVEE")
                    print(f"Output saved to {output_sample_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process dataset and render views for each sample.")
    parser.add_argument("--input_dataset_path", type=str, required=True, help="Input path of the dataset.")
    parser.add_argument("--output_path", type=str, required=True, help="Output path for the rendered views.")
    parser.add_argument("--views", type=int, default=30, help="Number of views to be rendered for each sample.")

    argv = sys.argv[sys.argv.index("--") + 1:]  # Extract script-specific arguments
    args = parser.parse_args(argv)

    process_dataset(args.input_dataset_path, args.output_path, args.views)