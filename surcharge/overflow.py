#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from zmq import Context
from zmq import SUB, PUB, REP, REQ
from zmq import SUBSCRIBE

from random import randint
from json import dumps
from json import loads
from collections import OrderedDict


# TODO: comments in english
# TODO: handles zeroMQ exceptions
# TODO: ipc adress
class Master(object):

    # TODO: check the socket adresse
    def __init__(self, full_socket_address):
        self.context = Context()
        self.workers = OrderedDict()
        self.overflow_launch = False
        self.full_socket_address = full_socket_address
        self.socket_address, self.socket_port = full_socket_address.split(':')

    @property
    def init_pubsocket(self):
        ''' initialise la socket pour permettre de lancer
        le benchmark via un publish
        '''
        self.pubsocket = self.context.socket(PUB)
        self.pubsocket.bind('tcp://{}'.format(self.full_socket_address))

    @property
    def init_repsocket(self):
        ''' init la socket pour permettre de repondre à un
        nouveau worker qui vient s'ajouter dynamiquement
        par default ce port est fixe (5555)
        '''
        self.repsocket = self.context.socket(REP)
        self.repsocket.bind('tcp://{}:5555'.format(self.socket_address))

    @property
    def wait_workers(self):
        ''' permet l'ajout de worker en attendand le
        message pour lancer le benchmark
        '''
        while not self.overflow_launch:
            message = loads(self.repsocket.recv_json())
            # workers
            if '_id' in message:
                self.workers[message['_id']] = 'ready'
                self.repsocket.send('ok')
                sys.stdout.write('worker {} is ready\n'.format(message['_id']))
            # overflow signals
            elif 'overflow' in message:
                self.repsocket.send('ok')
                sys.stdout.write('master: launch overflow\n')
                self.launch_benchmark

    @property
    def launch_benchmark(self):
        ''' declenche le benchmark
        '''
        self.pubsocket.send('OVERFLOW')


class Worker(object):

    def __init__(self, master_full_socket_address):
        self.context = Context()
        self.worker_id = randint(1, 100000)
        self.overflow_launch = False
        self.master_full_socket_address = master_full_socket_address
        self.master_socket_address, self.master_socket_port = master_full_socket_address.split(':')

    @property
    def init_subsocket(self):
        ''' permet de recevoir le message pour lancher le benchmark
        '''
        self.subsocket = self.context.socket(SUB)
        self.subsocket.connect('tcp://{}'.format(self.master_full_socket_address))
        self.subsocket.setsockopt(SUBSCRIBE, '')

    @property
    def init_reqsocket(self):
        ''' permet de prevenir le master de l'ajout d'un nouveau
        worker
        '''
        self.reqsocket = self.context.socket(REQ)
        self.reqsocket.connect('tcp://{}:5555'.format(self.master_socket_address))

    @property
    def iam_ready(self):
        ''' contact le master
        '''
        ready = False
        while not ready:
            msg = {'_id': self.worker_id}
            self.reqsocket.send_json(dumps(msg))
            if self.reqsocket.recv() == 'ok':
                ready = True

    @property
    def waiting_benchmark(self):
        '''
        attend le message d'overflow
        '''
        while not self.overflow_launch:
            self.subsocket.recv()
            self.overflow_launch = True


class Launcher(Worker):

    def __init__(self, master_full_socket_address):
        super(Launcher, self).__init__(master_full_socket_address)
        self.init_reqsocket
        self.launch_overflow

    @property
    def launch_overflow(self):
        msg = {'overflow': True}
        self.reqsocket.send_json(dumps(msg))
        if self.reqsocket.recv() == 'ok':
            sys.exit(0)
