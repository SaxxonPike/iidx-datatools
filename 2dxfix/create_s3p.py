import argparse
import glob
import os
import struct
import sys

def get_filesize(filename):
    filesize = 0

    with open(filename, "rb") as infile:
        infile.seek(0, 2)
        return infile.tell()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Input folder', required=True)
    parser.add_argument('--output', help='Output file', required=True)
    args = parser.parse_args()

    with open(args.output, "wb") as outfile:
        outfile.write(b"S3P0")

        files = sorted(glob.glob(os.path.join(args.input, "*.wma")))

        outfile.write(struct.pack("<I", len(files)))

        offset = len(files) * 8 + 8
        for i in range(len(files)):
            filesize = get_filesize(files[i]) + 0x20
            outfile.write(struct.pack("<II", offset, filesize))
            offset += filesize

        for i in range(len(files)):
            with open(files[i], "rb") as infile:
                data = infile.read()
                filesize = len(data)
                data_hash = 0

                outfile.write(b"S3V0")
                outfile.write(struct.pack("<III", 0x20, filesize, data_hash))
                outfile.write("".join(['\0'] * 16).encode('ascii'))
                outfile.write(data)
