from PyPDF2 import PdfReader
from io import BytesIO
import requests

def getContent(f, file_name) -> str:
    pdf_reader = PdfReader(f)
    content = f"\n\n--- Content of {file_name} ---"
    i = 1
    for page in pdf_reader.pages:
        content += f"\npage no. {i}:\t{page.extract_text()}"
        i += 1
    return content

def extractUploadedFilesByUser(mes) -> None:
    print("we're in")
    for e in mes.elements:
        # standard text files (.txt, .md, etc) # example of ele.get("mime") are
        # .txt == "text/plan" & .md == "text/markdown"

        if "text" in e.mime:
            with open(e.path, "r", encoding="utf-8") as f:
                mes.content += f"\n\n--- content of {e.name} ---\n{f.read()}"

        elif "pdf" in e.mime:
            with open(e.path, "rb") as f:
                mes.content += getContent(f, e.name)

def getFileContentFromElement(ele) -> str:
    try:
        if "text" in ele.get("mime"):
            response = requests.get(ele["url"])
            text_content = response.content.decode("utf-8", errors="ignore")
            return f" \n\n --- content of {ele.get('name')} ---\n{text_content}"

        elif "pdf" in ele.get("mime"):
            response = requests.get(ele["url"])
            file = BytesIO(response.content)
            content = getContent(file, ele.get("name"))
            return content

    except Exception as e:
        printError("Error fetching uploaded file", e)

def printError(title, message):
    RED = "\033[31m"
    RESET = "\033[0m"
    print(title + ":" + RED, message, RESET)

