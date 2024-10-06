import mido
import argparse
import os


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __hash__(self):
        return hash((self.x, self.y))


def get_points_from_midi(mid):
    notes = []
    for i, track in enumerate(mid.tracks):
        ticks = 0
        for msg in track:
            ticks += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append(Point((int)(ticks / mid.ticks_per_beat), msg.note))

    return notes


def split_points_to_pieces(points, step=4, length=4):
    pieces = []
    maxStep = max(points, key=lambda x: x.x).x
    remain = maxStep % step
    for i in range(0, maxStep - remain, step):
        piece = filter(lambda x: i <= x.x < i + length, points)
        pieces.append(list(piece))
    return pieces

def save_pieces_to_file(pieces, filepath):
    dirname = os.path.dirname(filepath)
    os.makedirs(dirname, exist_ok=True)

    with open(filepath, 'w') as f:
        # piece count
        f.write(str(len(pieces)) + '\n')
        for piece in pieces:
            # point count
            f.write(str(len(piece)) + '\n')
            # points data
            for point in piece:
                f.write(str(point.x) + '\n')
                f.write(str(point.y) + '\n')
        f.close()


def get_all_midi_files(directory):
    _midi_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mid'):
                _midi_files.append(os.path.join(root, file))
    return _midi_files


def convert_midi_to_points(input_file="",
                           output="",
                           directory="",
                           output_directory="",
                           step="",
                           window_size=""):
    PIECE_STEP = step
    PIECE_LENGTH = window_size

    if input_file:
        # Read midi files
        midi_data = None
        try:
            midi_data = mido.MidiFile(input_file)
        except Exception as e:
            print(f'Error reading midi file: {input_file}')
            exit(1)

        # Convert note to points
        midi_points = get_points_from_midi(midi_data)

        pieces = split_points_to_pieces(midi_points, PIECE_STEP, PIECE_LENGTH)
        save_pieces_to_file(pieces, output or os.path.join(
            os.path.dirname(input_file), os.path.splitext(os.path.basename(input_file))[0] + '.txt'))
        print(f'Converted {input_file} -> {output or os.path.join(os.path.dirname(input_file), os.path.splitext(os.path.basename(input_file))[0] + ".txt")}')

    elif directory:
        midi_files = get_all_midi_files(directory)
        for midi_file in midi_files:
            # Read midi files
            midi_data = None
            try:
                midi_data = mido.MidiFile(midi_file)
            except Exception as e:
                print(f'Error reading midi file: {midi_file}')
                continue

            # Convert note to points
            midi_points = get_points_from_midi(midi_data)

            pieces = split_points_to_pieces(midi_points, PIECE_STEP, PIECE_LENGTH)
            save_pieces_to_file(pieces, output_directory or os.path.join(
                os.path.dirname(midi_file), os.path.splitext(os.path.basename(midi_file))[0] + '.txt'))
            print(f'Converted {midi_file} -> {output_directory or os.path.join(os.path.dirname(midi_file), os.path.splitext(os.path.basename(midi_file))[0] + ".txt")}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input midi file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-d", "--directory", help="Directory of midi files")
    parser.add_argument("-od", "--output_directory", help="Output directory")

    parser.add_argument("-s", "--step", help="Piece step", type=int, default=8)
    parser.add_argument("-ws", "--window_size", help="Piece window size", type=int, default=16)

    args = parser.parse_args()
    if not args.input and not args.directory:
        parser.error('No action requested, add --input or --directory')

    convert_midi_to_points(args.input,
                           args.output,
                           args.directory,
                           args.output_directory,
                           args.step,
                           args.window_size)
