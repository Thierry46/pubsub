# -*- coding: utf-8 -*-
"""
Name :    test_PubSub.py
Author :  Thierry Maillard (TMD)
Date :    25 Feb. 2018 - 3 dec. 2020

Purpose : Unit tests for class PubSub with pytest
Ref. pytest : https://docs.pytest.org/en/latest/

Usage : python -m pytest tests
Quality checking : python3 -m pylint test_PubSub.py

Source : https://github.com/Thierry46/pubsub (This version)

*******************************************************************************
The MIT License

Copyright (c) 2012 Zhen Wang
Copyright (c) 2020 Thierry Maillard

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
******************************************************************************
"""

# for Python 2 and 3 compatibility
from __future__ import unicode_literals

import pytest

import pubsub


def test_subscribe():
    """ Test subscribe method : original test was written by by Zhen Wang
        Source : https://github.com/nehz/pubsub/blob/master/tests.py
    """

    # Get an instance of PubSub class
    communicator = pubsub.PubSub()
    # The Listener subscribes to the channel 'test'
    message_queue = communicator.subscribe('test')
    # The publisher put the message 'Hello World'
    # in the list of message for this channel
    communicator.publish('test', 'Hello World')
    # Test if listener has received the string 'Hello World'
    assert next(communicator.listen(message_queue))['data'] == 'Hello World'


def test_unsubscribe():
    """ Test unsubscribe :  : original test was written by  Zhen Wang
        Source : https://github.com/nehz/pubsub/blob/master/tests.py
    """

    communicator = pubsub.PubSub()
    # The Listener subscribes to the channel 'test'
    message_queue = communicator.subscribe('test')
    # The publisher put the message 'Hello World 1'
    communicator.publish('test', 'hello world 1')
    # The listener unsubscribes to the channel 'test'
    communicator.unsubscribe('test', message_queue)
    # The publisher put the message 'Hello World 2'
    # Should not have been received by listener
    communicator.publish('test', 'hello world 2')
    # The listener asks for all messages
    msgs = list(message_queue.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['data'] == 'hello world 1'


def test_no_message():
    """ Test a query if no message was put in queue"""

    communicator = pubsub.PubSub()
    # The Listener subscribes to the channel 'test'
    message_queue = communicator.subscribe('test')
    # Get message
    msgs = list(message_queue.listen(block=False))
    assert not msgs


def test_no_message_on_channel():
    """ Test query if no message put in queue for a given channel """

    communicator = pubsub.PubSub()
    # The Listener subscribes to the channel 'test'
    message_queue = communicator.subscribe('test')
    # The publisher put the message 'Hello World 1' on other channel
    communicator.publish('Otherchannel', 'hello world')
    # Queue should be empty
    msgs = list(message_queue.listen(block=False))
    assert not msgs


def test_2_subscribers():
    """ Test 2 subscribers on 1 channel """

    communicator = pubsub.PubSub()

    # The two Listeners subscribe to the channel 'test'
    message_queue1 = communicator.subscribe('test')
    message_queue2 = communicator.subscribe('test')

    # The publisher put 2 messages on channel test'
    communicator.publish('test', 'hello world 1')
    communicator.publish('test', 'hello world 2')

    # The listener 1 asks for all messages
    msgs = list(message_queue1.listen(block=False))
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'

    # Queue for listener 1 should be empty
    msgs = list(message_queue1.listen(block=False))
    assert not msgs

    # The publisher put the message 'Hello World 3'
    communicator.publish('test', 'hello world 3')

    # The two listeners ask for messages
    msgs = list(message_queue1.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['data'] == 'hello world 3'
    msgs = list(message_queue2.listen(block=False))
    assert len(msgs) == 3
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'
    assert msgs[2]['data'] == 'hello world 3'


def test_message_data_and_id():
    """ Test Id of published messages """

    communicator = pubsub.PubSub()

    # The Listener subscribes to the channel 'test'
    message_queue = communicator.subscribe('test')
    # The publisher put 2 messages on this channel
    communicator.publish('test', 'hello world 1')
    communicator.publish('test', 'hello world 2')

    # The listener asks for all messages
    msgs = list(message_queue.listen(block=False))

    # Tests
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'
    assert msgs[0]['id'] == 0
    assert msgs[1]['id'] == 1


def test_init_publish_id_false():
    """ Test PubSub constructors parameter is_updating_publish_id
        Id of published messages should be always equal to 0
        when is_updating_publish_id parameter equals to False """

    communicator = pubsub.PubSub(is_updating_publish_id=False)

    # The Listener subscribes to the channel 'test'
    message_queue = communicator.subscribe('test')
    # The publisher put 2 messages on this channel
    communicator.publish('test', 'hello world 1')
    communicator.publish('test', 'hello world 2')

    # The listener asks for all messages
    msgs = list(message_queue.listen(block=False))

    # Tests
    assert len(msgs) == 2
    assert msgs[0]['id'] == 0
    assert msgs[0]['id'] == msgs[1]['id']

def test_subscriber_along_the_way():
    """ Test if a subscriber receives only messages publisched after
        he subscribes """

    communicator = pubsub.PubSub()

    # The publisher put 1 message on the channel test
    communicator.publish('test', 'hello world 1')

    # The Listener subscribes now to the channel 'test'
    message_queue = communicator.subscribe('test')

    # The Listener ask for message published,
    # but no message are published after he subscribes
    msgs = list(message_queue.listen(block=False))
    assert not msgs

    # The publisher put a second message on the channel test
    communicator.publish('test', 'hello world 2')

    # The listener asks for all messages and receives te 2nd message
    msgs = list(message_queue.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['id'] == 1
    assert msgs[0]['data'] == 'hello world 2'

def test_channel_overflow():
    """ Test behaviour when a channel overflows for a listener
        It happens when PubSub parameter max_queue_in_a_channel
        is too low. """

    # Parameter max_queue_in_a_channel set to 2
    # to overflow if more than 2 messages are stored in it.
    communicator = pubsub.PubSub(max_queue_in_a_channel=2)

    # Listener 1 and 2 subscribe to the channel 'test'
    message_queue1 = communicator.subscribe('test')
    message_queue2 = communicator.subscribe('test')

    # The publisher put 2 messages on this channel
    communicator.publish('test', 'hello world 1')
    communicator.publish('test', 'hello world 2')

    # The listener1 asks for all messages, listener 2 does nothing
    msgs = list(message_queue1.listen(block=False))
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'

    # The publisher put one more message on this channel
    communicator.publish('test', 'hello world 3')

    # No problem for listener 1
    msgs = list(message_queue1.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['data'] == 'hello world 3'

    # But queue for listener 2 has overflowed so he get
    # an exception pubsub.UnsubscribeException
    with pytest.raises(pubsub.UnsubscribeException):
        msgs = list(message_queue2.listen(block=False))

    # No matter for listener 1 who can go on with this channel
    communicator.publish('test', 'hello world 4')
    msgs = list(message_queue1.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['data'] == 'hello world 4'

    # Listener 1 has been unsubscribe so he doesn't receive anyhing more.
    communicator.publish('test', 'hello world 5')
    msgs = list(message_queue2.listen(block=False))
    assert len(msgs) == 0
