
def msg2debug(origmsg, src):
    msg = utils.smime.message_from_anything(origmsg)
    try:
        cert = msg.verify()[0]
        sender_node_id = cliqueclique_node.models.Node.node_id_from_public_key(cert)
    except:
        print origmsg
        traceback.print_exc()
        sender_node_id = "UNABLETOVERIFYCERT"
        sys.exit(1)

    container_msg = msg.get_payload()[0]
    receiver_node_id = container_msg['receiver_node_id']

    print "%s <- %s" % (receiver_node_id[:settings.CLIQUECLIQUE_HASH_PRINT_LENGTH], sender_node_id[:settings.CLIQUECLIQUE_HASH_PRINT_LENGTH])
    for part in container_msg.get_payload():
        print "  %s(%s)" % (part['message_type'], part['document_id'][:settings.CLIQUECLIQUE_HASH_PRINT_LENGTH])
    #     for key, value in part.items():
    #         if key.lower() not in ('content-type', 'mime-version', 'message_type', 'document_id'):
    #             print "    %s = %s" % (key, value)


class LocalSocket(object):
    def __init__(self, dest):
        self.dest = dest
        self.buffer = []
        self.lock = threading.Lock()

    def sendto(self, data, x, address):
        with self.lock:
            self.buffer.append(data)

    def recvfrom(self, x):
        while True:
            with self.lock:
                if not self.buffer:
                    continue
                msg = self.buffer[0]
                del self.buffer[0]
                return (msg, self.dest)

