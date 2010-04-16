#coding: UTF-8

# Класс-"контейнер"
class AttributeContainer(object):
    
    # Словарь, где хранятся имена аттрибутов и их значения
    __dict__ = {}
    
    # Переопределение встроенного метода в Python
    # Задает значение val для аттрибута name
    def __setattr__(self, name, value):
        
        self.__dict__[name] = value
    
    # Переопределение встроенного метода в Python
    # Получаем значение аттрибута name
    def __getattr__(self, name):
        
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return None

    # Задание аттрибута "вручную"
    def set(self, name, value):
        
        self.__dict__[name] = value
