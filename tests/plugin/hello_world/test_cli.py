# -*- coding: utf-8 -*-
import sys
import json
import six
from . import KomandHelloWorld
from komand.cli import CLI
from komand.handler import stream_class

cli = CLI(KomandHelloWorld())


def capture_stdout():
    old = sys.stdout
    sys.stdout = stream_class()

    cli.run()

    value = sys.stdout.getvalue()
    sys.stdout = old

    return value


def test_cli_info():

    # Disabling test for python 2 because dicts are not ordered
    if six.PY2:
        return

    cli.args = ['info']
    actual_value = capture_stdout()
    expected_value = u"""Name:        [92mHello_world[0m
Vendor:      [92mkomand[0m
Version:     [92m1.0.0[0m
Description: [92mA hello world plugin for SDK testing[0m

Triggers ([92m3[0m):
└── [92mhello_trigger[0m (Prints a greeting every 10 seconds[0m)
└── [92mreturn_bad_json_trigger[0m (This trigger will return JSON which doesnt match the spec[0m)
└── [92mthrow_exception_trigger[0m (This trigger will always throw an exception as soon as its invoked[0m)

Actions ([92m3[0m):
└── [92mhello[0m (Print hello world[0m)
└── [92mreturn_bad_json[0m (This action will return JSON which doesnt match the spec[0m)
└── [92mthrow_exception[0m (This action will always throw an exception as soon as its invoked[0m)

"""
    assert actual_value == expected_value


def test_cli_sample_action():
    cli.args = ['sample', 'hello']
    value = capture_stdout()
    expected_value = u'{"body": {"action": "hello", "meta": {}, "input": {"name": ""}, ' + \
                     '"connection": {"greeting": "Hello, {}!"}}, "type": "action_start", "version": "v1"}'
    assert json.loads(value) == json.loads(expected_value)


def test_cli_sample_trigger():
    cli.args = ['sample', 'hello_trigger']
    value = capture_stdout()
    expected_value = u'{"body": {"trigger": "hello_trigger", "meta": {}, "input": {"name": ""}, ' + \
                     '"dispatcher": {"url": "http://localhost:8000", "webhook_url": ""}, ' + \
                     '"connection": {"greeting": "Hello, {}!"}}, "type": "trigger_start", "version": "v1"}'
    assert json.loads(value) == json.loads(expected_value)


def test_cli_test_action():
    cli.args = ['test']
    sys.stdin = open('./tests/plugin/action/input.json')
    expected_output = json.load(open('./tests/plugin/action/test_output.json'))
    actual_output = json.loads(capture_stdout())
    assert actual_output == expected_output


def test_cli_test_trigger():
    cli.args = ['test']
    sys.stdin = open('./tests/plugin/trigger/input.json')
    expected_output = json.load(open('./tests/plugin/trigger/test_output.json'))
    actual_output = json.loads(capture_stdout())
    assert actual_output == expected_output


def test_cli_run_action():
    cli.args = ['run']
    sys.stdin = open('./tests/plugin/action/input.json')
    expected_output = json.load(open('./tests/plugin/action/output.json'))
    actual_output = json.loads(capture_stdout())
    assert actual_output == expected_output
