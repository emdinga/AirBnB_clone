#!/usr/bin/python3
"""
This class  create a unique FileStorage instance and call the reload() method
"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()

