import unittest
import sys
import os
import json
import decimal

from komand.action import Action, Task
from komand.variables import Input, Output
from komand.connection import Connection

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                # This is potentially dangerous - it seems simplejson treats these as strings
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class CustomEncoderConnection(Connection):
    schema = {
        "type": "object",
        "properties": {
            "price": {
                "type": "number"
            },
            "name": {
                "type": "string"
            },
        }
    }

    def __init__(self):
        super(self.__class__, self).__init__(self.schema)
    
    def connect(self, params={}):
        return None


class CustomEncoderActionInput(Input):
    schema = {
        "type": "object",
        "properties": {
            "greeting": {
                "type": "string"
            },
        }
    }

    def __init__(self):
        super(self.__class__, self).__init__(schema=self.schema)


class CustomEncoderActionOutput(Output):
    schema = {
        "type": "object",
        "required": ["price", "name"],
        "properties": {
            "price": {
                "type": "number"
            },
            "name": {
                "type": "string"
            },
        }
    }

    def __init__(self):
        super(self.__class__, self).__init__(schema=self.schema)


class CustomEncoderAction(Action):
    def __init__(self):
        super(self.__class__, self).__init__(
                'stupid', 
                'an action',
                CustomEncoderActionInput(), 
                CustomEncoderActionOutput(),
                )

    def run(self, params={}):
        return {
            'price': decimal.Decimal('1100.0'),
            'name': 'Jon'
        }

    def test(self, params={}):
        return {
            'price': decimal.Decimal('1.1'),
            'name': 'Jon'
        }


class TestActionRunner(unittest.TestCase):

    def test_custom_encoder_action_succeeds(self):
        task = Task(CustomEncoderConnection(), CustomEncoderAction(), {
            'body': {
                'action': 'stupid',
                'input': {
                    'greeting': 'hello'
                },
                'meta': {
                    'action_id': 12345
                },
            }
        }, custom_encoder=DecimalEncoder)

        task.test()


if __name__ == '__main__':
    unittest.main()
