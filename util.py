import bitio
import huffman
import pickle


def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''
    tree = pickle.load(tree_stream)

    return tree

def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """      
    #The moment it thinks it is a leaf, it returns a value
    if type(tree) == huffman.TreeLeaf:
        return tree.getValue()    
    #Reads if the "bit" is 1 or 0
    bit = bitreader.readbit()    
    #if "bit" is 1, then it traverses the right, else the left
    if bit:
        return(decode_byte(tree.getRight(),bitreader))
    return(decode_byte(tree.getLeft(),bitreader))


def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''
    #We create a tree using read_tree as mentioned above
    tree_created = read_tree(compressed)
    
    
    # Instance to read bits from the "compressed" file
    read_bits = bitio.BitReader(compressed)
    # Instance to write bits to the "uncompressed" file
    write_bits = bitio.BitWriter(uncompressed)
    
    #We keep on going through the while loop till the time the end of the
    #file is reached
    #The flag checks if the file is empty (no bits) or not
    flag = True
    try:
        while flag:            
            bits_which_are_decoded = decode_byte(tree_created,read_bits)
            if bits_which_are_decoded == None:
                flag = False
            else:
                #8 bits is 1 byte
                write_bits.writebits(bits_which_are_decoded,8)
            
        write_bits.flush()
    except EOFError:
        pass
    


def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    '''
    pickle.dump(tree,tree_stream)

def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    
    #Write the tree to the file "compressed"
    write_tree(tree,compressed)
    #Make an encoding table to read every byte from it and writing
    #each bit to the "compressed" file
    table = huffman.make_encoding_table(tree)
    # Instance to read bits from the "uncompressed" file
    read_bits = bitio.BitReader(uncompressed)
    # Instance to write bits to the "compressed" file
    write_bits = bitio.BitWriter(compressed)
    #flag checks if we have reached the end of the file
    flag = False
    #the while loop goes till the time we have reached the end of
    #the file
    while not flag:
        try:
            #this reads 8 bits and stores a byte in this
            one_byte = read_bits.readbits(8)
            #we are encoding using the table (makes a dictionary)
            encode = table[one_byte]
            #going through a dictionary and writing every bit
            for bits in encode:
                write_bits.writebit(bits)
            #the moment we reach the end of the file, we make flag
            #true and the dictionary has None in it
        except EOFError:
            flag = True
            encode = table[None]
            # we then write None bitwise to mark the end of the file
            for bits in encode:
                write_bits.writebit(bits)

    write_bits.flush()