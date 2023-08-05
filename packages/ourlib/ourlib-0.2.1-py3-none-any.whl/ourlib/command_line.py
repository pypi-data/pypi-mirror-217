import argparse
import sys
from ourlib import ourlib

def main():
    parser = argparse.ArgumentParser(prog='ourlib', description='Upload files to the server and execute an inference script.')

    parser.add_argument('deployment', help='Choose to deploy or not')
    

    args = parser.parse_args()

    deployment = args.deployment

    # Upload files to the server
    if deployment == "deploy":
        ourlib.Model.upload_files_to_server()

    # Import and execute the user-defined inference script as if it were run with `python inference.py`
    # sys.path.insert(0, "")
    # sys.path.insert(0, ".")
    # with open(deployment, "r") as script_file:
    #     script_code = script_file.read()
    #     exec(script_code)

if __name__ == "__main__":
    main()
