# -*- coding: utf-8 -*-
"""
Name :    test_PubSub_load.py
Author :  Thierry Maillard (TMD)
Date :    25 Feb. 2018 - 3 dec. 2020

Purpose : Unit tests for class PubSub with pytest with threads
Ref. pytest : https://docs.pytest.org/en/latest/

Usage : python -m pytest tests
Quality checking : python3 -m pylint test_PubSub_load.py

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

import time
import threading

import six

import pubsub

# Global variable ARE_CHILDREN_OK may be set to False by a listener thread
# If there is a problem, so other listeners stop
ARE_CHILDREN_OK = True

def test_load_pubsub():
    """ Test 2 channels, 2 senders and 3 readers for many messages
        senders and listeners work in different threads """

    six.print_("test_load_pubsub : start")
    # Parameter max_queue_in_a_channel default value 100 must be increased
    # because more messages are send in channel C2.
    communicator = pubsub.PubSub(max_queue_in_a_channel=100000)

    # Max number of message send
    # also used to test if all message are received by listeners
    number_of_message_on_channel_1 = 50
    number_of_message_on_channel_2 = 500

    thread_name = "listener_1"
    chanel_name = "C1"
    full_thread_name = "Listener : " + thread_name + " on " + chanel_name
    listener_1 = Listener(chanel_name, full_thread_name,
                          communicator, number_of_message_on_channel_1)
    listener_1.start()

    thread_name = "listener_2"
    full_thread_name = "Listener : " + thread_name + " on " + chanel_name
    listener_2 = Listener(chanel_name, full_thread_name,
                          communicator, number_of_message_on_channel_1)
    listener_2.start()

    thread_name = "listener_3"
    chanel_name = "C2"
    full_thread_name = "Listener : " + thread_name + " on " + chanel_name
    listener_3 = Listener(chanel_name, full_thread_name,
                          communicator, number_of_message_on_channel_2)
    listener_3.start()

    thread_name = "sender_1"
    chanel_name = "C1"
    full_thread_name = "Sender : " + thread_name + " on " + chanel_name
    sender_1 = Sender(thread_name, chanel_name, full_thread_name,
                      communicator, number_of_message_on_channel_1)
    sender_1.start()

    thread_name = "sender_2"
    chanel_name = "C2"
    full_thread_name = "Sender : " + thread_name + " on " + chanel_name
    sender_2 = Sender(thread_name, chanel_name, full_thread_name,
                      communicator, number_of_message_on_channel_2)
    sender_2.start()

    # test_load_pubsub parent thread wait for children to finish
    sender_1.join()
    sender_2.join()
    listener_1.join()
    listener_2.join()
    listener_3.join()
    six.print_("test_load_pubsub : End")

    assert ARE_CHILDREN_OK, "Problem of number of messages"


class Listener(threading.Thread):
    """ Class defining a listener used in a thread """

    def __init__(self, chanel_name, full_thread_name,
                 communicator, number_of_message_waited):
        """
        Constructor for this listener
        parameters :
        - thread_name : name of this listener
        - chanel_name : name of the channel to listen
        - full_thread_name : long name for this thread
        - communicator : system pubsub.
        """

        threading.Thread.__init__(self, name=full_thread_name)
        self.full_thread_name = full_thread_name
        self.communicator = communicator
        self.number_of_message_waited = number_of_message_waited
        self.message_queue = self.communicator.subscribe(chanel_name)

    def run(self):
        """ Method called by start() method of the thread. """

        # If problem, this listener can warn the others with
        # ARE_CHILDREN_OK set to False.
        global ARE_CHILDREN_OK

        six.print_(self.full_thread_name, "Run start, listen to messages ",
                   " with a pause of 100ms between each one...")

        is_running = True
        counter = 0
        while is_running and ARE_CHILDREN_OK:

            message = next(self.communicator.listen(self.message_queue))
            # pubsub.publish() can send a None message and unsubscribe listener
            # if there is to many messages in the channel.
            # See parameter max_queue_in_a_channel.
            if message:
                six.print_(self.full_thread_name, "receives : id :",
                           message['id'], ":", message['data'])
                time.sleep(0.1)
                is_running = (message['data'] != "End")
                counter += 1
            else:
                is_running = False

        if ARE_CHILDREN_OK:
            six.print_(self.full_thread_name,
                       "Last message received : End so stop")
            # +1 for End message added by sender
            if counter != (self.number_of_message_waited + 1):
                ARE_CHILDREN_OK = False
                six.print_("problem in", self.full_thread_name,
                           ": bad number of messages received",
                           str(counter), "instead of",
                           str(self.number_of_message_waited))


class Sender(threading.Thread):
    """ Class defining a message sender used in a thread """

    def __init__(self, thread_name, chanel_name, full_thread_name,
                 communicator, nb_of_message_2_send):
        """
        Constructor for this sender
        parameters :
        - name : name of this listener
        - chanel_name : name of the channel to listen
        - full_thread_name : long name for this thread
        - communicator : system pubsub.
        - nb_of_message_2_send : number of message to send on the chanel
        """

        threading.Thread.__init__(self, name=full_thread_name)
        self.thread_name = thread_name
        self.chanel_name = chanel_name
        self.full_thread_name = full_thread_name
        self.nb_of_message_2_send = nb_of_message_2_send
        self.communicator = communicator
        self.message_queue = communicator.subscribe(chanel_name)

    def run(self):
        """ Methode called by start() method of the thread. """

        six.print_(self.full_thread_name, "Run start, send ",
                   self.nb_of_message_2_send,
                   "with a pause of 50ms between each one...")

        for counter in range(self.nb_of_message_2_send):
            message = ('hello world ' + str(counter) + ' from ' +
                       self.thread_name + ' for ' + self.chanel_name)
            self.communicator.publish(self.chanel_name, message)
            time.sleep(0.05)

        six.print_(self.full_thread_name, self.nb_of_message_2_send,
                   " sent End to stop chanels listeners.")
        self.communicator.publish(self.chanel_name, "End")
