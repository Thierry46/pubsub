# -*- coding: utf-8 -*-
"""
Name : test_PubSub.py
Author : Thierry Maillard (TMD)
Date : 25 - 7 feb. 2018
Purpose : Unit tests for class PubSub with pytest
Ref. : https://docs.pytest.org/en/latest/
Usage : python -m pytest .
Quality checking : python3 -m pylint --disable=invalid-name test_PubSub.py
"""
# for Python 2 and 3 compatibility
from __future__ import unicode_literals

import pytest

import pubsub

def test_subscribe():
    """ Test subscride method : original test was written by by Zhen Wang
        Source : https://github.com/nehz/pubsub/blob/master/tests.py
    """
    # Get an instance of PubSub class
    communicator = pubsub.PubSub()
    # The Listener subscribes to the channel 'test'
    messageQueue = communicator.subscribe('test')
    # The publisher put the message 'Hello World' in the list of message for this channel
    communicator.publish('test', 'Hello World')
    # Test if listener has received the string 'Hello World'
    assert next(communicator.listen(messageQueue))['data'] == 'Hello World'


def test_unsubscribe():
    """ Test unsubscribe :  : original test was written by  Zhen Wang
        Source : https://github.com/nehz/pubsub/blob/master/tests.py

    """
    communicator = pubsub.PubSub()
    # The Listener subscribes to the channel 'test'
    messageQueue = communicator.subscribe('test')
    # The publisher put the message 'Hello World 1'
    communicator.publish('test', 'hello world 1')
    # The listener unsubscribes to the channel 'test'
    communicator.unsubscribe('test', messageQueue)
    # The publisher put the message 'Hello World 2'
    # Should not have been received by listener
    communicator.publish('test', 'hello world 2')
    # The listener asks for all messages
    msgs = list(messageQueue.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['data'] == 'hello world 1'


def test_noMesage():
    """ Test a query if no message was put in queue"""

    communicator = pubsub.PubSub()
    # The Listener subscribes to the channel 'test'
    messageQueue = communicator.subscribe('test')
    # Get message
    msgs = list(messageQueue.listen(block=False))
    assert not msgs


def test_noMesageOnChannel():
    """ Test query if no message put in queue"""

    communicator = pubsub.PubSub()
    # The Listener subscribes to the channel 'test'
    messageQueue = communicator.subscribe('test')
    # The publisher put the message 'Hello World 1' on other channel
    communicator.publish('OtherChannel', 'hello world')
    # Queue should be empty
    msgs = list(messageQueue.listen(block=False))
    assert not msgs


def test_2Readers():
    """ Test 2 Readers on 1 channel """

    communicator = pubsub.PubSub()
    # The Listener subscribes to the channel 'test'
    messageQueue1 = communicator.subscribe('test')
    messageQueue2 = communicator.subscribe('test')
    # The publisher put the message 'Hello World 1'
    communicator.publish('test', 'hello world 1')
    communicator.publish('test', 'hello world 2')
    # The listeners ask for all messages
    msgs = list(messageQueue1.listen(block=False))
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    # Queue should be empty
    msgs = list(messageQueue1.listen(block=False))
    assert not msgs
    # The publisher put the message 'Hello World 1'
    communicator.publish('test', 'hello world 3')
    # The listeners ask for all messages
    msgs = list(messageQueue1.listen(block=False))
    assert len(msgs) == 1
    assert msgs[0]['data'] == 'hello world 3'
    msgs = list(messageQueue2.listen(block=False))
    assert len(msgs) == 3
    assert msgs[0]['data'] == 'hello world 1'


def test_messageDateAndId():
    """ Test Id of published messages """

    communicator = pubsub.PubSub()

    # The Listener subscribes to the channel 'test'
    messageQueue = communicator.subscribe('test')
    # The publisher put 2 messages on this channel
    communicator.publish('test', 'hello world 1')
    communicator.publish('test', 'hello world 2')

    # The listener asks for all messages
    msgs = list(messageQueue.listen(block=False))

    # Tests
    assert len(msgs) == 2
    assert msgs[0]['data'] == 'hello world 1'
    assert msgs[1]['data'] == 'hello world 2'
    assert msgs[0]['id'] < msgs[1]['id']


def test_initPublishIdFalse():
    """ Test Id of published messages is always equal to 0
        if constructor is called with publishId False """

    communicator = pubsub.PubSub(is_updating_publish_id=False)

    # The Listener subscribes to the channel 'test'
    messageQueue = communicator.subscribe('test')
    # The publisher put 2 messages on this channel
    communicator.publish('test', 'hello world 1')
    communicator.publish('test', 'hello world 2')

    # The listener asks for all messages
    msgs = list(messageQueue.listen(block=False))

    # Tests
    assert len(msgs) == 2
    assert msgs[0]['id'] == 0
    assert msgs[0]['id'] == msgs[1]['id']
