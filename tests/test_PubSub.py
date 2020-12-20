# -*- coding: utf-8 -*-
"""
==============================================================================
Name :    test_PubSub.py
Author :  Thierry Maillard (Thierry46)
Date :    25 Feb. 2018 - 20 Dec. 2020

Purpose : Unit tests for class PubSub and PubSubPriority with pytest
          PubSubPriority must behave PubSub class when no priority
          is given to publish() method

Source : https://github.com/Thierry46/pubsub (This version)

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

import pytest

from pubsub import PubSub, PubSubPriority


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_subscribe(class_2_test):
    """
    Test subscribe method : original test was written by by Zhen Wang
    Source : https://github.com/nehz/pubsub/blob/master/tests.py
    """

    # Get an instance of PubSub class
    communicator = class_2_test()

    channel = "test"

    # The Listener subscribes to the channel
    message_queue = communicator.subscribe(channel)
    assert message_queue.name == channel

    # The publisher put the message 'Hello World'
    # in the list of message for this channel
    communicator.publish(channel, 'Hello World')

    # Test if listener has received the string 'Hello World'
    assert next(message_queue.listen())['data'] == 'Hello World'


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_unsubscribe_communicator(class_2_test):
    """
    Test unsubscribe using communicator method
    """

    communicator = class_2_test()

    channel = "test"

    # The Listener subscribes to the channel
    message_queue = communicator.subscribe(channel)

    # The publisher put the message 'Hello World 1'
    communicator.publish(channel, 'hello world 1')

    # The listener unsubscribes to the channel
    communicator.unsubscribe(channel, message_queue)

    # The publisher put the message 'Hello World 2'
    # Should not have been received by listener
    communicator.publish(channel, 'hello world 2')

    # The listener asks for all messages
    msgs = list(message_queue.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['data'] == 'hello world 1'


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_unsubscribe_channel(class_2_test):
    """
    Test unsubscribe using channel queue method
    """

    communicator = class_2_test()

    channel = "test"

    # The Listener subscribes to the channel
    message_queue = communicator.subscribe(channel)

    # The publisher put the message 'Hello World 1'
    communicator.publish(channel, 'hello world 1')

    # The listener unsubscribes to the channel
    message_queue.unsubscribe()

    # The publisher put the message 'Hello World 2'
    # Should not have been received by listener
    communicator.publish(channel, 'hello world 2')

    # The listener asks for all messages
    msgs = list(message_queue.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['data'] == 'hello world 1'


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_no_message(class_2_test):
    """ Test a query if no message was put in queue """

    communicator = class_2_test()

    # The Listener subscribes to the channel 'test'
    message_queue = communicator.subscribe('test')

    # Get message but no message
    msgs = list(message_queue.listen(block=False))
    assert not msgs


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_no_message_on_channel(class_2_test):
    """ Test query if no message put in queue for a given channel """

    communicator = class_2_test()
    # The Listener subscribes to the channel 'test'
    message_queue = communicator.subscribe('test')
    # The publisher put the message 'Hello World 1' on other channel
    communicator.publish('Otherchannel', 'hello world')
    # Queue should be empty
    msgs = list(message_queue.listen(block=False))
    assert not msgs


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_2_subscribers(class_2_test):
    """ Test 2 subscribers on 1 channel """

    communicator = class_2_test()

    channel = "test"

    # The two Listeners subscribe to the same channel
    message_queue1 = communicator.subscribe(channel)
    message_queue2 = communicator.subscribe(channel)

    # The publisher put 2 messages on channel test'
    communicator.publish(channel, 'hello world 1')
    communicator.publish(channel, 'hello world 2')

    # The listener 1 asks for all messages
    msgs = list(message_queue1.listen(block=False))
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'

    # Queue for listener 1 should be empty
    msgs = list(message_queue1.listen(block=False))
    assert not msgs

    # The publisher put the message 'Hello World 3'
    communicator.publish(channel, 'hello world 3')

    # The two listeners ask for messages
    msgs = list(message_queue1.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['data'] == 'hello world 3'
    msgs = list(message_queue2.listen(block=False))
    assert len(msgs) == 3
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'
    assert msgs[2]['data'] == 'hello world 3'


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_message_data_and_id(class_2_test):
    """ Test Id of published messages """

    communicator = class_2_test()

    channel = "test"

    # The Listener subscribes to the channel
    message_queue = communicator.subscribe(channel)
    # The publisher put 2 messages on this channel
    communicator.publish(channel, 'hello world 1')
    communicator.publish(channel, 'hello world 2')

    # The listener asks for all messages
    msgs = list(message_queue.listen(block=False))

    # Tests
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'
    assert msgs[0]['id'] == 0
    assert msgs[1]['id'] == 1


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_subscriber_along_the_way(class_2_test):
    """
    Test if a subscriber receives only messages published after
    he subscribes
    """

    communicator = class_2_test()

    channel = "test"

    # The publisher put 1 message on the channel test
    communicator.publish(channel, 'hello world 1')

    # The Listener subscribes now to the channel
    message_queue = communicator.subscribe(channel)

    # The Listener ask for message published,
    # but no message are published after he subscribes
    msgs = list(message_queue.listen(block=False))
    assert not msgs

    # The publisher put a second message on the channel
    communicator.publish(channel, 'hello world 2')

    # The listener asks for all messages and receives the 2nd message
    msgs = list(message_queue.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['id'] == 1
    assert msgs[0]['data'] == 'hello world 2'


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_channel_overflow(class_2_test):
    """
    Test behaviour when a channel overflows for a listener
    It happens when PubSub parameter max_queue_in_a_channel
    is too low.
    When overflow a warning must be sent by publish method,
    but when problem is solved by pulling messages,
    the listener queue must run as usual.
    """

    # Parameter max_queue_in_a_channel set to 2
    # to overflow if more than 2 messages are stored in it.
    communicator = class_2_test(max_queue_in_a_channel=2)

    channel = "test"

    # Listener 1 and 2 subscribe to the same channel
    message_queue1 = communicator.subscribe(channel)
    message_queue2 = communicator.subscribe(channel)

    # The publisher put 2 messages on this channel
    communicator.publish(channel, 'hello world 1')
    communicator.publish(channel, 'hello world 2')

    # The listener1 asks for all messages, listener 2 does nothing
    msgs = list(message_queue1.listen(block=False))
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'

    # The publisher put one more message on this channel
    # Test that a warning must be sent for listener 2 that overflows
    with pytest.warns(UserWarning, match='Queue overflow for channel test'):
        communicator.publish(channel, 'hello world 3')

    # No problem for listener 1
    msgs = list(message_queue1.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['data'] == 'hello world 3'

    # But queue for listener 2 has overflowed so he
    # receives only the two first message
    msgs = list(message_queue2.listen(block=False))
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'

    # Listener 2 is not full and is again able to receive new messages
    communicator.publish(channel, 'hello world 4')
    msgs = list(message_queue2.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['data'] == 'hello world 4'


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_exception_subscribe(class_2_test):
    """
    Test exceptions and messages for PubSub.subscribe().
    """

    communicator = class_2_test()

    # Subscribing with wrong channel = None
    with pytest.raises(ValueError,
                       match=('channel : None value not allowed')):
        communicator.subscribe(None)


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_exception_unsubscribe(class_2_test):
    """
    Test exceptions and message for PubSub.unsubscribe().
    """

    communicator = class_2_test()

    message_queue = communicator.subscribe('Test')
    with pytest.raises(ValueError,
                       match=('channel : None value not allowed')):
        communicator.unsubscribe(None, message_queue)
    with pytest.raises(ValueError,
                       match=('message_queue : None value not allowed')):
        communicator.unsubscribe('Test', None)


@pytest.mark.parametrize("class_2_test", [PubSub, PubSubPriority])
def test_exception_publish(class_2_test):
    """
    Test exceptions and messages for PubSub.publish().
    """

    communicator = class_2_test()

    with pytest.raises(ValueError,
                       match=('channel : None value not allowed')):
        communicator.publish(None, "message")
    with pytest.raises(ValueError,
                       match=('message : None value not allowed')):
        communicator.publish('Test', None)


def test_exception_publish_priority():
    """
    Test exceptions and messages for PubSubPriority.publish().
    """

    communicator = PubSubPriority()

    with pytest.raises(ValueError,
                       match=('priority must be > 0')):
        communicator.publish("Test", "message", -1)
