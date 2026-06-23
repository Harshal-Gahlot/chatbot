from PyPDF2 import PdfReader

def extractUploadedFiles(mes):
    for ele in mes.elements:
        # standard text files (.txt, .md, etc) # example of ele.mime are
        if "text" in ele.mime: # .txt == "text/plan" & .md == "text/markdown"
            with open(ele.path, "r", encoding="utf-8") as f:
                mes.content += f"\n\n--- content of {ele.name} ---\n{f.read()}"

        elif "pdf" in ele.mime:
            with open(ele.path, "rb") as f:
                pdf_reader = PdfReader(f)
                mes.content += f"\n\n--- Content of {ele.name} ---"
                for page in pdf_reader.pages:
                    mes.content += f"/n{page.extract_text()}"

def printError(title, message):
    RED = "\033[31m"
    RESET = "\033[0m"
    print(title + ":" + RED, message, RESET)