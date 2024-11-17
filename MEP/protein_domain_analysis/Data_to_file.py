## the following function  writes data to a file with a filename that includes part of the input filename and an extension

def output_filename(input_filename, extension, filetype):
    # Extract the relevant part of the input filename
    # For example, if the input filename is "input_data.txt", you may want to extract "input_data"
    input_filename_without_extension = input_filename.split('.')[0]

    # Combine the extracted part with the desired extension to form the output filename
    output_filename = f"{input_filename_without_extension}_{extension}.{filetype}"
    return output_filename

def output_file_frontextension(extension,input_filename, filetype):
    # Extract the relevant part of the input filename
    # For example, if the input filename is "input_data.txt", you may want to extract "input_data"
    input_filename_without_extension = input_filename.split('.')[0]

    # Combine the extracted part with the desired extension to form the output filename
    output_filename = f"{extension}_{input_filename_without_extension}.{filetype}"
    return output_filename
