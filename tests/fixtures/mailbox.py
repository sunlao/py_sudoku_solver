import pytest
from actors.mailbox import Mailbox


@pytest.fixture
def mailbox() -> Mailbox:
    """Create a mailbox for testing"""
    return Mailbox()
