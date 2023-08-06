import warnings
import math

class _ErrorHandling():
    
    @staticmethod
    def _random_string_error_handler(length,url_safe,regex,only_letters,only_digits,only_lowercase,only_uppercase):
        #length
        if (length_type:=type(length)) is not int:
            error = "Value must be int not {}".format("".join(str(length_type).split("'")[1:-1]))
            raise ValueError(error)
        elif length<1:
            error = f"Length must be greater than 0. The Given length {length} is {int(math.fabs(length))+1} short."
            raise IndexError(error)
        #end length



        ##############
        #regex
        elif regex and type(regex) is not str :
            error = "Regex must be a string. example: 'AaBb123#$' "
            raise ValueError(error)
        #end regex

        #only letters or digits
        elif (letter_type:=type(only_letters)) is not bool:
            error = "Value for only_letters must be boolean not {}".format("".join(str(letter_type).split("'")[1:-1]))
            raise ValueError(error)
        elif (digits_type:=type(only_digits)) is not bool:
            error = "Value for only_digits must be boolean not {}".format("".join(str(digits_type).split("'")[1:-1]))
            raise ValueError(error)
        
        #Disallowing from using regex and only_letters and only_digits at the same time.
        elif sum([bool(regex),only_letters,only_digits]) > 1:
            values = {'regex':bool(regex),'only_letters':only_letters,'only_digits':only_digits}
            variable_names = " and ".join([variable for variable,value in values.items() if value==True])
            error = f"can't use {variable_names} at the same time."
            raise TypeError(error)

        ##############

        #url_safe
        elif url_safe_type:=type(url_safe) is not bool:
            error = "Value for url_safe must be boolean not {}".format("".join(str(url_safe_type).split("'")[1:-1]))
            raise ValueError(error)
        elif (bool(regex) is False) and (url_safe is True):
            warning = "You should Use url_safe with regex since it's useless by itself."
            warnings.warn(warning,category=Warning)


        #upper and lower
        if (type_lowercase:=type(only_lowercase)) is not bool:
            error = "Value for only_lowercase must be boolean not {}".format("".join(str(type_lowercase).split("'")[1:-1]))
            raise ValueError(error)
        elif (type_uppercase:=type(only_uppercase)) is not bool:
            error = "Value for only_uppercase must be boolean not {}".format("".join(str(type_uppercase).split("'")[1:-1]))
            raise ValueError(error)
        if only_digits is True and (only_lowercase or only_uppercase):
            warning = "Using only_lowercase or only_uppercase with only_digits it's useless and won't do anything."
            warnings.warn(warning,category=Warning)
        if only_lowercase and only_uppercase:
            error = "Can't use both only_lowercase and only_uppercase at the same time."
            raise ValueError(error)
        
    
        
    @staticmethod
    def _format_finder_error_handler(filenames,customformats,find_formats,no_dot_filename,rename_files):
        #filenames
        _ErrorHandling.__find_format_errors(filenames,'filenames')
    
        #customformats
        _ErrorHandling.__find_format_errors(customformats,'customformats')
        
        #find_formats
        _ErrorHandling.__find_format_errors(find_formats,'find_formats')
        
        #no_dot_filename
        if no_dot_filename is not None:
            if (ndf_type:=type(no_dot_filename)) is not bool:
                error = """Invalid argument type. Expected a boolean value, but received {}.
                Please provide a boolean value (True or False) as the argument.""".format(str(ndf_type).split("'")[-2])
                raise TypeError(error)


        #rename_files
        if rename_files is not None:
            if (rf_type:= type(rename_files)) is not str:
                error = """Invalid argument type. Expected a string, but received {}. 
                Please provide a value of type string as the argument.""".format(str(rf_type).split("'")[-2])
                raise TypeError(error)


    @staticmethod
    def __is_iterable(obj):
        try:
            iter(obj)
            return True
        except TypeError:
            return False
        
    @staticmethod
    def __find_format_errors(param,param_name):
        if param is not None:
            if type(param) is str or  not _ErrorHandling.__is_iterable(param) :
                error = f"{param_name} must be an array with strings inside it."
                raise TypeError(error)
            elif not all(tuple(map(lambda item: isinstance(item,str),param))):
                error = "The array contains non-string elements."
                raise TypeError(error)
            elif not all(tuple(map(lambda item:'.' in item,param))):
                error = "The array contains non-file elements."
                raise ValueError(error)
            elif type(param) is dict:
                error = "Only lists, tuples, and sets are supported. Dictionaries cannot be used as an array."
                raise ValueError(error)