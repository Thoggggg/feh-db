"""
Representation of a class to store some data into the db next
"""


from abc import abstractmethod


class GenericDataConverterToDb:
    """ Abstract class defining the method that must be used for conversion """

    @abstractmethod
    def is_valid(self):
        """ Used to check if the given data fit """
        pass
