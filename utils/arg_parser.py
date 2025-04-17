import argparse

def parse_arguments():
    """
    Parses command-line arguments for the script.

    Returns:
        argparse.Namespace: The parsed arguments encapsulated within a Namespace
        object.
    """
    parser = argparse.ArgumentParser(description='Enter the prompt type you need')
    parser.add_argument('--prompt_type', help='prompt type')
    args = parser.parse_args()
    return args