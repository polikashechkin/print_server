import os, sys, json

from domino.core import DOMINO_ROOT

class Console:
    def __init__(self, module_id = 'questions'):
        self.DIR = os.path.join(DOMINO_ROOT, 'data', 'test')
        os.makedirs(self.DIR, exist_ok=True)
        self.VALUES_FILE = os.path.join(self.DIR, f'{module_id}.def')
        self.VALUES = {}
        os.makedirs(os.path.dirname(self.VALUES_FILE), exist_ok=True)
        try:
            with open(os.path.join(self.VALUES_FILE)) as f:
                self.VALUES = json.load(f)
        except:
            pass

    def question(self, q):
        old_value = self.VALUES.get(q, ' ').strip()
        new_value = input(f'{q} [{old_value}] ? ')
        if new_value:
            self.VALUES[q] = new_value.strip()
            with open(self.VALUES_FILE, 'w') as f:
                json.dump(self.VALUES, f)
            return new_value.strip()
        else:
            return old_value

    def input(self, name, description):
        old_value = self.VALUES.get(name)
        if old_value is None:
            old_value = ''
        else:
            old_value = old_value.strip()
        new_value = input(f'{description} [{old_value}] ? ')
        if new_value:
            self.VALUES[name] = new_value.strip()
            with open(self.VALUES_FILE, 'w') as f:
                json.dump(self.VALUES, f)
            return new_value.strip()
        else:
            return old_value

    def set(self, name, value):
        if value:
            value = value.strip()
        self.VALUES[name] = value
        with open(self.VALUES_FILE, 'w') as f:
            json.dump(self.VALUES, f)

    def get(self, name, default=None):
        return self.VALUES.get(name, default)
