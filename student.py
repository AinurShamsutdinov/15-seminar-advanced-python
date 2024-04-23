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
import argparse
import csv
import logging

import pytest


class Student:
    file_name: str = ''

    logging.basicConfig(filename='project.log',
                        filemode='w',
                        encoding='utf-8',
                        level=logging.INFO,
                        format='%(levelname)s %(asctime)s %(message)s',
                        datefmt='%m/%d/%Y%I:%M:%S %p')

    def __init__(self, name, subjects_file):
        logging.info(f'Student name = {name}, subjects file name = {subjects_file}')
        self.name = name
        self.subjects = subjects_file

    def __setattr__(self, name, value):
        logging.info(f'Setting attribute = {name}, attribute value = {value}')
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
        logging.info(f'Get attribute = {name}')
        return self.__dict__[name]

    def __str__(self):
        result = f'Студент: {self.__dict__['name']}\nПредметы: '
        logging.info(f'Student to string, name = {self.name}, subjects = {self.subjects.keys}')
        for keys in self.__dict__['subjects'].keys():
            if len(self.__dict__['subjects'][keys]['grade']) != 0 or len(self.__dict__['subjects'][keys]['grade']) != 0:
                result += (keys + ', ')
        result = result[:len(result) - 2]
        return result

    # interesting point, this function is used to parse csv file, and it called from __setattr__ descriptor function
    def load_subjects(self, subjects_file):
        logging.info(f'Reading subjects from file {subjects_file}')
        file = open(subjects_file, mode='r')
        subj_name = csv.DictReader(file).fieldnames
        subjects = dict()
        for subject in subj_name:
            subjects[subject] = {'grade': list(), 'test': list()}
        return subjects

    def add_grade(self, subject, grade):
        logging.info(f'Adding subject {subject}, with grade {grade}')
        if 2 <= grade <= 5 and subject in self.__dict__['subjects'].keys():
            self.__dict__['subjects'][subject]['grade'].append(grade)
        elif not 2 <= grade <= 5:
            raise ValueError('Оценка должна быть целым числом от 2 до 5')

    def add_test_score(self, subject, test_score):
        logging.info(f'Adding test score of subject {subject} and score {test_score}')
        if 0 <= test_score <= 100 and subject in self.__dict__['subjects'].keys():
            self.__dict__['subjects'][subject]['test'].append(test_score)
        elif not 0 <= test_score <= 100:
            raise ValueError('Результат теста должен быть целым числом от 0 до 100')

    def get_average_test_score(self, subject):
        logging.info(f'Getting average test score of subject {subject}, student {self.name}')
        if subject not in self.__dict__['subjects'].keys():
            raise ValueError(f'Предмет {subject} не найден')
        summ: int = 0
        amount: int = len(self.__dict__['subjects'][subject]['test'])
        for i in self.__dict__['subjects'][subject]['test']:
            summ += i
        average_test_score = summ / amount
        logging.info(f'Getting average test score {average_test_score} of subject {subject}, student {self.name}')
        return average_test_score

    def get_average_grade(self):
        logging.info(f'Getting average grade of student {self.name}')
        summ: int = 0
        amount: int = 0
        for subject in self.__dict__['subjects'].values():
            amount += len(subject['grade'])
            for grade in subject['grade']:
                summ += grade
        average_grade = summ / amount
        logging.info(f'Getting average grade of student {self.name}, average grade {average_grade}')
        return average_grade


def test_add_grade():
    subjects_file = Student.file_name
    stud = Student("John Johnson", subjects_file)
    try:
        stud.add_grade('Математика', 666)
        assert False
    except ValueError:
        assert True


def test_add_test_score():
    subjects_file = Student.file_name
    stud = Student("John Johnson", subjects_file)
    try:
        stud.add_test_score('Математика', 666)
        assert False
    except ValueError:
        assert True


def test_get_average_test_score():
    subjects_file = Student.file_name
    stud_2 = Student('John Johnson', subjects_file)
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
    subjects_file = Student.file_name
    stud_3 = Student('John Johnson', subjects_file)
    stud_3.add_grade('История', 5)
    stud_3.add_grade('Математика', 5)
    assert stud_3.get_average_grade() == 5.0
    stud_3.add_grade('Литература', 4)
    stud_3.add_grade('Физика', 4)
    assert stud_3.get_average_grade() == 4.5


parser = argparse.ArgumentParser(description='Console argument parser')
parser.add_argument('file_name', default=None, metavar='N', type=str, nargs='*', help='File name with subjects')
args = parser.parse_args()
Student.file_name = args.__dict__['file_name'][0]
print(f'Student.file_name = {Student.file_name}')
# start test from consle with command: python3 student.py subjects.csv
pytest.main(["--no-header", '-q', "--durations=0", 'student.py'])
