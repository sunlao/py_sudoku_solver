from asyncio import Queue

import pytest
from actors.mailbox import Mailbox
from shared.models.messages import Message
from shared.models.side_effects import MailboxSideEffects

@pytest.fixture
def mailbox() -> Mailbox:
    return Mailbox(MailboxSideEffects(queue=Queue[Message]()))


@pytest.fixture
def test_mailbox() -> Mailbox:
    return Mailbox(MailboxSideEffects(queue=Queue[Message]()))
