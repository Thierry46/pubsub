# pubsub

Simple publish & subscribe communication pattern implemented in pure Python.

Messages can be posted by one ore more publishers on chanels and subscribers can get those messages.

Can be used in a threaded project to communicate asynchronously
between light process running in different threads.
It permits to completly separate parts of a model–view–controller software.
In that case there is no direct method calls between parts.
Message are exchanged asynchonously on communication channels and treated when subscribers are available.

This class is based on thread-safe FIFO queue standard Python
implementation and was designed thread-safe by Zhen Wang.
Compatible with python 2 and 3.

- Original author: Zhen Wang
- [https://github.com/nehz/pubsub] : Original project location
- [https://github.com/Thierry46/pubsub] : Version modified by Thierry Maillard

General documentation :
- https://en.wikipedia.org/wiki/Publish–subscribe_pattern
- https://en.wikipedia.org/wiki/Model-view-controller

Usage
=====

    import pubsub

    communicator = pubsub.PubSub()
    messageQueue = communicator.subscribe('test')
    communicator.publish('test', 'Hello World !')
    print(next(communicator.listen(messageQueue))['data'])

Hello World !

    communicator.unsubscribe('test', messageQueue)

For more information on usage, see test case file source : test_PubSub.py

Changelog
==========
* 0.2:
   * Embbed original version in a class to use it as an object in different file sources
   * Add more comments
   * Adapt unit tests written by Zhen Wang and add new ones
   * Use pytest to run unit test
* 0.1.2:
    * Updated to support Python 3
* 0.1.1:
    * Added channel unsubscribe helper: channel.unsubscribe()
    * Each published message now has a unique incrementing ID


Pre-Requisites
============
- [x] python3 or python2:  [https://www.python.org/downloads] : Download python
- [x ] six : [http://six.readthedocs.io] : Six: Python 2 and 3 Compatibility Library
- [ ] pytest : [https://docs.pytest.org/en/latest/contents.html] : for running unit tests
- [ ] pylint : [https://www.pylint.org] : A quality tool developped by Logilab.
- [ ] flex8 : [https://www.pylint.org] : The modular source code checker: pep8, pyflakes and co.


The MIT License
===============

Copyright (c) 2012 Zhen Wang

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
