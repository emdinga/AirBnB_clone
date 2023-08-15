#!/usr/bin/python3
"""
command interpreter for HBNB console
"""

import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """Command interpreter for the HBNB console."""

    prompt = '(hbnb) '
    VALID_CLASSES = ['BaseModel', 'User', 'State', 'City', 'Amenity', 'Place', 'Review']

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt."""
        pass

    def do_quit(self, arg):
        """Exit the command interpreter."""
        return True

    def do_EOF(self, arg):
        """Exit the command interpreter (Ctrl-D or Ctrl-Z)."""
        print()
        return True

    def do_help(self, arg):
        """Provide help information."""
        cmd.Cmd.do_help(self, arg)

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it (to the JSON file) and print the id"""
        if not arg:
            print("** class name missing **")
        elif arg not in self.VALID_CLASSES:
            print("** class doesn't exist **")
        else:
            new_obj = eval(arg)()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.VALID_CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key in models.storage.all():
                print(models.storage.all()[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id (save the change into the JSON file)"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.VALID_CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key in models.storage.all():
                models.storage.all().pop(key)
                models.storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances based or not on the class name"""
        args = arg.split()
        obj_list = []
        if not arg or args[0] in self.VALID_CLASSES:
            for key, obj in models.storage.all().items():
                obj_list.append(str(obj))
            print(obj_list)
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
    """Updates an instance based on the class name and id with a dictionary representation."""
    args = arg.split(",")
    if not args:
        print("** class name missing **")
        return
    class_name = args[0]
    if class_name not in self.VALID_CLASSES:
        print("** class doesn't exist **")
        return
    if len(args) < 2:
        print("** instance id missing **")
        return
    instance_id = args[1].strip()
    key = "{}.{}".format(class_name, instance_id)
    if key not in models.storage.all():
        print("** no instance found **")
        return
    if len(args) < 3:
        print("** attribute name missing **")
        return
    attr_name = args[2].strip()
    if len(args) < 4:
        print("** value missing **")
        return
    attr_value = args[3].strip()
    obj = models.storage.all()[key]
    if hasattr(obj, attr_name):
        if hasattr(obj, attr_name) and isinstance(getattr(obj, attr_name), int):
            attr_value = int(attr_value)
        elif hasattr(obj, attr_name) and isinstance(getattr(obj, attr_name), float):
            attr_value = float(attr_value)
        setattr(obj, attr_name, attr_value)
        obj.save()
    else:
        print("** attribute doesn't exist **")

    def default(self, line):
        """Handles commands of the form <class name>.method()"""
        tokens = line.split('.')
        if len(tokens) >= 2 and tokens[0] in self.VALID_CLASSES:
            class_name = tokens[0]
            method_tokens = tokens[1].split('(')
            method_name = method_tokens[0]
            method_args = method_tokens[1][:-1]  # Remove the closing parenthesis

            if method_name == "all":
                self.do_all(class_name)
            elif method_name == "count":
                self.do_count(class_name)
            elif method_name == "show":
                self.do_show(f"{class_name} {method_args}")
            elif method_name == "destroy":
                self.do_destroy(f"{class_name} {method_args}")
            elif method_name == "update":
                self.do_update(f"{class_name} {method_args}")
        else:
            print("*** Unknown syntax: {}".format(line))

    def do_count(self, arg):
        """Prints the count of instances of a class"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] in self.VALID_CLASSES:
            count = 0
            for key in models.storage.all():
                if args[0] in key:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()

