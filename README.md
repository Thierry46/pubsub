# pubsub

Simple publish & subscribe communication pattern written in pure Python (object designed).

Messages can be posted by one ore more publishers on channels and subscribers can get those messages.

Can be used in a threaded project to communicate asynchronously
with light-weight process running in different threads.
(see test case tests/test_pubsub_load.py for example)

It allows complet separation of parts of a model–view–controller software.
In that case there are no direct method calls between parts.
Message are exchanged asynchronously on communication channels and processed when subscribers are available.

This class PubSub is based on thread-safe Python standard FIFO (First In First Out) queue implementation and was designed thread-safe by Zhen Wang.
Compatible with python >= 3.6 only.

New in v0.4 : implement PubSubPriority class to register messages with priorities

- Original author: Zhen Wang
- [https://github.com/nehz/pubsub] : Original project location
- [https://github.com/Thierry46/pubsub] : Version modified by Thierry Maillard

General documentation :
- [https://en.wikipedia.org/wiki/Publish–subscribe_pattern]
- [https://en.wikipedia.org/wiki/Model-view-controller]

Usage
=====

    import pubsub

    communicator = pubsub.PubSub()
    messageQueue = communicator.subscribe('test')
    communicator.publish('test', 'Hello World !')
    print(next(messageQueue.listen())['data'])

Hello World !

    communicator.unsubscribe('test', messageQueue)

For more information on usage, see test case file sources : in tests subdirectory

Changelog
==========
* v0.4 :
    * just warn when queue overflows when publishing in a channel
    * implement PubSubPriority to register messages with priorities
    * only support Python >= 3.6 but not Python 2
    * improve quality metrics
    * remove listen method in main PubSub communicator class, use ChanelQueue*.listen() instead.
    * replace functool.partial use by ChanelQueue* class
* 0.3:
   * Improved explanation of parameter max_queue_in_a_channel with comments.
   * Addition of a new test case with listeners and senders working in threads.
   * Placement of test cases in a separate directory.
   * Addition of new test cases to check possible usage problems.
   * Restoration of original behaviour when a channel overflows.
   * Correction of spelling mistakes.
* 0.2:
   * Embedment of original version in a class to use PubSub as an object
     in different file sources
   * Addition of more comments
   * Adaptation of unit tests written by Zhen Wang and add new ones
   * Use of pytest to run unit test
* 0.1.2:
    * Updated to support Python 3
* 0.1.1:
    * Added channel unsubscribe helper: channel.unsubscribe()
    * Each published message now has a unique incrementing ID


Pre-Requisites
============
- [x] python3.6 :  [https://www.python.org/downloads] : Download python
- [ ] pytest : [https://docs.pytest.org/en/latest/contents.html] : for running unit tests
- [ ] pylint : [https://www.pylint.org] : A quality tool developed by Logilab.
- [ ] flake8 : [https://flake8.pycqa.org/en/latest] : Tool For Style Guide Enforcement, McCabe complexity.
- [ ] coverage : [https://coverage.readthedocs.io/en/coverage-5.3.1] : a tool for measuring code coverage of Python programs

The MIT License
===============

Copyright (c) 2012 Zhen Wang
Copyright (c) 2020 Thierry Maillard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
