def import_package(string:'module import string'):
    '''
    Импорт модуля. В случае его отсутствия - производится попытка установки модуля в систему.
    '''
    # type 1.1: import sys
    # type 1.2: import sys, pandas
    # type 1.3: import matplotlib.pyplot as plt
    # type 1.4: import matplotlib.pyplot as plt, sys
    # type 2.1: from IPython.display import display, Markdown
    # type 2.2: from IPython.display import display as dis, Markdown
    split_string = string.replace(',', ', ').split()
    if split_string[0] == 'import':
        #package = split_string[1]
        string1 = string[string.find('import')+7:].strip()
        split_string = string1.split(',')
        packages={}
        for package in split_string:
            tmp = package.split(' as ')
            package_name = tmp[0].strip()
            package_alias = tmp[1].strip() if len(tmp) == 2 else package_name
            packages[package_alias] = package_name
            #print(f'6: {pd=}')
            try:
                    print(f'1: {package_alias=} {globals().keys()=}')
                    #global pd
                    if package_alias in globals(): print(f'8')
                    else: print(f'9')
                    print(f'5: {pd=}')
                    var = eval(package_alias)
                    print(f'4: {var=}')
                    if str(type(eval(package_alias))) == "<class 'module'>":
                        print('2')
                        class_of_alias = str(eval(package_alias)).split("'")[1]
                        print(f'Псевдоним {package_alias} уже используется модулем "{class_of_alias}". Загрузка пропущена.')
                    else: print('3')
            except:
                pass
        print(f'{packages=}')
        #if split_string[2] == 'as': alias = split_string[3]
        #else: alias = package
    elif split_string[0] == 'from':
        package = split_string[1]
# загвоздка со взаимодействием с глобальными переменными

[https://habr.com/ru/articles/512102/](Динамическое определение класса в Python)

#_print_default = print
#def print(string):
    #_print_default('перегуженная версия print')
#    _print_default(string)

#def import_package(string:'module import string'):
#    '''
#    Импорт модуля. В случае его отсутствия - производится попытка установки модуля в систему.
#    '''
#    try:
#        exec(string)
#        print(f'{string}		successfully')
#    except:
#        print(f'{string}		failed. ')
#        query = string.split()
#        if query[0] == 'import':
#            package = query[1]
#        elif query[2] == 'import':
#            package = query[1]
#        else:
#            print(f'The "{string}" query failed to recognize the module name')
#            return
#        print(f'An attempt will be made to install the module into the system.')
#        error_code = system(f'pip install {package}')
#        if error_code == 0:
#            print('Attempt to install module "{package}" into the system: successful')
#            try:
#                exec(string)
#                print(f'{string}		successfully')
#            except:
#                print(f'{string}		failed')
#        else:
#            print(f'"pip install {package}" return {error_code} error code')

# декоратор для pandas
# источник идеи https://tirinox.ru/class-decorator/
#def pandas_with_added_functions(cls):
#    class pandas_upd:
#        def __init__(self, *args, **kwargs):
#            self._obj = cls(*args, **kwargs)
#        def __getattribute__(self, s):
#            try:
#                x = super().__getattribute__(s)
#            except AttributeError:
#                pass
#            else:
#                return x
#            
#            attr = self._obj.__getattribute__(s)
#            # это метод?
#            if isinstance(attr, type(self._obj.__init__)):
#                return self._obj.attr
#            else:
#                # не метод, что-то другое
#                return attr
#        def test(self):
#            self.test.__annotations__['return'] = 'test'
#            return 'test'
#        def __str__(self):
#            # позволяет использовать print
#            return self._obj.__str__()
#        def __repr__(self):
#            # формирует текстовое представление в функциях display,
#            # интерактивном выводе значения переменной и пр.
#            return self._obj.__repr__()
#        #def __format__(self, format_spec):
#            #if isinstance(format_spec, unicode):
#            #    return unicode(str(self._obj))
#            #else:
#            #    return str(self._obj)
#        #    return str(self._obj)
#        
#        # автоматически не подтягивается индексирование декорированного класса
#        # укажем явно
#        def __getitem__(self, s):
#            return self._obj.__getitem__(s)
#    return pandas_upd

def duplicated__set(dataset:'pd.core.frame.DataFrame'):
    '''
    Возвращает сет индексов строк, являющихся полными дубликатами
    '''
    result = []
    for i , v in enumerate(dataset.duplicated()):
        if v: result.append(i)
    return set(result)

