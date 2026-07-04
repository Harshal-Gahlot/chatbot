from PyPDF2 import PdfReader
import io, requests

def extractUploadedFilesByUser(mes):
    for ele in mes.elements:
        # standard text files (.txt, .md, etc) # example of ele.get("mime") are
        if "text" in ele.get("mime"): # .txt == "text/plan" & .md == "text/markdown"
            with open(ele.path, "r", encoding="utf-8") as f:
                mes.content += f"\n\n--- content of {ele.name} ---\n{f.read()}"

        elif "pdf" in ele.get("mime"):
            with open(ele.path, "rb") as f:
                pdf_reader = PdfReader(f)
                mes.content += f"\n\n--- Content of {ele.name} ---"
                for page in pdf_reader.pages:
                    mes.content += f"/n{page.extract_text()}"

def getUploadedFilesFromBucket(elements):
    print("running getting files from bucket")
    for ele in elements:
        print(ele)
        if "text" in ele.get("mime"):
            with open(ele.path, "r", encoding="utf-8") as f:
                content += f"\n\n--- content of {ele.name} ---\n{f.read()}"

        elif "pdf" in ele.get("mime"):
            print("pdf exist")
            fileURL = requests.get(ele["url"])
            file = io.BytesIO(fileURL.content)
            pdf_reader = PdfReader(file)
            content = f"\n\n--- Content of {ele.get('name')} ---"
            for page in pdf_reader.pages:
                content += f"/n{page.extract_text()}"
            print(content)

def printError(title, message):
    RED = "\033[31m"
    RESET = "\033[0m"
    print(title + ":" + RED, message, RESET)
