#coding: UTF-8

""" Основной файл, который вам скорее всего не придется править """
""" @author: Sm[SteeL] """

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
import os
import pickle
import inspect

def get_url_handlers(path, importadd = ""):

    """ Получаем список всех обработчиков URL из модулей и файлов """

    url_handlers = []
    # Для каждого файла или папки
    for item in os.listdir(path):
#        print item + " "
#        print os.path.join(importadd[0:-1] + "\\" + item, "__init__.py") + "\n"
        try:
            # Если это модуль
            if os.path.exists(os.path.join(importadd[0:-1], item, "__init__.py")):
                # Для каждого полученного обработчика URL из модуля
                for handler in get_url_handlers(os.path.join(path, item), importadd + item + "."):
                    # Проверяем, нет ли уже такого обработчика, и добавляем
                    if not handler in url_handlers:
                        url_handlers.append(handler)
            # Если это файл
            else:
                # Пробуем подключить
                module = __import__(importadd + item.split(".")[0], globals(), locals(), [item.split(".")[0]]) if item.split(".")[0] else False
                # Достаем все классы из модуля
                classes = inspect.getmembers(module, inspect.isclass)
                # Смотрим по всем классам
                for classes_name, classes_item in classes: #@UnusedVariable
                    # Если в классе объявлен обработчик URL, то добавляем его в список (если его там еще нет)
                    if hasattr(classes_item, 'url_handler'):
                        if not (classes_item().url_handler, classes_item) in url_handlers:
                            url_handlers.append((classes_item().url_handler, classes_item))
        # Обработчик ошибки для __init__.py и папок-не-модулей
        except ImportError: pass
    # Возвращаем отсортированный список (сортировка по обработчику, чтобы / и /.+ были в конце
    return sorted(url_handlers, key=lambda(t): t[0], reverse = True)

if __name__ == "__main__":

    """ Запускаем App Engine """

    # Пробуем получить из кэша обработчики URL
    url_handlers = memcache.get("url_handlers") #@UndefinedVariable
    # Если их там нет, получаем их с нуля и добавляем в кэш
    if not url_handlers:
        url_handlers = get_url_handlers(os.path.curdir)
        memcache.add("url_handlers", pickle.dumps(url_handlers), 3600) #@UndefinedVariable
    # Если есть, загружаем
    else:
        url_handlers = pickle.loads(url_handlers)
    # Запускаем GAE
    application = webapp.WSGIApplication(url_handlers, debug=True)
    run_wsgi_app(application)
