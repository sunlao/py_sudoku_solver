from asyncio import Queue
import pytest
from actors.mailbox import Mailbox
from shared.models.messages import MessageReceive
from shared.models.side_effects import MailboxSideEffects


@pytest.fixture
def mailbox() -> Mailbox:
    return Mailbox(MailboxSideEffects(queue=Queue[MessageReceive]()))


@pytest.fixture
def test_mailbox() -> Mailbox:
    return Mailbox(MailboxSideEffects(queue=Queue[MessageReceive]()))
