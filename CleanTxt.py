import os
import argparse

def delete_txt_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                os.remove(os.path.join(root, file))
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory to delete txt files", required=True)

    args = parser.parse_args()

    delete_txt_files(args.directory)