# -*- coding: utf-8 -*-

"""Operator plugin that inherits a base class and is made available through `type`."""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from PyInquirer import prompt

from typing import Union, List, Dict
from cookiecutter.operators import BaseOperator

logger = logging.getLogger(__name__)


class InquirerExpandOperator(BaseOperator):
    """
    Operator for PyInquirer `expand` type prompt.

    https://github.com/CITGuru/PyInquirer/blob/master/examples/expand.py

    :param message: String message to show when prompting.
    :param choices: A list of strings or list of k/v pairs per above description
    :param name: A key to insert the output value to. If not provided defaults
        to inserting into parent key
    :return: List of answers
    """

    type: str = 'expand'

    default: Union[Dict, List[str], str] = None
    name: str = 'tmp'
    message: str = None

    def execute(self):
        if not self.no_input:
            question = {
                'type': self.type,
                'name': self.name,
                'message': self.message,
            }
            if self.default:
                question.update({'default': self.default})

            response = prompt([question])
            if self.name != 'tmp':
                return response
            else:
                return response['tmp']
        elif self.default:
            return self.default
        else:
            # When no_input then return empty list
            return []
