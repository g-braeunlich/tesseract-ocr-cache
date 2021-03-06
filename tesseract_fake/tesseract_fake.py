#!/usr/bin/python3

import os
import shutil
import sys

from tesseract_cache import tesseract_cache

#
# Wrapper for tesseract command line interface
#
# if result output file in cache, copy from cache, else return fake OCR result with status
#

def tesseract_cli_wrapper(argv, cache_dir='/var/cache/tesseract', verbose=True):
    
    if os.getenv('TESSERACT_CACHE_DIR'):
        cache_dir = os.getenv('TESSERACT_CACHE_DIR')

    if not cache_dir.endswith(os.path.sep):
        cache_dir += os.path.sep

    input_filename, tesseract_configfilename, cache_filename = tesseract_cache.parse_tesseract_parameters(argv, verbose=verbose)

    output_filename = argv[2] + '.' + tesseract_configfilename

    
    if os.path.isfile(cache_dir + cache_filename):
        if verbose:
            print("Copying OCR result for content of {} from cache {}".format(input_filename, cache_filename))
        # copy cached result to output filename
        shutil.copy(cache_dir + cache_filename, output_filename)
        return 0

    else:

        if verbose:
            print("OCR result not in cache, writing fake OCR result with status info to {}".format(output_filename))
        
        textfile = open(output_filename, 'w')
        textfile.write('[Image (no OCR yet)]')
        textfile.close()
    
        return 0


#
# If started by command line (not imported for functions) get command line parameters and start OCR
#

if __name__ == "__main__":

    # read command line parameters
    argv = sys.argv
    
    # copy OCR result from cache or run OCR by Tesseract
    result_code = tesseract_cli_wrapper(argv)
    
    sys.exit(result_code)
