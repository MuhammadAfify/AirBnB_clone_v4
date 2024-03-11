#!/usr/bin/env python3
"""Defines file storage class"""

import json

class FileStorage:
    """Represent abstracted storage engine

    Attributes:
        __file_path (str): The name of the file to save
        __objects (dict): A dictionary of instantiated objects
    """

    __file_path = "file.json"
    __objects = {}
    
    def all(self, cls=None):
        """Return dictionary of instantiated objects

        Return:
            If a cls is specified, a dictionary of objects of that type.
            Otherwise, the __objects dictionary.
        """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            dictionary = {}
            for k, v in self.__objects.items():
                if type(v) == cls:
                    dictionary[k] = v
            return dictionary
        return self.__objects
    
    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id."""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj
        
    def save(self):  
        """Serialize __objects to the JSON file"""
        
        dictionary = {}
        for key in self.__objects:
            dictionary[key] = self.__objects[key].to_dict(remove_password=False)
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(dictionary, f)

    def reload(self):
        """deserialize the JSON file __file_path to __objects"""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                for o in json.load(f).values():
                    name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(name)(**o))
        except FileNotFoundError:
            pass

