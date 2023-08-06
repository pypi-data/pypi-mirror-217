import pytest

from smsit import GatewayManager, Gateway, Message


class DummyGateway(Gateway):
    def send(self, message):  # pragma: nocover
        pass


def test_gateway_manager():
    manager = GatewayManager()
    manager.register("dummy_gateway1", DummyGateway)
    manager.configure({"dummy_gateway1": {}})

    with pytest.raises(ValueError):
        manager.configure({"dummy_gateway2": {}})

    sms = Message(text="Hi!", receiver="989211234565")
    manager.send("dummy_gateway1", sms)
