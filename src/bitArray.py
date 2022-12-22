import array


class BitArray(object):
    '''
        Simple Bit Array class for representing an array of booleans (bits)
    '''

    def __init__(self):
        pass

    def makeBitArray(self, bitSize, fill = 0):
        '''
            Creates a bit array

            Parameters
            ----------
            bitSize : int
                    Size of bit array
            fill : int
                    Always zero

            Returns
            -------
                Bit array of a determined size for bloom filter's usage
        '''
        intSize = bitSize >> 5                  # number of 32 bit integers
        if (bitSize & 31):                      # if bitSize != (32 * n) add
            intSize += 1                        #    a record for stragglers
        if fill == 1:
            fill = 4294967295                   # all bits set
        else:
            fill = 0                            # all bits cleared

        bitArray = array.array('I')             # 'I' = unsigned 32-bit integer
        bitArray.extend((fill,) * intSize)
        return(bitArray)


    def testBit(self, array_name, bit_num):
        '''
            Checks if a bit is set to 1

            Parameters
            ----------
            array_name : str
                    Name of bit array
            bit_num : int
                    Bit number

            Returns
            -------
                Nonzero result, 2**offset, if the bit at 'bit_num' is set to 1
        '''
        record = bit_num >> 5
        offset = bit_num & 31
        mask = 1 << offset
        return(array_name[record] & mask)


    def setBit(self, array_name, bit_num):
        '''
            Sets a specific bit to 1

            Parameters
            ----------
                array_name : str
                        Name of bit array
                bit_num : int
                        Bit number

            Returns
            -------
                Integer with the bit at 'bit_num' set to 1
        '''
        record = bit_num >> 5
        offset = bit_num & 31
        mask = 1 << offset
        array_name[record] |= mask
        return(array_name[record])


    def clearBit(self, array_name, bit_num):
        '''
            Sets a specific bit to 0

            Parameters
            ----------
                array_name : str
                        Name of bit array
                bit_num : int
                        Bit number

            Returns
            -------
                Integer with the bit at 'bit_num' cleared
        '''
        record = bit_num >> 5
        offset = bit_num & 31
        mask = ~(1 << offset)
        array_name[record] &= mask
        return(array_name[record])