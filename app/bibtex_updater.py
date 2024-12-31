#### Zotero BibTeX Updater
# This script monitors a WebDAV database folder for new PDF files 
# and updates a BibTeX file using the metadata from the PDFs.
#
# Author: Jiho Ryoo
# E-mail: yoopata@postech.ac.kr
# Date  : 2024.12.31

import argparse
from webdav import WebDAVClient
from pdf2bib import PDFProcessor

def parse_arguments():
    parser = argparse.ArgumentParser(description='Update BibTeX file from WebDAV PDF files.')
    parser.add_argument('--webdav-url', required=True,
                      help='WebDAV server URL')
    parser.add_argument('--username', required=True,
                      help='WebDAV username')
    parser.add_argument('--password', required=True,
                      help='WebDAV password')
    parser.add_argument('--output-dir', default='extracted_pdfs',
                      help='Directory for extracted PDFs (default: extracted_pdfs)')
    parser.add_argument('--bibtex-path', required=True,
                      help='Path to output BibTeX file')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Initialize WebDAV client
    webdav = WebDAVClient(
        webdav_url=args.webdav_url,
        username=args.username,
        password=args.password
    )

    # Initialize PDF processor
    pdf_processor = PDFProcessor(output_dir=args.output_dir)

    # Download and process ZIP file
    try:
        file_list = webdav.get_list()

        for i in range(len(file_list)):
            # Download ZIP file
            zip_content = webdav.download_file(file_list[i])
            
            # Process PDFs and generate BibTeX
            extracted_pdfs, bibtex = pdf_processor.process_zip(
                zip_content,
                output_bibtex_path=args.bibtex_path
            )
            
            # Print results
            print("\nExtracted PDFs:")
            for pdf in extracted_pdfs:
                print(f"- {pdf}")
            
            print("\nGenerated BibTeX:")
            print(bibtex)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()