

import pytest, os, sys, time

from fdi.testsupport.fixtures import BG_SERVER_LOG


def test_pool_server_url(server, pytestconfig):
    if os.path.exists(BG_SERVER_LOG):
        os.unlink(BG_SERVER_LOG)

    assert not os.path.exists(BG_SERVER_LOG)
    url, client, auth, pool, poolurl, pstore, server_type = server
    assert url.startswith('http://127.0.0.1:9885/fdi/v')
    assert server_type in ['mock', 'live']
    assert pytestconfig.getoption('--server') in ['mock', 'background', 'external']
    print(url, client, pool, server_type)

    res = client.get(url).text
    assert 'docker  pool server' in res
    print(client.get(url).text)
    assert len(pstore.getPools()) == 1

def test_csdb_server_url(csdb_server):
    url, client, auth, pool, poolurl, pstore, server_type = csdb_server
    print(csdb_server)

    res = client.get(url).text
    print(res)
    assert res.endswith('{"code":1,"msg":"Not Permission","total":0}')
    print(res)

    
#def para_server(pc, pytestconfig, new_user_read_write, request):
#    pytestconfig['--server'] = request.param
#    yield server #(pc, pytestconfig, new_user_read_write)
   
#@pytest.mark.server_arch('http')

#@pytest.mark.parametrize("server",[ 'mock','background'], indirect=True)

