# -*- coding: utf-8 -*-
"""
==============================================================================
Name :    test_PubSub_priority.py
Author :  Thierry Maillard (Thierry46)
Date :    20 Dec. 2020

Purpose : Unit tests for class PubSubPriority with pytest
          Specific tests for priorities between messages.
          Test for messages with default priority are done
          in test_PubSub.py

==============================================================================
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
==============================================================================
"""

from pubsub import PubSubPriority


def test_messages_explicit_equal_priority():
    """
    Test order of received messages published with
    2 equal explicit priorities
    """

    communicator = PubSubPriority()

    channel = "test"

    # listener subscribes to the channel
    message_queue = communicator.subscribe(channel)

    # Publisher put 2 messages with priorities different to default
    communicator.publish(channel, 'hello world 1', priority=200)
    communicator.publish(channel, 'hello world 2', priority=200)

    # listener asks for all messages
    msgs = list(message_queue.listen(block=False))

    # Tests
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'
    assert msgs[0]['id'] == 0
    assert msgs[1]['id'] == 1


def test_messages_implicit_explicit_priority_equal_priority():
    """
    Test order of received messages published with
    2 equal implicit explicit priorities
    """

    communicator = PubSubPriority()

    channel = "test"

    # listener subscribes to the channel
    message_queue = communicator.subscribe(channel)

    # Publisher put 2 messages without/with priority
    communicator.publish(channel, 'hello world 1')
    communicator.publish(channel, 'hello world 2', priority=100)

    # listener asks for all messages
    msgs = list(message_queue.listen(block=False))

    # Tests
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'
    assert msgs[0]['id'] == 0
    assert msgs[1]['id'] == 1


def test_messages_explicit_decreasing_priority():
    """
    Test order of received messages published with
    2 decreasing explicit priorities
    """

    communicator = PubSubPriority()

    channel = "test"

    # listener subscribes to the channel
    message_queue = communicator.subscribe(channel)

    # Publisher put 2 messages on this channel with explicit priorities
    communicator.publish(channel, 'hello world 1', priority=50)
    communicator.publish(channel, 'hello world 2', priority=200)

    # listener asks for all messages
    msgs = list(message_queue.listen(block=False))

    # Tests
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'
    assert msgs[0]['id'] == 0
    assert msgs[1]['id'] == 1


def test_messages_implicit_explicit_decreasing_priority():
    """
    Test order of received messages published with
    2 decreasing implicit explicit priorities
    """

    communicator = PubSubPriority()

    channel = "test"

    # listener subscribes to the channel
    message_queue = communicator.subscribe(channel)

    # Publisher put 2 messages on this channel without/ with priority
    communicator.publish(channel, 'hello world 1')
    communicator.publish(channel, 'hello world 2', priority=200)

    # listener asks for all messages
    msgs = list(message_queue.listen(block=False))

    # Tests
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'
    assert msgs[0]['id'] == 0
    assert msgs[1]['id'] == 1


def test_messages_explicit_increasing_priority():
    """
    Test order of received messages published with
    2 increasing explicit priorities
    """

    communicator = PubSubPriority()

    channel = "test"

    # listener subscribes to the channel
    message_queue = communicator.subscribe(channel)

    # Publisher put 2 messages on this channel with explicit priority
    communicator.publish(channel, 'hello world 1', priority=200)
    communicator.publish(channel, 'hello world 2', priority=50)

    # listener asks for all messages
    msgs = list(message_queue.listen(block=False))

    # Tests
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 2'
    assert msgs[1]['data'] == 'hello world 1'
    assert msgs[0]['id'] == 1
    assert msgs[1]['id'] == 0


def test_messages_implcit_explicit_increasing_priority():
    """
    Test order of received messages published with
    2 increasing implicit explicit priorities
    """

    communicator = PubSubPriority()

    channel = "test"

    # listener subscribes to the channel
    message_queue = communicator.subscribe(channel)

    # Publisher put 2 messages on this channel without/with priority
    communicator.publish(channel, 'hello world 1')
    communicator.publish(channel, 'hello world 2', priority=50)

    # listener asks for all messages
    msgs = list(message_queue.listen(block=False))

    # Tests
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 2'
    assert msgs[1]['data'] == 'hello world 1'
    assert msgs[0]['id'] == 1
    assert msgs[1]['id'] == 0


def test_messages_explicit_random_priority():
    """
    Test order of received messages published with
    random explicit priority
    """

    communicator = PubSubPriority()

    channel = "test"

    # listener subscribes to the channel
    message_queue = communicator.subscribe(channel)

    # Publisher put 5 messages on this channel with explicit priorities
    communicator.publish(channel, 'hello world 1', priority=200)
    communicator.publish(channel, 'hello world 2', priority=50)
    communicator.publish(channel, 'hello world 3', priority=25)
    communicator.publish(channel, 'hello world 4', priority=400)
    communicator.publish(channel, 'hello world 5', priority=25)

    # listener asks for all messages
    msgs = list(message_queue.listen(block=False))

    # Tests
    assert len(msgs) == 5
    assert msgs[0]['data'] == 'hello world 3'
    assert msgs[1]['data'] == 'hello world 5'
    assert msgs[2]['data'] == 'hello world 2'
    assert msgs[3]['data'] == 'hello world 1'
    assert msgs[4]['data'] == 'hello world 4'
    assert msgs[0]['id'] == 2
    assert msgs[1]['id'] == 4
    assert msgs[2]['id'] == 1
    assert msgs[3]['id'] == 0
    assert msgs[4]['id'] == 3
