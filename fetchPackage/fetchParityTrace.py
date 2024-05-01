from web3 import HTTPProvider

client = HTTPProvider('https://cold-twilight-surf.discover.quiknode.pro/d8184f0b27f7ac8eabbadf88bd3f9c6466b18832/')
result = client.make_request('trace_call', [{
    "to": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "data": "0x70a082310000000000000000000000006E0d01A76C3Cf4288372a29124A26D4353EE51BE"
    },["trace"], "latest"])
print(result)
