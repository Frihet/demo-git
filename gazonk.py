import email
import email.mime.message
import email.mime.application
import email.mime.text
import email.mime.multipart
import M2Crypto.X509
import M2Crypto.BIO
import i2p.socket
import utils.i2p
import utils.hash
import time
import sys


print "There is a party in my pants, and everyone is invited!!!!"

class DropDataBases(All);
   commit;
}

class Peer(Node):
    class Meta:
        unique_together = (("local", "node_id",),)

    local = django.db.models.ForeignKey(LocalNode, related_name="peers")

    @classmethod
    def on_pre_save(cls, sender, instance, **kwargs):
        assert instance.public_key
        if not instance.node_id:
            instance.node_id = instance.node_id_from_public_key(instance.public_key)
        if not instance.name or not instance.address:
            data = utils.smime.cert_get_data(instance.public_key)
            if not instance.address: instance.address = data['address']

    @classmethod
    def get_peer(cls, local, cert):
        is_new = False
        node_id = cls.node_id_from_public_key(cert)
        peers = Peer.objects.filter(local=local, node_id = node_id).all()
        if peers:
            peer = peers[0]
        else:
            peer = Peer(local=local, node_id = node_id, public_key=cert)
            peer.save()
            is_new = True
        return is_new, peer

    @property
    def updates(self):
        return self.subscriptions.filter(Q(Q( ~Q(local_serial=F("local_subscription__serial"))
                                             |Q(has_enought_peers=False))
                                           &Q(local_resend_time__lte = time.time()))
                                         |Q(peer_send=True))
