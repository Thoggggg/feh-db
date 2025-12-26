"""
Representation of a class to store some data into the db next
"""


from abc import abstractmethod


class GenericDataConverterToDb:
    @abstractmethod
    def is_valid(self):
        pass

    @abstractmethod
    def add_to_db(self, db):
        pass
