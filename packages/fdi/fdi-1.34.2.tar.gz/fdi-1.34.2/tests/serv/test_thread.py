# -*- coding: utf-8 -*-

from serv.test_httppool import getPayload, check_response
from fdi.utils.getconfig import getConfig
from fdi.dataset.deserialize import deserialize
from fdi.dataset.product import Product
from fdi.pns.fdi_requests import safe_client, reqst, get_aio_result

import sys
import json
import os
import time
import pytest
import asyncio
import aiohttp
# from requests_threads import AsyncSession

if sys.version_info[0] >= 3:  # + 0.1 * sys.version_info[1] >= 3.3:
    PY3 = True
else:
    PY3 = False


def setuplogging():
    import logging
    import logging.config
    from .logdict1 import logdict

    # create logger
    logging.config.dictConfig(logdict)
    logging.getLogger("requests").setLevel(logging.WARN)
    logging.getLogger("urllib3").setLevel(logging.WARN)
    logging.getLogger("filelock").setLevel(logging.WARN)
    return logging


logging = setuplogging()
logger = logging.getLogger()

logger.setLevel(logging.INFO)
logger.debug('logging level %d' % (logger.getEffectiveLevel()))

# https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp


@pytest.fixture
def num_pool(tmp_remote_storage_no_wipe, server, client, auth):

    ps, pool = tmp_remote_storage_no_wipe
    aburl, header = server
    poolurl = pool.poolurl
    print(pool.poolname)
    Number = 100
    return aburl, header, pool, poolurl, auth, Number


what_ = pytest.mark.skip


@what_
def xtest_cio_post(num_pool):
    aburl, header, pool, poolurl, auth, Number = num_pool
    pool.removeAll()
    plist = [Product(description=str(i)).serialized() for i in range(Number)]
    urns = []

    start_time = time.time()

    async def m100():
        async with aiohttp.ClientSession() as session:
            tasks = []
            for n in range(len(plist)):
                d = plist[n]
                tasks.append(asyncio.ensure_future(
                    get_aio_result(session.post, poolurl, data=d, headers=header)))

            content = await asyncio.gather(*tasks)
            res = [deserialize(c)['result'] for code, c in content]
            print('pppp', res[0])
            print(len(res))
            return res

    urns = asyncio.run(m100())

    print("--- %s seconds ---" % (time.time() - start_time))
    assert len(urns) == Number
    res = []
    out = ''
    for n in range(Number):
        idx = int(urns[n].rsplit(':', 1)[1])
        out += f"{n} idx={idx} "
    logger.debug(out)
    print('test urn in /tmp/testurn')
    for n in range(Number):
        idx = int(urns[n].rsplit(':', 1)[1])
        out += f"{n} idx={idx} "
    logger.debug(out)
    print('test urn in /tmp/testurn')
    with open('/tmp/testurn', 'w') as f:
        json.dump(urns, f)


def test_cio_post2(num_pool):
    aburl, header, pool, poolurl, auth, Number = num_pool
    pool.removeAll()
    plist = [Product(description=str(i)).serialized() for i in range(Number)]
    urns = []

    start_time = time.time()
    purls = [poolurl] * len(plist)
    urns = reqst('post', apis=purls, data=plist, headers=header, auth=None, no_retry_controls=True)

    print("--- %s seconds ---" % (time.time() - start_time))
    assert len(urns) == Number
    res = []
    out = ''
    for n in range(Number):
        idx = int(urns[n].rsplit(':', 1)[1])
        out += f"{n}: {idx}"
        out += '\n' if n % 10 == 0 else ' '
    logger.debug(out)
    print('test urn in /tmp/testurn')
    with open('/tmp/testurn', 'w') as f:
        json.dump(urns, f)


@what_
def xtest_cio_read(num_pool):
    aburl, header, pool, poolurl, auth, Number = num_pool
    # server url
    urns = []
    try:
        with open('/tmp/testurn', 'r') as f:
            urns = json.load(f)
    except FileNotFoundError:
        urns = [""] * Number

    start_time = time.time()

    async def m100():
        async with aiohttp.ClientSession() as session:
            tasks = []
            for n in range(len(urns)):
                url = aburl+'/'+urns[n]
                tasks.append(asyncio.ensure_future(
                    get_aio_result(session.get, url, headers=header)))

            content = await asyncio.gather(*tasks)
            res = []
            for code, text in content:
                if code != 200:
                    raise RuntimeError(
                        f'AIO {method_name} error {code}: %s' % lls(text, 200))
                res.append(deserialize(text)['result'])
            print('qqqq', type(res[0]))
            print(len(res))
            return res

    res = asyncio.run(m100())
    assert len(urns) == Number
    print("--- %s seconds ---" % (time.time() - start_time))

    for n in range(Number):
        idx = int(urns[n].rsplit(':', 1)[1])
        p = res[n]
        print(f"{n} {p.description} {idx}", end=' ')


def test_cio_read2(num_pool):
    aburl, header, pool, poolurl, auth, Number = num_pool
    # server url
    urns = []
    try:
        with open('/tmp/testurn', 'r') as f:
            urns = json.load(f)
    except FileNotFoundError:
        urns = [""] * Number

    start_time = time.time()

    apis = [aburl+'/'+u for u in urns]
    res = reqst('get', apis=apis, headers=header, auth=None, no_retry_controls=True)

    assert len(urns) == Number
    print("--- %s seconds ---" % (time.time() - start_time))

    out = ''
    for n in range(Number):
        idx = int(urns[n].rsplit(':', 1)[1])
        p = res[n]
        out += f"{n} {p.description} {idx}"
        out += '\n' if n % 10 == 0 else ' '
    logger.debug(out)


def test_cio_remove2(num_pool):
    aburl, header, pool, poolurl, auth, Number = num_pool

    urns = pool.getAllUrns()
    print(f'remove all {len(urns)} urns in a pool with AIO.')
    start_time = time.time()

    apis = [aburl+'/'+u for u in urns]
    res = reqst('delete', apis=apis, headers=header, auth=None, no_retry_controls=True)

    print("--- %s seconds --- %d" % (time.time() - start_time, len(res)))
    assert len(res) == Number
    assert len(pool.getAllUrns()) == 0


def est_threaded_post(num_pool):
    aburl, header, pool, poolurl, auth, Number = num_pool
    pool.removeAll()
    plist = [Product(description=str(i)).serialized() for i in range(Number)]
    # server url
    refs, urns = [], []
    ppath = '/tmp/data/v0.15/test_remote_pool'
    # x = safe_client(client.get, aburl, auth=None)
    from requests_threads import AsyncSession
    session = AsyncSession(n=Number)

    async def p_x100():
        rs = []
        for n in range(Number):
            d = plist[n]
            r = await session.post(poolurl, data=d,
                                   auth=auth, headers=header)
            # urns
            urn = r.json()['result']
            # print(urn)
            rs.append(urn)
            urns.append(urn)
        print(len(rs))  # deserialize(r.content))
        # if os.path.exists(ppath):
        #     files = os.listdir(ppath)
        # else:
        #     files = []
        return rs
    # get pool

    t0 = time.time()
    if 1:
        with pytest.raises(SystemExit):
            for x in session.run(p_x100):
                continue
                print('p', x)
                urns.append(x)
    t1 = time.time()

    print('p_x100', t1-t0)
    assert len(urns) == Number
    with open('/tmp/testurn', 'w') as f:
        json.dump(urns, f)
    # refs.sorted()


def est_threaded_read(num_pool):
    aburl, header, pool, poolurl, auth, Number = num_pool
    try:
        with open('/tmp/testurn', 'r') as f:
            urns = json.load(f)
    except FileNotFoundError:
        return

    from requests_threads import AsyncSession
    session = AsyncSession(n=Number)

    async def r_x100():
        rs = []
        for n in range(len(urns)):
            r = await session.get(aburl+'/'+urns[n], auth=auth, headers=header)
            prod = deserialize(r.content)['result']
            print(n, urns[n], prod.description)
            rs.append(prod)
        return rs

    ta = time.time()
    with pytest.raises(SystemExit):
        for x in session.run(r_x100):
            pass
            prod = deserialize(x.content)
            print(prod)
    tb = time.time()
    print(tb-ta)


def est_rd100(tmp_remote_storage, server, client, auth):

    ps = tmp_remote_storage
    aburl, header = server
    pool = ps.getPool(ps.getPools()[0])
    poolurl = pool.poolurl

    Number = 10
    refs = []

    # x = safe_client(client.get, aburl, auth=None)
    session = AsyncSession(n=Number)
    # get pool

    async def r_x100():
        rs = []
        for n in range(Number):
            rs.append(await session.get(aburl, auth=None))
        print(rs)

    ta = time.time()
    with pytest.raises(SystemExit):
        for x in session.run(r_x100):
            refs.append(x)
            o, code = getPayload(x)
            # check to see if the pool url is malformed
            check_response(o, code=code, failed_case=False, ordered=False)
            # pool name is found
            assert poolname in o['reults']
        tb = time.time()
        print('@@@@ %d %.3f' % (len(refs), tb-ta))
        assert len(refs) == Number
