# Создайте класс студента.
# ○ Используя дескрипторы проверяйте ФИО на первую заглавную букву и наличие только букв. Если ФИО не соответствует
# условию, выведите:
#
#
# ФИО должно состоять только из букв и начинаться с заглавной буквы
# ○ Названия предметов должны загружаться из файла CSV при создании экземпляра. Другие предметы в экземпляре
# недопустимы. Если такого предмета нет, выведите:
#
#
# Предмет {Название предмета} не найден
# ○ Для каждого предмета можно хранить оценки (от 2 до 5) и результаты тестов (от 0 до 100). В противном случае выведите:
#
#
# Оценка должна быть целым числом от 2 до 5
#
# Результат теста должен быть целым числом от 0 до 100
# ○ Также экземпляр должен сообщать средний балл по тестам для каждого предмета и по оценкам всех предметов
# вместе взятых.
#
# Вам предоставлен файл subjects.csv, содержащий предметы. Сейчас в файл записана следующая информация.
#
#
# Математика,Физика,История,Литература
# Создайте класс Student, который будет представлять студента и его успехи по предметам. Класс должен иметь
# следующие методы:
# Атрибуты класса:
#
# name (str): ФИО студента. subjects (dict): Словарь, который хранит предметы в качестве ключей и информацию об
# оценках и результатах тестов для каждого предмета в виде словаря.
#
# Магические методы (Dunder-методы):
#
# __init__(self, name, subjects_file): Конструктор класса. Принимает имя студента и файл с предметами и их результатами.
# Инициализирует атрибуты name и subjects и вызывает метод load_subjects для загрузки предметов из файла.
#
# __setattr__(self, name, value): Дескриптор, который проверяет установку атрибута name. Убеждается, что name
# начинается с заглавной буквы и состоит только из букв.
#
# __getattr__(self, name): Позволяет получать значения атрибутов предметов (оценок и результатов тестов) по их именам.
#
# __str__(self): Возвращает строковое представление студента, включая имя и список предметов.
# Студент: Иван Иванов
# Предметы: Математика, История
#
# Методы класса:
#
# load_subjects(self, subjects_file): Загружает предметы из файла CSV. Использует модуль csv для чтения данных из
# файла и добавляет предметы в атрибут subjects.
#
# add_grade(self, subject, grade): Добавляет оценку по заданному предмету. Убеждается, что оценка является целым
# числом от 2 до 5.
#
# add_test_score(self, subject, test_score): Добавляет результат теста по заданному предмету. Убеждается, что
# результат теста является целым числом от 0 до 100.
#
# get_average_test_score(self, subject): Возвращает средний балл по тестам для заданного предмета.
#
# get_average_grade(self): Возвращает средний балл по всем предметам.
import csv
import pytest


class Student:

    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects = subjects_file

    def __setattr__(self, name, value):
        if name == 'name':
            name_list = value.split(' ')
            is_name_ok = True
            for name_part in name_list:
                if name_part[0].islower() or not name_part.isalpha():
                    is_name_ok = False
            if is_name_ok:
                self.__dict__[name] = value
            else:
                raise ValueError('ФИО должно состоять только из букв и начинаться с заглавной буквы')
        if name == 'subjects':
            self.__dict__[name] = self.load_subjects(value)

    def __getattr__(self, name):
        return self.__dict__[name]

    def __str__(self):
        result = f'Студент: {self.__dict__['name']}\nПредметы: '
        for keys in self.__dict__['subjects'].keys():
            if len(self.__dict__['subjects'][keys]['grade']) != 0 or len(self.__dict__['subjects'][keys]['grade']) != 0:
                result += (keys + ', ')
        result = result[:len(result) - 2]
        return result

    # interesting point, this function is used to parse csv file, and it called from __setattr__ descriptor function
    def load_subjects(self, subjects_file):
        file = open(subjects_file, mode='r')
        subj_name = csv.DictReader(file).fieldnames
        subjects = dict()
        for subject in subj_name:
            subjects[subject] = {'grade': list(), 'test': list()}
        return subjects

    def add_grade(self, subject, grade):
        '''
        :param subject: Предмет
        :param grade: Оценка
        :return: Ничего если оценка между 2 и 5, если нет ошибка значения
        >>> stud = Student("John Johnson", 'subjects.csv')
        >>> stud.add_grade('Математика', 666)
        Traceback (most recent call last):
        ...
        ValueError: Оценка должна быть целым числом от 2 до 5
        '''
        if 2 <= grade <= 5 and subject in self.__dict__['subjects'].keys():
            self.__dict__['subjects'][subject]['grade'].append(grade)
        elif not 2 <= grade <= 5:
            raise ValueError('Оценка должна быть целым числом от 2 до 5')

    def add_test_score(self, subject, test_score):
        '''
        :param subject: Предмет
        :param grade: Результат теста
        :return: Ничего если оценка между 0 и 100, если нет ошибка значения
        >>> stud_1 = Student("John Johnson", 'subjects.csv')
        >>> stud_1.add_test_score('Математика', 666)
        Traceback (most recent call last):
        ...
        ValueError: Результат теста должен быть целым числом от 0 до 100
        '''
        if 0 <= test_score <= 100 and subject in self.__dict__['subjects'].keys():
            self.__dict__['subjects'][subject]['test'].append(test_score)
        elif not 0 <= test_score <= 100:
            raise ValueError('Результат теста должен быть целым числом от 0 до 100')

    def get_average_test_score(self, subject):
        '''
        :param subject: Предмет
        :return: Средний результат тестов
        >>> stud_2 = Student('John Johnson', 'subjects.csv')
        >>> stud_2.add_test_score('Математика', 90)
        >>> stud_2.add_test_score('Математика', 90)
        >>> stud_2.add_test_score('Физика', 80)
        >>> stud_2.add_test_score('Физика', 80)
        >>> stud_2.add_test_score('Физика', 80)
        >>> stud_2.add_test_score('История', 70)
        >>> stud_2.add_test_score('История', 70)
        >>> stud_2.add_test_score('История', 70)
        >>> stud_2.add_test_score('История', 70)
        >>> stud_2.get_average_test_score('История')
        70.0
        '''
        if subject not in self.__dict__['subjects'].keys():
            raise ValueError(f'Предмет {subject} не найден')
        summ: int = 0
        amount: int = len(self.__dict__['subjects'][subject]['test'])
        for i in self.__dict__['subjects'][subject]['test']:
            summ += i
        return summ / amount

    def get_average_grade(self):
        '''
        :return: Средняя оценка студента
        >>> stud_3 = Student('John Johnson', 'subjects.csv')
        >>> stud_3.add_grade('История', 5)
        >>> stud_3.add_grade('Математика', 5)
        >>> stud_3.get_average_grade()
        5.0
        >>> stud_3.add_grade('Литература', 4)
        >>> stud_3.add_grade('Физика', 4)
        >>> stud_3.get_average_grade()
        4.5
        '''
        summ: int = 0
        amount: int = 0
        for subject in self.__dict__['subjects'].values():
            amount += len(subject['grade'])
            for grade in subject['grade']:
                summ += grade
        return summ / amount


# Пример
#
# На входе:


# student = Student("Иван Иванов", "subjects.csv")
# print(student.subjects)
#
# student.add_grade("Математика", 4)
# student.add_test_score("Математика", 85)
#
# student.add_grade("История", 5)
# student.add_test_score("История", 92)
#
# print(student.subjects)
# average_grade = student.get_average_grade()
# print(f"Средний балл: {average_grade}")
#
# print(student.subjects)
# average_test_score = student.get_average_test_score("Математика")
# print(f"Средний результат по тестам по математике: {average_test_score}")
#
# print(student)
# На выходе:
#
#
# Средний балл: 4.5
# Средний результат по тестам по математике: 85.0
# Студент: Иван Иванов
# Предметы: Математика, История

def test_add_grade():
    stud = Student("John Johnson", 'subjects.csv')
    try:
        stud.add_grade('Математика', 666)
        assert False
    except ValueError:
        assert True


def test_add_test_score():
    stud = Student("John Johnson", 'subjects.csv')
    try:
        stud.add_test_score('Математика', 666)
        assert False
    except ValueError:
        assert True


def test_get_average_test_score():
    stud_2 = Student('John Johnson', 'subjects.csv')
    stud_2.add_test_score('Математика', 90)
    stud_2.add_test_score('Математика', 90)
    stud_2.add_test_score('Физика', 80)
    stud_2.add_test_score('Физика', 80)
    stud_2.add_test_score('Физика', 80)
    stud_2.add_test_score('История', 70)
    stud_2.add_test_score('История', 70)
    stud_2.add_test_score('История', 70)
    stud_2.add_test_score('История', 70)
    assert stud_2.get_average_test_score('История') == 70.0


def test_get_average_grade():
    stud_3 = Student('John Johnson', 'subjects.csv')
    stud_3.add_grade('История', 5)
    stud_3.add_grade('Математика', 5)
    assert stud_3.get_average_grade() == 5.0
    stud_3.add_grade('Литература', 4)
    stud_3.add_grade('Физика', 4)
    assert stud_3.get_average_grade() == 4.5


# Запускаем pytest.main() с нужными параметрами
pytest.main(["--no-header", '-q', "--durations=0", '5-task.py'])
