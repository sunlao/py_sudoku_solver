import pytest
from actors.mailbox import Mailbox


@pytest.fixture
def mailbox() -> Mailbox:
    return Mailbox()


@pytest.fixture
def test_mailbox() -> Mailbox:
    return Mailbox()
