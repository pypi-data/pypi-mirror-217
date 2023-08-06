import uuid
from .__managers._django_manager import _rename_file_manager


class DjangoTools:
    def rename_file(instance,filename,customformats:list=[],filenamemethod:str=uuid.uuid4(),hardpath:str=False,*args,**kwargs) -> str :
        """
        This function is originally made for Django, but you can use it anywhere depending on your needs.
        
        This function will return you a string containing the name and format of the file and you should use this function in upload_file in Django models.
        The files are stored in the MEDIA_ROOT path in your settings.py.
        If you want to use customformat or filenametype or other things in Django models.py , create a separate function in models.py and put the following codes in it.

        def created_function(instance,filename):
            return rename_file(instance,filename,customformats=[give formats here],filenamemethod=give your method for naming files here,hardpath=give path here)

        In your model:
        image = models.ImageField(upload_to=created_function)


        If you want to save the files in another Directory in your MEDIA_ROOT you can give a path to hard path and it will save file in that path .
        
        Example: 

        def created_function(instance,filename):
            return rename_file(instance,filename,hardpath='profiles') --> file saves in -> MEDIA_ROOT/profiles/image.png


        """

        return _rename_file_manager(instance,filename,customformats,filenamemethod,hardpath,*args,**kwargs)
            








__all__= [ 'DjangoTools']

def __dir__():
    return __all__

def __getattr__(name):
    if name not in __all__:
        raise AttributeError(name)
    return globals()[name]