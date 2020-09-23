import os
from typing import List, Tuple

import flask
from flask import request


app = flask.Flask(__name__)


@app.route('/')
def home():
    return {'page': 'Welcome', 'href': {
        'blood_tests': flask.url_for('blood_test')
    }}


@app.route('/bloodtests')
def blood_tests():
    return {
        'page': 'List of blood tests',
        'data': [bt.dump() for bt in Datastore().get()],
        'action': {
            'add': flask.url_for('blood_test_add'),
            'delete': flask.url_for('blood_test_delet')
        }
    }


@app.route('/bloodtest/add', methods=['POST'])
def blood_test_add():
    Datastore().put(BloodTest(request.form['fullname'],
                              request.form['birthday'],
                              request.form['sex'],
                              request.form['residence'],
                              request.form['code'],
                              request.form['request']))
    return {}, 200


@app.route('/bloodtest/delete/<fullname>/<birthday>', method=['Delete'])
def blood_test_delete(fullname, birthday):
    Datastore().delete(fullname, birthday)
    return {}, 200


class BloodTest:
    fullname = birthday = sex = residence = code = result = ''

    def __init__(self, fullname='', birthday='', sex='',
                 residence='', code='', result=''):
        self.fullname = fullname
        self.birthday = birthday
        self.sex = sex
        self.residence = residence
        self.code = code
        self.result = result

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.fullname == other.fullname and self.birthday == other.birthday
        else:
            return False

    def dump(self) -> Tuple[str]:
        return (self.fullname, self.birthday, self.sex,
                self.residence, self.code, self.result)


class Datastore:
    _ds = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       '.store')

    def __init__(self):
        if not os.path.exists(self._ds):
            with open(self._ds, 'a'):
                pass

    def _read(self) -> List[str]:
        with open(self._ds, 'r') as fs:
            return fs.readlines()

    def _write(self, line: str):
        with open(self._ds, 'a') as fs:
            fs.writelines([line])

    def _rewrite(self, lines: List[str]):
        with open(self._ds, 'w') as fs:
            fs.writelines(lines)

    def get(self) -> List[BloodTest]:
        return [BloodTest(*line.split(';')) for line in self._read()]

    def put(self, blood_test: BloodTest):
        self._write(';'.join(blood_test.dump()))

    def delete(self, fullname: str, birthday: str):
        blood_tests = self.get()
        try:
            idx = blood_tests.index(BloodTest(fullname, birthday))
            blood_tests.pop(idx)
            self._rewrite([';'.join(bt.dump()) for bt in blood_tests])
        except ValueError:
            pass

