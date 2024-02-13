import argparse
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor


def process_model(blender_executable, views, model_path, output_sample_path, engine, hide_output=True):
    os.makedirs(output_sample_path, exist_ok=True)

    command = [
        blender_executable, "--background", "--python", "render_rgb.py", "--",
        "--views", str(views),
        "--obj", model_path,
        "--output_folder", output_sample_path,
        "--scale", "1",
        "--remove_doubles", "True",
        "--edge_split", "True",
        "--color_depth", "8",
        "--format", "PNG",
        "--resolution", "600",
        "--engine", engine
    ]

    with open(os.devnull, 'w') as devnull:

        print(f"Processing {model_path}...")
        if hide_output:
            subprocess.run(command, check=True, stdout=devnull, stderr=devnull)
        else:
            subprocess.run(command, check=True)
        print(f"Output saved to {output_sample_path}")


def process_dataset(input_dataset_path, output_path, views, blender_executable, engine, max_processes, categories, hide_output):
    tasks = []
    with ProcessPoolExecutor(max_workers=max_processes) as executor:
        for category_name in os.listdir(input_dataset_path):

            if categories and category_name not in categories:
                continue

            category_path = os.path.join(input_dataset_path, category_name)
            if os.path.isdir(category_path):
                for sample_name in os.listdir(category_path):
                    sample_path = os.path.join(category_path, sample_name)
                    model_path = os.path.join(sample_path, "models", "model_normalized.obj")

                    if os.path.exists(model_path):
                        output_sample_path = os.path.join(output_path, category_name, sample_name)
                        # Check if output directory exists and has sufficient views
                        if os.path.exists(output_sample_path):
                            num_files = len([f for f in os.listdir(output_sample_path) if
                                             os.path.isfile(os.path.join(output_sample_path, f))])
                            if num_files == views:
                                print(f"Skipping {model_path} as it already has sufficient views.")
                                continue

                        tasks.append(
                            executor.submit(process_model, blender_executable, views, model_path, output_sample_path,
                                            engine, hide_output))




    # Wait for all tasks to complete
    for future in tasks:
        future.result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process dataset and render views for each sample.")
    parser.add_argument("--input_dataset_path", type=str, required=True, help="Input path of the dataset.")
    parser.add_argument("--output_path", type=str, required=True, help="Output path for the rendered views.")
    parser.add_argument("--views", type=int, default=10, help="Number of views to be rendered for each sample.")
    parser.add_argument("--blender_path", required=True, help="Path to the Blender executable.")
    parser.add_argument("--engine", default="BLENDER_WORKBENCH", help="Blender engine to use.")
    parser.add_argument("--max_processes", type=int, default=4, help="Maximum number of parallel processes.")
    parser.add_argument("--hide_output", default=True, help="Hide output from Blender.")
    parser.add_argument("--categories", nargs='*',
                        help="Optional list of categories to process. If not provided, "
                             "all categories will be processed.")

    args = parser.parse_args()

    process_dataset(args.input_dataset_path, args.output_path, args.views, args.blender_path, args.engine,
                    args.max_processes, args.categories, args.hide_output)
