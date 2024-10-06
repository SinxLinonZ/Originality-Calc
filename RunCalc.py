from MidiConvert.main import convert_midi_to_points
import os

def find_point_files(directory):
    target_point_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                target_point_files.append(os.path.join(root, file))
    return target_point_files


if __name__ == '__main__':
    convert_midi_to_points(
        directory='data',
        window_size=16,
        step=8)

    target_point_files = find_point_files(os.path.join(os.getcwd(), 'single_melody', 'Morzat'))
    original_point_files = find_point_files(os.path.join(os.getcwd(), 'single_melody', 'Beet'))

    # Add double quotes to each file path
    target_point_files = ['"' + file + '"' for file in target_point_files]
    original_point_files = ['"' + file + '"' for file in original_point_files]

    arg_original_point_files = ' '.join(original_point_files)
    for i in range(len(target_point_files)):
        target_point_file = target_point_files[i]
        cmd = f'./CalcSimilarity/bin/CalcSimilarity {target_point_file} {arg_original_point_files}'
        print(f'[ {i} / {len(target_point_files)} ] {cmd}')
        os.system(cmd)

