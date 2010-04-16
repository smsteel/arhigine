#coding: UTF-8

""" Класс-"контейнер" """
class AttributeContainer(object):
    
    # Словарь, где хранятся имена аттрибутов и их значения
    __dict__ = {}
    
    # Переопределение встроенного метода в Python
    # Задает значение val для аттрибута name
    def __setattr__(self, name, val):
        
        self.__dict__[name] = val
    
    # Переопределение встроенного метода в Python
    # Получаем значение аттрибута name
    def __getattr__(self, name):
        
        return self.__dict__[name]

    # Задание аттрибута "вручную"
    def set(self, name, val):
        
        self.__dict__[name] = val
