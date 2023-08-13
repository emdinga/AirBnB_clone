#!/usr/bin/python3
"""
a class FileStorage that serializes instances
to a JSON file and deserializes JSON file to instances
"""

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    This class manages the serialization and deserialization of objects to/from JSON files.
    """
    __file_path = "file.json"
    __objects = {}
    classes = {
            "BaseModel": BaseModel,
            "User": User,
    }

    def all(self):
        """
        Returns the dictionary __objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Add a new object to the __objects dictionary.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serialize and save the objects to the JSON file.
        """
        obj_dict = {key: obj.to_dict() for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserialize and reload the objects from the JSON file.
        """
        if exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    class_name = value['__class__']
                    del value['__class__']
                    obj = globals()[class_name](**value)
                    FileStorage.__objects[key] = obj
    def do_create(self, data):
        """
        Creates a new User instance"""

        new_user = User(**data)
        self.new(new_user)
        self.save()
        return new_user.id

    def do_show(self, class_name, obj_id):
        """
        Retrieves a User instance by class name and ID
        """
        key = "{}.{}".format(class_name, obj_id)
        return FileStorage.__objects.get(key, None)

    def do_destroy(self, class_name, obj_id):
        """
        Deletes a User instance by class name and ID
        """
        key = "{}.{}".format(class_name, obj_id)
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
            self.save()

    def do_update(self, class_name, obj_id, data):
        """
        Updates a User instance by class name and ID
        """
        key = "{}.{}".format(class_name, obj_id)
        if key in FileStorage.__objects:
            obj = FileStorage.__objects[key]
            for attr, value in data.items():
                setattr(obj, attr, value)
            self.save()

    def do_all(self, class_name):
        """
        Retrieves all User instances or all instances of a specific class
        """
        if class_name:
            return {key: obj for key, obj in FileStorage.__objects.items()
                    if key.startswith(class_name)}
        return FileStorage.__objects

if __name__ == "__main__":
    storage = FileStorage()
    storage.reload()

