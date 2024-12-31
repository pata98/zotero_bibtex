#### Pdf Parser
# This read pdf file and extract metadata, then convert it to bibtex format
#
# Author: Jiho Ryoo
# E-mail: yoopata@postech.ac.kr
# Date  : 2024.12.31

import zipfile
import io
from PyPDF2 import PdfReader
import re
from datetime import datetime
import os
from typing import List, Tuple, Optional

class PDFProcessor():
    """Class to handle PDF extraction and metadata processing"""
    
    def __init__(self, output_dir: str):
        """
        Initialize PDF processor.
        
        Args:
            output_dir (str): Directory to store extracted PDFs
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def process_zip(self, zip_content: bytes, output_bibtex_path: Optional[str] = None, cleanup: bool = True) -> Tuple[List[str], str]:
        """
        Process a ZIP file containing PDFs.
        
        Args:
            zip_content (bytes): Content of the ZIP file
            output_bibtex_path (str, optional): Path to save BibTeX file
            cleanup (bool): Whether to delete extracted PDFs after processing
            
        Returns:
            Tuple[List[str], str]: (List of extracted PDF paths, BibTeX string)
        """
        zip_buffer = io.BytesIO(zip_content)
        extracted_files = self._extract_pdfs(zip_buffer)
        bibtex = self._generate_bibtex(zip_buffer, output_bibtex_path)
        
        if cleanup:
            self._cleanup_pdfs(extracted_files)
        
        return extracted_files, bibtex
    
    def _extract_pdfs(self, zip_buffer: io.BytesIO) -> List[str]:
        """Extract PDFs from ZIP buffer to output directory"""
        extracted_files = []
        
        with zipfile.ZipFile(zip_buffer) as zip_ref:
            pdf_files = [f for f in zip_ref.namelist() if f.lower().endswith('.pdf')]
            
            for pdf_file in pdf_files:
                try:
                    filename = os.path.basename(pdf_file)
                    if filename:
                        output_path = os.path.join(self.output_dir, filename)
                        with zip_ref.open(pdf_file) as source, open(output_path, 'wb') as target:
                            target.write(source.read())
                        extracted_files.append(output_path)
                        print(f"Extracted: {filename}")
                except Exception as e:
                    print(f"Error extracting {pdf_file}: {str(e)}")
        
        return extracted_files
    
    def _generate_bibtex(self, zip_buffer: io.BytesIO, output_path: Optional[str] = None) -> str:
        """Generate BibTeX entries from PDFs in ZIP buffer"""
        bibtex_entries = []
        zip_buffer.seek(0)
        
        with zipfile.ZipFile(zip_buffer) as zip_ref:
            pdf_files = [f for f in zip_ref.namelist() if f.lower().endswith('.pdf')]
            
            for pdf_file in pdf_files:
                try:
                    with zip_ref.open(pdf_file) as pdf_in_zip:
                        pdf_bytes = io.BytesIO(pdf_in_zip.read())
                        pdf_reader = PdfReader(pdf_bytes)
                        
                        metadata = pdf_reader.metadata
                        if metadata is None:
                            continue
                        
                        bibtex_entries.append(self._create_bibtex_entry(metadata, pdf_file))
                        
                except Exception as e:
                    print(f"Error processing {pdf_file}: {str(e)}")
        
        full_bibtex = "\n".join(bibtex_entries)
        
        if output_path:
            # Read existing content if file exists
            existing_content = ""
            if os.path.exists(output_path):
                with open(output_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            
            # Append new content
            with open(output_path, 'w', encoding='utf-8') as f:
                if existing_content:
                    # Add a newline between existing content and new content
                    f.write(f"{existing_content.rstrip()}\n\n{full_bibtex}")
                else:
                    f.write(full_bibtex)
        
        return full_bibtex
    
    def _create_bibtex_entry(self, metadata: dict, pdf_file: str) -> str:
        """Create a single BibTeX entry from PDF metadata"""
        title = metadata.get('/Title', '')
        if not title:
            title = pdf_file.split('/')[-1].replace('.pdf', '')
        
        citation_key = re.sub(r'[^\w]', '', title.split()[0].lower()) if title else 'unknown'
        year = metadata.get('/CreationDate', '')
        if year:
            year_match = re.search(r'D:(\d{4})', year)
            year = year_match.group(1) if year_match else datetime.now().year
        else:
            year = datetime.now().year
        
        return f"""@article{{{citation_key}{year},
                    title = {{{title}}},
                    author = {{{metadata.get('/Author', 'Unknown')}}},
                    year = {{{year}}},
                    publisher = {{{metadata.get('/Producer', 'Unknown')}}},
                }}
                """

    def _cleanup_pdfs(self, pdf_files: List[str]):
        """Delete extracted PDF files to free up space"""
        for pdf_file in pdf_files:
            try:
                if os.path.exists(pdf_file):
                    os.remove(pdf_file)
                    print(f"Cleaned up: {pdf_file}")
            except Exception as e:
                print(f"Error deleting {pdf_file}: {str(e)}")
        
        # Try to remove the output directory if it's empty
        try:
            if os.path.exists(self.output_dir) and not os.listdir(self.output_dir):
                os.rmdir(self.output_dir)
                print(f"Removed empty directory: {self.output_dir}")
        except Exception as e:
            print(f"Error removing directory {self.output_dir}: {str(e)}")