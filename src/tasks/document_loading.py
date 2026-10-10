import os
import pathlib
from pypdf import PdfReader

class DocumentLoader:
    def __init__(self: DocumentLoader) -> None:
        self.data: str = ""
        self.docs_path: pathlib.Path = pathlib.Path(__file__).parent.parent.parent / "data" / "docs"
        self.save_path: pathlib.Path = pathlib.Path(__file__).parent.parent.parent / "data" / "artifacts"

    def load_documents(self: DocumentLoader, input_folder: pathlib.Path) -> str:
        """ Reads all PDF files in input_folder, extracts their text, and combines them into output_txt_path. """
        
        input_folder: str = input_folder.absolute()
        combined_text: list[str] = []
        
        if not os.path.exists(input_folder):
            print(f"Error: The folder '{input_folder}' does not exist.")
            return

        pdf_files: list[str] = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in '{input_folder}'.")
            return

        print(f"Found {len(pdf_files)} PDF(s). Starting extraction...")

        for filename in pdf_files:
            pdf_path: str = os.path.join(input_folder, filename)
            print(f"Processing: {filename}")
            
            try:
                reader = PdfReader(pdf_path)
                combined_text.append(f"\n\n{'='*40}\nFILE: {filename}\n{'='*40}\n") # adding a header for each file in the combined text
                
                # extracting text page by page
                for page_num, page in enumerate(reader.pages):
                    text: str = page.extract_text()
                    if text:
                        combined_text.append(text)
                    else:
                        combined_text.append(f"[Warning: Could not extract text from page {page_num + 1} of {filename}]")
                        
            except Exception as e:
                print(f"Error reading {filename}: {e}")

        self.data = "".join(combined_text)

        try:
            with open(file=self.save_path / "knowledge_base.txt", mode='w', encoding='utf-8') as output_file:
                output_file.write(self.data)
            print(f"Success! Combined text saved to: {self.save_path / "knowledge_base.txt"}")

        except Exception as e:
            print(f"Error saving output file: {e}")
    
        return self.data
    
    def load_knowledge_base(self: DocumentLoader) -> str:
        with open(file=self.save_path, mode='r') as fp:
            content: str = fp.read()
            return content

