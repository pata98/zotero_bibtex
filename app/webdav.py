#### Webdav Client
# This is a client to interact with WebDAV server
#
# Author: Jiho Ryoo
# E-mail: yoopata@postech.ac.kr
# Date  : 2024.12.31

import requests
from requests.auth import HTTPBasicAuth
import urllib3
import xml.etree.ElementTree as ET
from typing import List

class WebDAVClient():
    """
    Class to handle WebDAV server interactions
    """
    def __init__(self, webdav_url: str, username: str, password: str, verify_ssl: bool = False):
        """
        Initialize WebDAV client.
        
        Args:
            webdav_url (str): Base URL of the WebDAV server
            username (str): WebDAV username
            password (str): WebDAV password
            verify_ssl (bool): Whether to verify SSL certificates
        """
        self.webdav_url = webdav_url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password)
        self.verify_ssl = verify_ssl
        
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def get_list(self, path: str = "", extension: str = None) -> List[str]:
        """
        List files in the WebDAV directory.
        
        Args:
            path (str): Subdirectory path
            extension (str): Filter files by extension (e.g., '.zip')
            
        Returns:
            List[str]: List of filenames
        """
        headers = {'Depth': '1'}
        url = f"{self.webdav_url}/{path}"
        print(url)
        response = requests.request('PROPFIND', url, headers=headers, 
                                 auth=self.auth, verify=self.verify_ssl)
        
        # Parse the XML response
        root = ET.fromstring(response.content)

        # Define the XML namespaces used in the response
        namespaces = {
            'd': 'DAV:',
        }

        # Extract file names
        files = []
        for response in root.findall('.//d:response', namespaces):
            href = response.find('d:href', namespaces).text
            file_name = href.rstrip('/').split('/')[-1]
            if file_name.endswith('.zip'):
                files.append(file_name)
        
        return files
    
    def download_file(self, filename: str) -> bytes:
        """
        Download a file from the WebDAV server.
        
        Args:
            filename (str): Name of the file to download
            
        Returns:
            bytes: File content
        """
        url = f"{self.webdav_url}/{filename}"
        response = requests.get(url, auth=self.auth, verify=self.verify_ssl)
        response.raise_for_status()
        return response.content