Name: Ajiitesh Gupta
ID: 1562557
CMPUT 274 Fa20

Collaborated with: No-one
Assignment 2 - Huffman Coding

Description: This file contains functions that can compress and decompress any file using Huffman Coding. Two seperate libraries, huffman.py and bitio.py contain functions crucial to the execution of this program. This file can be used by compress.py and decompress.py. Compressed files are stored as file_name.huf

Included Files:
    * util.py
    * README

Running instructions:

1.) To run the decompress dunction, in the terminal of the directory wwwroot, type the following:
	* python3 ../webserver.py
	* After that, visit http://localhost:8000 in your web browser. You should see 2 images, a person and an oval with dots around it

2.) To run the compress function, add any of the ".pdf" files to the wwwroot directory and open the terminal, and type the following:
	* python3 ../compress.py <filename>.pdf
	* After that, it will create <filename>.pdf.huf in that directory and the decompressed file can be accessed at the URL, http://localhost:8000/<filename>.pdf

3.) In the directory containing util.py, huffman.py, bitio.py, compress.py, and decompress.py, open the terminal. To access the entire program, type "make test" in the terminal and there will be a bunch of steps commpressing and decompressing and will safe decompressed files as <filename.huf>.decomp