import msgpackrpc

client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
result = client.call('check_connection')

print('Result is:',result)
