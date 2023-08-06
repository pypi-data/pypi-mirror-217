from orwynn.base.module import Module
from orwynn.base.service import Service
from orwynn.boot import Boot
from orwynn.bootscript.bootscript import Bootscript
from orwynn.bootscript.calltime import CallTime
from orwynn.di.di import Di
from orwynn.utils import validation


class SomeService(Service):
    def __init__(self) -> None:
        super().__init__()
        self.some_var: int = 0


def some_bootscript(some_service: SomeService) -> None:
    some_service.some_var = 1


def test_basic():
    Boot(
        Module(Providers=[SomeService]),
        bootscripts=[
            Bootscript(
                fn=some_bootscript,
                call_time=CallTime.AFTER_ALL
            )
        ]
    )

    some_service: SomeService = validation.apply(
        Di.ie().find("SomeService"),
        SomeService
    )

    assert some_service.some_var == 1
