import sys, traceback, config
RED = "\033[31m"
RESET = "\033[0m"

def handle_error(fun, *args):
    try:
        fun(*args)
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        print("\nUnder CODE BLOCK: ",RED,traceback.extract_tb(exc_tb)[1].line, RESET)
        print("line number: ",traceback.extract_tb(exc_tb)[1].lineno)
        print("function name: ",traceback.extract_tb(exc_tb)[1].name)
        print("filename: ", "/".join(traceback.extract_tb(exc_tb)[1].filename.split("/")[-2:]))
        print("ERROR MESSAGE:",RED, str(e), RESET)
    
