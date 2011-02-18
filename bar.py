import django.db.models
import idmapper.models
import django.contrib.auth.models
import fcdjangoutils.signalautoconnectmodel
import settings
import cliqueclique_node.models
import cliqueclique_document.models
from django.db.models import Q
from utils.curryprefix import curryprefix

import email
import email.mime.message
import email.mime.application
import email.mime.text
import email.mime.multipart

import utils.smime

import time
import sys

import query

def format_change(n, o, trunk = False):
    nn = n
    oo = o
    if trunk:
        nn = nn[:settings.CLIQUECLIQUE_HASH_PRINT_LENGTH]
        oo = oo[:settings.CLIQUECLIQUE_HASH_PRINT_LENGTH]
    res = str(nn)
    if n != o:
        res += '(%s)' % (oo,)
    return res

class BaseDocumentSubscription(fcdjangoutils.signalautoconnectmodel.SharedMemorySignalAutoConnectModel):
    class Meta:
        abstract = True

    center_node_is_subscribed = django.db.models.BooleanField(default=False)
    center_node_id = django.db.models.CharField(max_length=settings.CLIQUECLIQUE_HASH_LENGTH, null=True, blank=True)
    center_distance = django.db.models.IntegerField(default = 0)
    serial = django.db.models.IntegerField(default = 0)

    PROTOCOL_ATTRS = ('has_enought_peers',
                      'is_wanted',
                      'is_subscribed',
                      'center_node_is_subscribed',
                      'center_node_id',
                      'center_distance',
                      'serial')
