import msgpackrpc

class FileServer(object):
    def upload_text(self, text_str):
        print('text data uploaded:\n{}'.format(text_str))
        return 'received {} bytes'.format(len(text_str))

server = msgpackrpc.Server(FileServer())
server.listen(msgpackrpc.Address('128.97.92.68', 18800))
server.start()

