# import sys
# import argparse
# from ourlib import ourlib

# # def main():
# #     server_url = "http://your-server-url"
# #     Model.upload_files_to_server(server_url)

# # if __name__ == "__main__":
# #     main()

# def main():
#     # if len(args) < 2:
#     #     print("Usage: ourlib <inference_script> <model_class>")
#     #     return

#     parser = argparse.ArguemmtParser(description="")
#     model_class = args[1]

#     # Upload files to the server
#     # server_url = "http://your-server-url"
#     ourlib.Model.upload_files_to_server()

#      # Import and execute the user-defined inference script as if it were run with `python inference.py`
#     sys.path.insert(0, "")
#     sys.path.insert(0, ".")
#     with open(inference_script, "r") as script_file:
#         script_code = script_file.read()
#         exec(script_code)

# if __name__ == "__main__":
#     main(sys.argv[1:])

import argparse
import sys
from ourlib import ourlib

def main():
    parser = argparse.ArgumentParser(prog='ourlib', description='Upload files to the server and execute an inference script.')

    parser.add_argument('inference_script', help='Path to the user-defined inference script')
    parser.add_argument('model_class', help='Name of the model class defined in the inference script')

    args = parser.parse_args()

    inference_script = args.inference_script
    model_class = args.model_class

    # Upload files to the server
    # server_url = "http://your-server-url"
    ourlib.Model.upload_files_to_server()

    # Import and execute the user-defined inference script as if it were run with `python inference.py`
    sys.path.insert(0, "")
    sys.path.insert(0, ".")
    with open(inference_script, "r") as script_file:
        script_code = script_file.read()
        exec(script_code)

if __name__ == "__main__":
    main()
