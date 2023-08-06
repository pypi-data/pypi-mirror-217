def _rename_file_manager(instance,filename,customformats,filenamemethod,hardpath):
    custom_format = ['tar.gz'] + customformats
    sp = [i for i in filename.split('.') if len(i)>0] 
    if len(sp) < 2:
        error = 'No Formats Found , Upload a File'
        raise FileNotFoundError(error)
    elif len(sp) == 2:
        ext = sp[-1]
    else:
        for format in custom_format:
            g = format.split('.')
            lg = len(g) 
            if sp[-lg:] == g:
                ext = format
                break
    if hardpath == False:
        try:
            return '%s.%s' % (filenamemethod,ext)
        except UnboundLocalError:
            return '%s.%s' % (filenamemethod,sp[-1])
    
    else:
        while hardpath[-1] == '/':
            hardpath = hardpath[0:-1:1]
        try:
            return '%s/%s.%s' % (hardpath,filenamemethod,ext)
        except UnboundLocalError:
            return '%s/%s.%s' % (hardpath,filenamemethod,sp[-1])


__all__= [ '_rename_file_manager']

def __dir__():
    return __all__

def __getattr__(name):
    if name not in __all__:
        raise AttributeError(name)
    return globals()[name]