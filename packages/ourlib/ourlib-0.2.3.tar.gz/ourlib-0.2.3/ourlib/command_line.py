import argparse
import sys
from ourlib import ourlib

def main():
    parser = argparse.ArgumentParser(prog='ourlib', description='Upload files to the server and execute an inference script.')

    parser.add_argument('argument', help='Choose to argument or not')

    args = parser.parse_args()

    argument = args.argument

    # Upload files to the server
    if argument == "upload":
        ourlib.Model.upload_files_to_server()

    elif argument == "deploy":
        ourlib.Model.deploy()
    # Import and execute the user-defined inference script as if it were run with `python inference.py`
    # sys.path.insert(0, "")
    # sys.path.insert(0, ".")
    # with open(deployment, "r") as script_file:
    #     script_code = script_file.read()
    #     exec(script_code)

if __name__ == "__main__":
    main()
