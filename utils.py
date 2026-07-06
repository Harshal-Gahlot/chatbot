from PyPDF2 import PdfReader
import io, requests

def extractUploadedFilesByUser(mes):
    for ele in mes.elements:
        # standard text files (.txt, .md, etc) # example of ele.get("mime") are
        if "text" in ele.mime: # .txt == "text/plan" & .md == "text/markdown"
            with open(ele.path, "r", encoding="utf-8") as f:
                mes.content += f"\n\n--- content of {ele.name} ---\n{f.read()}"

        elif "pdf" in ele.mime:
            with open(ele.path, "rb") as f:
                pdf_reader = PdfReader(f)
                mes.content += f"\n\n--- Content of {ele.name} ---"
                i = 1
                for page in pdf_reader.pages:
                    mes.content += f"\npage no. {i}:\t{page.extract_text()}"
                    i += 1

def getUploadedFilesFromBucket(ele):
    try:
        if "text" in ele.get("mime"):
            print("found a text file")
            response = requests.get(ele["url"])
            text_content = response.content.decode("utf-8", errors="ignore")
            return f" \n\n --- content of {ele.get('name')} ---\n{text_content}"

        elif "pdf" in ele.get("mime"):
            print("found a pdf file")
            response = requests.get(ele["url"])
            file = io.BytesIO(response.content)
            pdf_reader = PdfReader(file)
            content = f"\n\n--- Content of {ele.get('name')} ---"
            i = 1
            for page in pdf_reader.pages:
                content += f"\npage no. {i}:\t{page.extract_text()}"
                i += 1
            return content
    except Exception as e:
        printError("Error featching uploaded file", e)

def printError(title, message):
    RED = "\033[31m"
    RESET = "\033[0m"
    print(title + ":" + RED, message, RESET)
