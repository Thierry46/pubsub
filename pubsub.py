# -*- coding: utf-8 -*-
"""==============================================================================
Name:         pubsub
Purpose:      Simple publish & subscribe in pure python
                Can be used in a threaded project to communicate asynchronously
                between light process running in different threads.
Reference:    https://en.wikipedia.org/wiki/Publish–subscribe_pattern
Requirement:  Python v2.7.x or 3.x
Quality:
    - Codding rules control :
        python3 -m pylint pubsub.py
        flake8
    - 7 unit tests in test_PubSub.py : python2 -m pytest .
Author:       Zhen Wang
Created:      23 Oct 2012
Modified:     7 febr. 2018 by Thierry Maillard
    - Embbed original version in a class to use it as an object in different
      file sources of your project.
    - Add more comments
    - Adapt unit tests written by Zhen Wang and add new ones
Licence:      MIT License
Source :
    - https://github.com/nehz/pubsub (Original version)
    - https://github.com/Thierry46/pubsub (This version)

**********************************************************************************
The MIT License

Copyright (c) 2012 Zhen Wang
Copyright (c) 2018 Thierry Maillard

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
*****************************************************************************************
"""

from threading import Lock as lock
from functools import partial

# for Python 2 and 3 compatibility
from six.moves.queue import Queue as queue, Empty


class PubSub():
    """ Implement communication Design Patern : Publish-subscribe
        Ref : https://en.wikipedia.org/wiki/Publish–subscribe_pattern
        Publishers write messages on channels and subscribers get them
        in an asynchronious way.

        For limitations, see  __init__() constructor parameters and default
        values.

        This class is based on thread-safe FIFO queue standard Python
        implementation and was designed thread-safe by Zhen Wang. """

    def __init__(self, max_queue_in_a_channel=100, max_id_4_a_chanel=2**31,
                 is_updating_publish_id=True):
        """ Create an object to be used as a communicator in a project
            between publishers and subscribers
            Optionals parameters :
            - max_queue_in_a_channel :
                - Maximum number of queue that can be listened on a given
                    channel.
                - Default value: 100
            - max_id_4_a_chanel :
                - Maximum value for message 'id' field value on a
                    communication chanel.
                - Default value: 2**31
            - is_updating_publish_id :
                - If set, message dictionnary key 'id' is updated with
                    an uniq integer
                - Else id is always set to 0
                - Default value: True. """

        self.max_queue_in_a_channel = max_queue_in_a_channel
        self.max_id_4_a_chanel = max_id_4_a_chanel
        self.is_updating_publish_id = is_updating_publish_id

        self.channels = {}
        self.count = {}

        self.channels_lock = lock()
        self.count_lock = lock()

    def subscribe(self, channel):
        """ Return a synchronized FIFO queue object used by a subscriber to listen
            at messages sent by a publisher on a given channel.
            No problem if channel doesn't exists yet.
            Ref.: https://docs.python.org/2/library/queue.html """

        if not channel:
            raise ValueError('channel')

        if channel not in self.channels:
            self.channels_lock.acquire()
            # Need to check again
            if channel not in self.channels:
                self.channels[channel] = []
            self.channels_lock.release()

        msg_q = queue()
        self.channels[channel].append(msg_q)

        msg_q.listen = partial(self.listen, msg_q)
        msg_q.unsubscribe = partial(self.unsubscribe, channel, msg_q)
        msg_q.name = channel
        return msg_q

    def unsubscribe(self, channel, msg_q):
        """ Used by a subscriber who doesn't want to receive message on a
            given channel and on a queue (msg_q) obtained previously by
            subscribe method """

        if not channel:
            raise ValueError('channel')
        if not msg_q:
            raise ValueError('msg_q')
        try:
            self.channels[channel].remove(msg_q)
        except ValueError:
            pass

    def listen(self, msg_q, block=True, timeout=None):
        """ Called by a subscriber.
            Returns an iterator that can be used to get messages sent by a
            publisher in the queue.

            Iterator can be casted in Python list by a instruction i.e. :
                msgs = list(messageQueue.listen(block=False))

            Messages are of type dictionary with 2 keys registred inside
            by publish() method:
                'data' : the message's payload that was put in the queue by
                            publishers (see publish() method).
                'id' : Number of this message on the current channel
            Ref. : https://docs.python.org/2/tutorial/datastructures.html

            Parameters :
            - msg_q : a queue obtained by the subscriber by subscribe() method
            - block (default value: True) and timeout (default value: None)
                and behaviours if no message is in the queue can be found in
                Python official Queue documentation and especially in its get()
                method : see : https://docs.python.org/2/library/queue.html """
        while True:
            try:
                data = msg_q.get(block=block, timeout=timeout)
            except Empty:
                return
            yield data

    def publish(self, channel, data):
        """ Called by publisher.
            Send a message in a channel, all subscribers registred on this
            communication channel are going to receive the message.
            If the channel doesn't exists, it is created.
            If Nobody listen to the channel (like often in real life) :
            no matter...

            Parameters :
                - channel : a string identifying the channel
                - data : payload that wil be carried by the message.

            Message received by subscribers using listen() method is a
            python dictionnary with 2 keys registred inside, see listen()
            method documentation for more."""

        if not channel:
            raise ValueError('channel')
        if not data:
            raise ValueError('data')

        if channel not in self.channels:
            self.channels_lock.acquire()
            # Need to check again
            if channel not in self.channels:
                self.channels[channel] = []
            self.channels_lock.release()

        # Update message self.counts
        if self.is_updating_publish_id:
            self.count_lock.acquire()
            if channel not in self.count:
                self.count[channel] = 0
            else:
                self.count[channel] = (self.count[channel] + 1) % self.max_id_4_a_chanel
            self.count_lock.release()
        else:
            self.count[channel] = 0

        # ID of current message
        _id = self.count[channel]

        # Push to all subscribers in channel
        for channel_queue in self.channels[channel]:
            # Remove queues that are not being consumed
            if channel_queue.qsize() > self.max_queue_in_a_channel:
                # Send termination msg and unsub
                channel_queue.put(None, block=False)
                self.unsubscribe(channel, channel_queue)
                continue
            # Build and send message to this queue
            channel_queue.put({'data': data, 'id': _id}, block=False)
