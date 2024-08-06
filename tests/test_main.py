import pytest

from meemirobotti import main

def test_greeter():
    assert main.greeter() == "Hello, world!"
