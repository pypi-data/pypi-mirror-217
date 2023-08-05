import sys
from ourlib import Model

# def main():
#     server_url = "http://your-server-url"
#     Model.upload_files_to_server(server_url)

# if __name__ == "__main__":
#     main()

def main(args):
    if len(args) < 2:
        print("Usage: ourlib <inference_script> <model_class>")
        return

    inference_script = args[0]
    model_class = args[1]

    # Upload files to the server
    # server_url = "http://your-server-url"
    Model.upload_files_to_server()

     # Import and execute the user-defined inference script as if it were run with `python inference.py`
    sys.path.insert(0, "")
    sys.path.insert(0, ".")
    with open(inference_script, "r") as script_file:
        script_code = script_file.read()
        exec(script_code)

if __name__ == "__main__":
    main(sys.argv[1:])