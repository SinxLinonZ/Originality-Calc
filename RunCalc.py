from MidiConvert.main import convert_midi_to_points
import os
import argparse

def find_point_files(directory):
    target_point_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                target_point_files.append(os.path.join(root, file))
    return target_point_files


def get_file_name_without_extension(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-sd", "--source_directory", help="Source directory, where midi files are located", required=True)
    parser.add_argument("-td", "--target_directory", help="Target directory, where converted files are located", required=True)
    parser.add_argument("-od", "--original_directory", help="Original directory, where original files are located", required=True)
    parser.add_argument("-rd", "--result_directory", help="Result directory, where the results will be saved", required=True)

    args = parser.parse_args()

    # Create result directory
    os.makedirs(args.result_directory, exist_ok=True)

    convert_midi_to_points(
        directory=args.source_directory,
        window_size=16,
        step=8)

    target_point_files = find_point_files(os.path.join(os.getcwd(), args.target_directory))
    original_point_files = find_point_files(os.path.join(os.getcwd(), args.original_directory))

    # Add double quotes to each file path
    target_point_files = ['"' + file + '"' for file in target_point_files]
    original_point_files = ['"' + file + '"' for file in original_point_files]

    arg_original_point_files = ' '.join(original_point_files)
    for i in range(len(target_point_files)):
        target_point_file = target_point_files[i]
        cmd = f'./CalcSimilarity/bin/CalcSimilarity {target_point_file} {arg_original_point_files}'
        print(f'[ {i} / {len(target_point_files)} ] {cmd}')
        os.system(cmd)
        # move file
        target_point_file_name = get_file_name_without_extension(target_point_file) + '.json'
        if os.path.exists(target_point_file_name):
            os.rename(target_point_file_name, os.path.join(args.result_directory, target_point_file_name))
        else:
            print(f'Error: {target_point_file_name} failed to be processed.')
