#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import requests
import pytest
from datetime import datetime
from functools import lru_cache
import time
import json
from fdi.pns.fdi_requests import reqst, ServerError
from fdi.pns.public_fdi_requests import read_from_cloud, load_from_cloud
from fdi.pal.publicclientpool import PublicClientPool
from fdi.utils.tofits import is_Fits
from fdi.utils.common import lls
from fdi.utils.getconfig import getConfig
from serv.test_httppool import getPayload
from fdi.dataset.testproducts import get_demo_product, get_related_product
from fdi.dataset.baseproduct import BaseProduct
from fdi.dataset.product import Product
from fdi.dataset.dateparameter import DateParameter
from fdi.dataset.serializable import serialize
from fdi.pal.context import MapContext
from fdi.pal.urn import parseUrn
from fdi.dataset.arraydataset import ArrayDataset
from fdi.dataset.stringparameter import StringParameter
from fdi.pal.productstorage import ProductStorage
from fdi.dataset.eq import deepcmp
from fdi.pns.jsonio import auth_headers
from fdi.dataset.classes import Classes, Class_Module_Map, Class_Look_Up, get_All_Products

from fdi.pal.poolmanager import dbg_7types
from fdi.testsupport.fixtures import csdb_pool_id, SHORT, make_csdb
# create logger


def setuplogging():
    import logging
    import logging.config
    from . import logdict1

    # create logger
    ld = logdict1.logdict
    for h in ld['handlers'].values():
        h['formatter'] = 'threaded'
    logging.config.dictConfig(ld)
    logging.getLogger("requests").setLevel(logging.WARN)
    logging.getLogger("urllib3").setLevel(logging.WARN)
    logging.getLogger("filelock").setLevel(logging.WARN)
    return logging


logging = setuplogging()
logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
logger.debug('logging level %d' % (logger.getEffectiveLevel()))

pc = getConfig()

# disable these
del_datatype = pytest.mark.skipif(True, reason='del type is bad')
what_wipe = pytest.mark.skipif(0, reason='digging')
no_wipe123 = pytest.mark.skipif(1, reason='keep pool contents')

# markers

# total of 7*N
N = 1
ASYN = 0
""" Use async http """


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "cmp_wipe"
    )

# -------------------TEST CSDB WITH Requests.session a client -----
# low level and not as complete as the later part.


def get_all_prod_types(urllist, client):
    x = client.get(urllist)
    o, code = getPayload(x)
    types = o['data'] if issubclass(o.__class__, dict) else x.text
    return types


def add_a_dataType(full_name, jsn, client, urlup):
    """ not using csdb_client fixture. returns csdb ['data'] result. """
    hdr = {"accept": "*/*"}
    fdata = {"file": (full_name, jsn)}
    data = {"metaPath": "/metadata", "productType": full_name}
    x = reqst(client.post, apis=urlup, files=fdata,
              data=data, headers=hdr)
    return x


asci = False


@lru_cache(maxsize=8)
def cls2jsn(clsn):
    obj = Class_Look_Up[clsn]()
    # return json.dumps(obj.zInfo, ensure_ascii=asci, indent=2)
    return obj.serialized(indent=2)


def XXXest_delete_pool(csdb_server):
    url, client, auth, pool, poolurl, pstore, server_type = csdb_server

    pname = pool._poolname
    urlc = url
    plist = read_from_cloud('listPool', token=pool.token)
    # output example:
    """[{'userId': 3631, 'userName': '...',
     'name': 'test_csdb_fdi11676496230', 'ownerId': '...w',
     'status': 'active',  'createDate': '2023-02-16 05:23:49',
     'groups': ['default'], 'accessLevel': 'public',
     'readPermission': 0, 'writePermission': 0} ...]
    """

    tmplist = [pl['name'] for pl in plist if '11676' in pl['name']]

    sort(tmplist)
    try:
        tmplist.pop()
        tmplist.pop()
    except:
        pass
    res = []
    data = """{
            "endTime": "",
            "page": 1,
            "pageSize": 100,
            "poolName": "",
            "startTime": "",
            "status": ""
        }"""
    for pl in tmplist:
        r = read_from_cloud('wipePool', token=test_pool.token,
                            data=data, poolname=pl, keep=True)

        if r is None:
            logger.info(f'Done deleting pool {pl}')

    plist2 = read_from_cloud('listPool', token=test_pool.token)
    tmplist = [pl['name'] for pl in plist if '11676' in pl['name']]
    sort(tmplist)
    try:
        tmplist.pop()
        tmplist.pop()
    except:
        pass
    assert len(tmplist) == 0


def pool_exists(poolname, urlc, client, create_clean=False):
    x = client.get(urlc+f"/pool/info?storagePoolName={poolname}")
    assert x.status_code == 200
    o, code = getPayload(x)
    if o['code'] == 0:
        if create_clean:
            for u in get_all_in_pool(poolname, what='urn', urlc=urlc, client=client, nulltype=False):
                part = u[3:].replace(':', '/')
                x = client.post(urlc+f'/storage/deleteData?path={part}')
                assert x.status_code == 200, x.text
                o, code = getPayload(x)
                if o['code']:
                    raise RuntimeError(
                        'Cleanin exisiting pool {part} failed.')
        return True
    elif create_clean:
        x = client.post(
            urlc+f"/pool/create?poolName={poolname}&read=0&write=0")
        assert x.status_code == 200
        o, code = getPayload(x)
        return o['code'] == 0
    return o['code'] == 0


def upload_defintion(full_cls, urlcsdb,
                     client=None, check=True, skip=False):
    """ Client level implementation to upload the definition of given class.

    """
    urlupload = urlcsdb + '/datatype/upload'
    urldelete = urlcsdb + '/datatype/'
    urllist = urlcsdb + '/datatype/list'

    if isinstance(full_cls, list):
        alist = True
        fs = full_cls
    else:
        alist = False
        fs = [full_cls]

    # upload
    for f in fs:
        if skip:
            # check type exists
            x = client.get(urllist + '?substring=' + f)
            o, code = getPayload(x)
            if f in o['data']:  # must not "in o['data']" as TC will fall throught due to TCC
                continue
        payload = cls2jsn(f.rsplit('.', 1)[-1])
        r = add_a_dataType(f, payload, client=client, urlup=urlupload)
        assert r.status_code == 200
    if check:
        # check ptypes again
        ptypes = get_all_prod_types(urllist, client)
        # print(types)
        for f in fs:
            assert f in ptypes
    return fs if alist else fs[0]


USE_SV_MODULE_NAME = False
Tx = 'TP' + '_0X'  # + str(datetime.now())


def test_upload_def_Tx(csdb_server):
    """ define a prodect and upload the definition """
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server

    cls = Tx
    if USE_SV_MODULE_NAME:
        cls_full_name = f'sv.{cls}'  # cls_full_name.rsplit('.', 1)[-1]
    else:
        cls_full_name = Class_Module_Map[cls] + '.' + cls
    upload_defintion(cls_full_name, urlcsdb, client=client, check=True)


def test_upload_All_prod_defn(csdb_server):
    """ upload all  product  definition """
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server

    full_names = get_All_Products('Full_Class_Names')
    # full_names = ['fdi.dataset.products.Product']

    upload_defintion(full_names, urlcsdb,
                     client=client)


def upload_prod_data(prd, cls_full_name,
                     desc, obj, obs_id, instr, start, end,
                     level='CL1a', program='GRB', url='',
                     client=None, verify=False, token='',
                     asyn=False, **kwds):
    """ upload product data """

    hdr = client.headers
    hdr.update(kwds.pop('header', {}))
    if issubclass(prd.__class__, BaseProduct):
        prd.description = desc
        prd.instrument = StringParameter(instr)
        prd.version = '0.1'
        prd.startDate = DateParameter(start)
        prd.startDate = DateParameter(end)
        prd.meta['object'] = StringParameter(obj)
        prd.meta['obs_id'] = StringParameter(obs_id)
        prd.level = level
        prd.meta['program'] = StringParameter(program)
        payload = prd.serialized(indent=2)
        content = 'application/json;charset=UTF-8'
    else:
        fitsn = is_Fits(prd)
        if fitsn:
            content = 'application/fits'
        else:
            raise TypeError('unknown type of data.')
        payload = prd

    if 0:
        filen = f'/cygdrive/d/code/tmp/clz/{cls_full_name}.payload'
        with open(filen, 'w+', encoding='utf-8') as f:
            f.write(payload)
        hdr = hdr.update({"accept": "*/*",
                          'X-CSDB-METADATA': '/_ATTR_meta'
                          })
        with open(filen, 'rb') as f:
            fdata = [("file", (filen, f))]
    if 1:

        hdr.update({"accept": "*/*", 'X-CSDB-METADATA': '/_ATTR_meta'})
        hdr['X-AUTH-TOKEN'] = token
        hdr['X-CSDB-AUTOINDEX'] = '1'
        hdr['X-CSDB-METADATA'] = '/_ATTR_meta'
        hdr['X-CSDB-HASHCOMPARE'] = '0'
        tags = {"tags": f'foo,{prd.__class__.__name__},{datetime.now()}'}
        fdata = {'file': ('file',
                          payload,
                          #content,
                          #tags
                          )}
        data = tags
        # url urlupdata = urlcsdb + f'/storage/{pool}/{cls_full_name}'
        # x = client.post(url, files=fdata, data=data, headers=hdr)
        if asyn:
            if 1:
                res = load_from_cloud('uploadProduct', token=token,
                                      products=payload,
                                      path=['/%s/%s' %
                                            tuple(url.rsplit('/', 2)[-2:])],
                                      tags=str(datetime.now()),
                                      resourcetype=cls_full_name,
                                      header=hdr,
                                      content=content,
                                      asyn=True,
                                      **kwds)
                od = res[0]
                assert len(od) > 4
            else:
                x = reqst('post', [url], data=data, headers=hdr,
                          **kwds)
                assert x.status_code == 200, lls(x.text, 500)
        else:
            x = reqst(client.post, url, files=fdata, data=data,
                      headers=hdr, **kwds)
            assert x.status_code == 200, lls(x.text, 500)
            o, code = getPayload(x)
            od = o['data']
            assert o['code'] == 0
        urn = od['urn']
        path = od['path']
        typ = od['dataType']

        if not typ:
            __import__("pdb").set_trace()

            msg = f'{urn} has no dataType. Upload Datatype definition to fix.'
            logger.error(msg)
            raise ValueError(msg)
        logger.debug(f"uploaded product urn={urn} path={path} type={typ}")
        """ output example:
    Example:
    {
      "code": 0,
      "data": {
        "dataType": "string",
        "index": 0,
        "md5": "string",
        "path": "string",
        "size": 0,
        "tags": [
          "string"
        ],
        "timestamp": 0,
        "type": "string",
        "url": "string",
        "urn": "string"
      },
      "msg": "string",
      "total": 0
    }
"""
    if verify:
        # read back
        y = client.get(od['url'])
        assert y.text == payload
        logger.debug('upload verified')
    logger.info('UPLD URN %s' % od['urn'])
    return od


def ddd():
    if 1:
        x = add_a_dataType(cls_full_name, jsn=payload, client=client)
        #### !!!! This throws error !!! ####
        assert x.status_code == 200, x.text
        o, code = getPayload(x)
        assert o['code'] == 0
        assert o['data'] is None


TxFITS = None

@pytest.fixture
def uploadFITS():

    global TxFITS
    global Tx

    prd = get_demo_product()
    Tx = prd.__class__.__name__
    TxFITS = prd.fits()


def test_upload_data_Tx(csdb_server, csdb_token): #, uploadFITS):
    """ upload a Tx prod. definition not auto uploaded"""
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server
    global TxFITS
    pool = csdb_pool_id
    cls = Tx
    if USE_SV_MODULE_NAME:
        cls_full_name = f'sv.{cls}'
    else:
        cls_full_name = Class_Module_Map[cls] + '.' + cls

    logger.debug(f'Upload {cls_full_name} data. Datatype %s found in type list.' % (
        '' if cls_full_name in get_all_prod_types(urlcsdb+ '/datatype/list', client=client) else 'not'))
    urlupdata = urlcsdb + f'/storage/{pool}/{cls_full_name}'
    urn_in_pool_before = get_all_in_pool(poolname=pool,
                                         what='urn',
                                         urlc=urlcsdb,
                                         client=client)
    if  TxFITS:
        prod = TxFITS
    else:
        prod = Class_Look_Up[cls]()

    res = upload_prod_data(prod,
                           cls_full_name=cls_full_name,
                           desc='Demo_Product',
                           obj='3c273',
                           obs_id='b2000a',
                           instr='VT',
                           start='2000-01-01T00:00:00',
                           end='2021-01-01T00:00:00',
                           level='CL2a',
                           program='PPT',
                           url=urlupdata,
                           client=client,
                           verify=True,
                           token=csdb_token,
                           asyn=ASYN
                           )
    urn_in_pool_after = get_all_in_pool(poolname=pool,
                                        what='urn',
                                         urlc=urlcsdb,
                                        client=client)
    diff = set(urn_in_pool_before) ^ set(urn_in_pool_after)
    assert len(diff) == 1
    assert diff.pop() == res['urn']
    logger.debug(f'{cls_full_name} uploaded {res}')




    
def get_all_in_pool(poolname=None, path=None, what='urn', urlc='', client=None, limit=10000, nulltype=True):
    """Return all of something in a pool.

    Parameters
    ----------
    poolname : str
         name of te pool. If both `poolname` and `path` are given, take `poolname`.
    path : str
        part in a path '{poolname}', or '/{poolname}/{product-name}', or
        '{poolname}/{product-name}/{index.aka.serial-number}',
        e.g. '/sv1/sv.BaseProduct'
    what : str
        which item in ['data'] list to return. e.g. 'urn' means a list
        of URNs found in the poolname. 'count' means the length of
        ['data'].
    urlc : str
        path to be prepended before `/storage/searcBy...`.
    client : Session
        requets.Session
    limit : str
        how many items per page maximum.

    Returns
    -------
    list or int
        list of `what` or lenth.

    """
    url = urlc
    if poolname:
        url += f'/storage/searchByPoolOrPath?limitCount={limit}&pool={poolname}'
    else:
        url += f'/storage/searchByPoolOrPath?limitCount={limit}&path={path}'

    x = client.get(url)
    assert x.status_code == 200
    o, code = getPayload(x)
    assert o['code'] == 0
    od = o['data']
    prodList = od if nulltype else [p for p in od if p['dataType']]
    """
  "data": [
    {
      "url": "http://123.56.102.90:31702/csdb/v1/storage/sv1/fdi.dataset.testproducts.TP/22",
      "path": "/sv1/fdi.dataset.testproducts.TP/22",
      "urn": "urn:sv1:fdi.dataset.testproducts.TP:22",
      "timestamp": 1673396754678,
      "tags": [],
      "index": 22,
      "md5": "A69D8B3411999CF25500969B53B691BA",
      "size": 45395,
      "contentType": null,
      "fileName": "fdi.dataset.testproducts.TP",
      "dataType": "fdi.dataset.testproducts.TP"
    }, ...]
    """
    return len(prodList) if what == 'count' else [p[what] for p in prodList]


def test_getDataInfo(csdb_uploaded, csdb_server):  # _uploaded

    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server
    test_pool, uniq, resPrds, pstore = csdb_uploaded
#    r = resPrds
    pname = test_pool.poolname

    # add another prod in pool2
    pool2 = test_pool._poolname + '2'
    cls = 'TCC'
    if USE_SV_MODULE_NAME:
        cls_full_name = f'sv.{cls}'
    else:
        cls_full_name = Class_Module_Map[cls] + '.' + cls
    aip_ctl = add_a_prod_in_another_pool(
        pool2, urlcsdb, cls_full_name, client, nulltype=True)

    assert len(aip_ctl) > 0

    # this only has non-null types
    pinfo = test_pool.getPoolInfo()[pname]

    tget = test_pool.getDataInfo

    # info of all prods in this pool
    dinfo = tget()
    assert dinfo == tget('') == tget(what='', paths='', pool=pname)
    no_nul = tget(nulltype=False)
    # w_nul = test_pool.getCount()
    cnt = test_pool.getPoolInfo(update_hk=False, count=True)
    cp = cnt.get(test_pool._poolname, 0)
    w_nul = cp.get('_urns', 0)
    assert len(no_nul) == w_nul

    # get all URNs in the pool. including nulltype
    urns = tget('urn')
    assert set(urns) >= set(pinfo['_urns'])
    assert set(x['urn'] for x in dinfo) == set(urns)
    # of all pools
    p2urns = tget('urn', pool=pool2)
    assert set(p2urns) == set(aip_ctl)

    # not include null typed. and all pools
    urns2 = tget('urn', paths=cls, pool='', nulltype=False)
    p2urns2 = tget('urn', pool=pool2, nulltype=False)
    p3urns2 = tget('urn', pool=pname+'3', nulltype=False)
    # this may fail if other pools have
    assert set(urns2) >= set(
        u for u in pinfo['_urns'] if cls in u) | set(p2urns2) | set(p3urns2)

    # get info of a URN with a identifying part as `paths`
    if urns2:
        assert tget('', urns2[0][3:].replace(':', '/'))[0]['urn'] == urns2[0]

    # a list of urns: get their index one by one
    urn_test_pool = [x for x in urns2 if pname in x]
    num = min(len(urn_test_pool), 5)
    t0 = time.time()
    ilsns = []
    _urns = urn_test_pool[:num]
    for part in _urns:
        if pname not in part:
            continue
        sn = part.rsplit(':', 1)[-1]
        isn = int(sn)
        assert tget('index', part, nulltype=False)[0] == isn
        ilsns.append([isn])

    logger.info(time.time() - t0)

    # a list of urns: get their indices as a list
    t0 = time.time()
    parts = list(map(lambda x: x[3:].replace(':', '/'), urn_test_pool[:num]))
    # take only the first if multiple are found
    inds = [i[:1] for i in tget('index', parts)]
    # stupid csdb behavior: if sn is 0, sn is not shown.
    # p = [[0] if i == [] else i for i in ilsns]
    p = ilsns
    assert inds == p
    logger.info(f'no asyn get index {time.time() - t0}')

    # a list of urns: fix the pool, get their indices as a list
    t0 = time.time()
    po, dt, sn = parseUrn(urns[:num])
    parts = list(map(lambda x: x[3:].replace(':', '/'), urn_test_pool[:num]))
    # take only the first if multiple are found
    inds = [i[:1] for i in tget('index', parts, asyn=1)]
    logger.info(f'asyn {time.time() - t0}')


@del_datatype
def delDataType( path, csdb_server):
    """ This API deletes all products of the given datatype and the datatype object. """
    urlc, client, auth, test_pool, poolurl, pstore, server_type = csdb_server
    logger.debug('Try storage/delDatatype')
    url = urlc + \
        f"/storage/delDatatype?path=/{path}"
    x = client.delete(url)
    logger.debug('x.text: '+x.text)
    if x.status_code != 200:
        return False
    o, code = getPayload(x)
    assert o['code'] == 0, o['msg']
    return o


@del_datatype
def delete_datatype(urlc, cls_full_name, client):
    """ This API deletes the datatype object of the given datatype. """
    logger.debug('Try delete /v1/datatype/dataType')
    url = urlc + \
        f"/datatype/{cls_full_name}"
    x = client.delete(url)

    logger.debug('x.text: ' + x.text)
    if x.status_code != 200:
        return x.text
    o, code = getPayload(x)
    assert o['code'] == 0, o['msg']
    return o

@del_datatype
def delete_defintion(clsn, full_name, client=None, poolname=None, urlc=None, deldatt=True):
    """delete the definition of a given class.

    Datatypes are not supposed to be deleted frequently. Use upload to update.
    """

    if deldatt:
        pass
    urldelete = urlc + '/datatype/'
    urllist = urlc + '/datatype/list'
    # delDataTypeData failed, usually due to no exisiting products
    res = delete_datatype(urlc, full_name, client=client)
    # gone
    types = get_all_prod_types(urllist, client)
    assert full_name not in types, ''

# @del_datatype


def test_del_def_Tx(csdb_server):
    """ define a product and upload/update the definition. WARNING: not for regular use. """
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server

    assert test_pool.serverDatatypes

    urlc = urlcsdb
    urlupload = urlc + '/datatype/upload'
    urllist = urlc + '/datatype/list'

    ######
    if dbg_7types:
        tl = test_pool.getDataType(substrings='testproducts')
        print('='*21, len(tl), tl)

    cls = Tx
    if USE_SV_MODULE_NAME:
        cls_full_name = f'sv.{cls}'  # cls_full_name.rsplit('.', 1)[-1]
    else:
        cls_full_name = Class_Module_Map[cls] + '.' + cls

    pinfo = test_pool.getPoolInfo()
    pname = test_pool.poolname
    # If type is in, remove it first
    assert test_pool.serverDatatypes
    if cls_full_name in test_pool.serverDatatypes:
        delete_defintion(cls, cls_full_name,
                         client=client, poolname=pname, urlc=urlc, deldatt=True)
    # add type
    jsn = cls2jsn(cls)
    x = add_a_dataType(cls_full_name, jsn=jsn,
                       client=client, urlup=urlupload)
    clz = get_all_prod_types(urllist, client)
    assert cls_full_name in clz
    delete_defintion(cls, cls_full_name,
                     client=client, poolname=pname, urlc=urlc, deldatt=True)
    clz = get_all_prod_types(urllist, client)
    assert cls_full_name not in clz
    #####
    if dbg_7types:
        tl = test_pool.getDataType(substrings='testproducts')
        print('-'*21, len(tl), tl)


@del_datatype
def xxxfollow():
    # add a type and a prod
    x = add_a_dataType(cls_full_name, jsn=jsn,
                       client=client, urlup=urlupload)
    assert cls_full_name in clz
    clz = test_pool.getProductClasses()
    assert cls_full_name in clz
    urlupdata = urlc + f'/storage/{pname}/{cls_full_name}'
    res = upload_prod_data(prod,
                           cls_full_name=cls_full_name,
                           desc='Demo_Product',
                           obj='3c273',
                           obs_id='b2000a',
                           instr='VT',
                           start='2000-01-01T00:00:00',
                           end='2001-01-01T00:00:00',
                           level='CL2a',
                           program='PPT',
                           url=urlupdata,
                           client=client,
                           verify=True
                           )
    assert res['type'] == cls_full_name
    prod_urn = res['urn']
    # Then delete
    with pytest.raises(TypeError):
        delete_defintion(cls, cls_full_name, urllist, urldelete,
                         client=client, urlc=urlc, deldatt=True)
    pinfo = test_pool.getPoolInfo()
    # The prod is still there
    assert prod_urn in pinfo[pname]['_urns']


@ pytest.fixture(scope=SHORT)
def upload_7products(csdb_server, tmp_prods):
    """ Upload a number of products.

    Returns
    -------
    list
       Example `[{'index': 647,
  'md5': '4F15BDC99BFDB1077F5EF80A98924094',
  'path': '/test_csdb_fdi/fdi.dataset.testproducts.TB/647',
  'size': 9838,
  'tags': ['foo', '2023-01-28 11:15:33.938743'],
  'timestamp': 1674875733148,
  'dataType': None,
  'url': 'http://...:31702/csdb/v1/storage/test_csdb_fdi/fdi.dataset.testproducts.TB/647',
  'urn': 'urn:test_csdb_fdi:fdi.dataset.testproducts.TB:647'}, ...]`

    """
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server 

    #####

    
    if dbg_7types:
        tl = test_pool.getDataType(substrings='testproducts')
        print('@'*21, len(tl), tl)

    # 7 products
    prds = tmp_prods

    all_data = []

    for i, prd in enumerate(prds):
        cls = prd.__class__.__name__
        # make full names
        if USE_SV_MODULE_NAME:
            cls_full_name = f'sv.{cls}'  # cls_full_name.rsplit('.', 1)[-1]
        else:
            cls_full_name = Class_Module_Map[cls] + '.' + cls
        urlupdata = urlcsdb + f'/storage/{test_pool.poolname}/{cls_full_name}'
        all_data.append(upload_prod_data(prd,
                                         cls_full_name=cls_full_name,
                                         desc=f'Demo_{cls}',
                                         obj=cls,
                                         obs_id=f'b2000a_{cls_full_name}',
                                         instr='VT',
                                         start='2000-01-01T00:00:00',
                                         end='2001-01-01T00:00:00',
                                         level='CL2a',
                                         program='PPT',
                                         url=urlupdata,
                                         client=client
                                         )
                        )
    return all_data


def test_upload_7products(csdb_upload_7types, upload_7products):
    all_types = csdb_upload_7types
    all_data = upload_7products

    assert len(all_data) == 7
    assert set(d['dataType'] for d in all_data) == {t for t in all_types}


def add_a_prod_in_another_pool(poolname2, urlc, cls_full_name, client, nulltype=True):
    path2 = f'{poolname2}/{cls_full_name}'
    urlupdata = urlc + f'/storage/{path2}'
    cls = cls_full_name.rsplit('.', 1)[1]
    prd = Classes.mapping[cls]()
    pool_exists(poolname2, urlc, client,  create_clean=True)
    jsn = cls2jsn(cls)
    add_a_dataType(cls_full_name, jsn, client, urlc+'/datatype/upload')
    upload_prod_data(prd,
                     cls_full_name=cls_full_name,
                     desc=f'delte_dataType_control',
                     obj='ctrl',
                     obs_id=f'test_ctrl_{cls_full_name}',
                     instr='VT',
                     start='2000-01-01T00:00:00',
                     end='2001-01-01T00:00:00',
                     level='CL2a',
                     program='PPT',
                     url=urlupdata,
                     client=client
                     )
    # number of control prod
    aip_ctl = get_all_in_pool(
        path=f'/{path2}', what='urn', urlc=urlc, client=client,
        nulltype=nulltype
    )
    assert all(cls_full_name in a for a in aip_ctl)
    return aip_ctl


@ pytest.fixture(scope='function')
def get_list(csdb_client, urlcsdb):
    """ list all urns in a pool """

    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server 
    urlc = urlcsdb
    allurns = get_all_in_pool(csdb_pool_id, None, 'urn', urlc, client)
    # logger.info(pformat(allurns))
    return allurns


def test_del_7products(csdb_server, upload_7products):
    """ delete product data from a pool"""

    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server 

    poolname = csdb_pool_id
    data = upload_7products
    urlc = urlcsdb

    l0 = get_all_in_pool(
        path=f'/{poolname}', what='urn', urlc=urlc, client=client)

    # 1 for del one prod; 0 for del all of the type
    del1 = 1
    urns = []
    for dt in data:
        # ‘dataType' in post storage/pool/prod, None in ['type']
        cls_full_name = dt['path'].rsplit('/', 2)[-2]
        ind = dt['index']
        path = f'/{poolname}/{cls_full_name}'
        # not true now:
        # the first urn in aip does not have  ':0' at the end
        # urn = dt['urn'][:-2] if dt['urn'].endswith(':0') else dt['urn']
        urn = dt['urn']

        if del1:  # delete one product
            # number of prod of the same type
            aip = get_all_in_pool(
                path=path, what='urn', urlc=urlc, client=client)
            assert urn in aip
            # delete
            url = urlc + \
                f"/storage/deleteData?path={path}/{ind}"
            x = client.post(url)
            aip = get_all_in_pool(
                path=path, what='urn', urlc=urlcsdb, client=client)
            assert urn not in aip

        else:
            url = urlc + \
                f"/storage/delete?path={path}"
            x = client.post(url)

            if 0:
                # add a prod in a different pool {pool}2
                aip_ctl = add_a_prod_in_another_pool(
                    poolname+'2', urlc, cls_full_name, client)
                # delete from pool 1
                urlxxx = urlc + \
                    f"/storage/delDatatypeData?path=/{poolname}/{cls_full_name}"
                url = urlc + \
                    f"/storage/deleteData?path=/{poolname}/{cls_full_name}{ind}"
                x = client.delete(url)

        assert x.status_code == 200, x.text
        o, code = getPayload(x)
        assert o['code'] == 0, o['msg']
        urns.append(urn)

    # fixture get_list is exhausted so use get_all_in_pool
    l1 = get_all_in_pool(
        path=f'/{poolname}', what='urn', urlc=urlc, client=client)
    assert set(l0) - set(l1) == set(urns)
    assert set(l0) == set(l1) | set(urns)
    if 0:
        aip_ctl2 = get_all_in_pool(
            path=f'/{poolname}2/{cls_full_name}', what='urn', urlc=urlc, client=client)
        # control pool not affected
        assert len(aip_ctl) == len(aip_ctl2)


# ----------------------TEST CSDB WITH ProductStorage----------------


def genProduct(size=1, cls='ArrayDataset', unique='', prod_cls=None):
    res = []
    if prod_cls is None:
        prod_cls = Product
    for i in range(size):
        x = prod_cls(description="product example with several datasets" + unique,
                     instrument="Crystal-Ball", modelName="Mk II", creator='Cloud FDI developer')
        i0 = i
        i1 = [[i0, 2, 3], [4, 5, 6], [7, 8, 9]]
        i2 = 'ev'  # unit
        i3 = 'image1'  # description
        image = ArrayDataset(data=i1, unit=i2, description=i3)
        # put the dataset into the product
        x["RawImage"] = image
        x.set('QualityImage', ArrayDataset(
            [[0.1, 0.5, 0.7], [4e3, 6e7, 8], [-2, 0, 3.1]]))
        res.append(x)
    if size == 1:
        return res[0]
    else:
        return res


def genMapContext(size=1):
    map1 = MapContext(description='product with refs 1')
    map1['creator'] = 'Cloud FDI developer'
    return map1


@ pytest.fixture(scope=SHORT)
def csdb_token(csdb_server):
    logger.info('test token')

    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server    

    token = pc['cloud_token']
    if token and (token != test_pool.token):
        logger.info("Tokens are not equal or not synchronized")
    return test_pool.token


def test_csdb_token(csdb_token):
    tok = csdb_token


def test_verifyToken(csdb_server):
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server

    from fdi.pal.publicclientpool import verifyToken

    tokenMsg = read_from_cloud('getToken', client=client)
    token = tokenMsg['token']
    # verify it

    # success
    v = read_from_cloud('verifyToken', token=token, client=client)
    logger.info('TOKEN fresh')
    assert verifyToken(token, client) == 0
    # empty token
    t = ''
    v = read_from_cloud('verifyToken', token=t, client=client)
    assert 'JWT String argument cannot be null or empty.' in v['message']
    assert verifyToken(t, client) == (1, 'Empty token')
    # invalid format
    t = token[:-5]
    v = read_from_cloud('verifyToken', token=t, client=client)
    assert 'Signature length not correct' in v['message']
    assert verifyToken(t, client) == (2, 'Incorrect format')
    # diff string
    t = token[:-3] + 'zxc'
    v = read_from_cloud('verifyToken', token=t, client=client)
    assert 'JWT signature does not match locally computed signature.' in v['message']
    assert verifyToken(t, client) == (
        3, 'JWT signature does not match locally computed signature.')


def test_csdb_createPool(new_csdb):
    logger.info('test create a brand new pool')
    test_pool, url, pstore = new_csdb
    try:
        pinfo = test_pool.poolInfo[test_pool.poolname]
        assert len(pinfo['_classes']) == 0
    except ValueError:
        # found deleted pool by this name.
        assert test_pool.restorePool() is True
    assert test_pool.poolExists() is True
    try:
        assert test_pool.poolExists('non_existant') is False
    except ServerError as e:
        pass


def test_new_pool(csdb_server):
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server
    url = pc['cloud_scheme'] + \
        urlcsdb[len('csdb'):] + '/' + csdb_pool_id
    # url = pc['cloud_scheme'] + urlcsdb[len('csdb'):] + '/' + csdb_pool_id
    
    ps = make_csdb(url)
    ps.register(poolurl=url, client=client, auth=auth)
    pool = ps.getWritablePool(True)  # PublicClientPool(poolurl=url)
    poolname = pool._poolname
    assert ps.PM.isLoaded(poolname)
    logger.debug('make new {pool._poolurl}')
    #return pool, url, ps


def test_csdb_poolInfo(csdb_server):
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server

    test_pool.getPoolInfo()
    # logger.info(test_pool.poolInfo)


def test_clean_csdb(clean_csdb_fs):
    logger.info('test get classes')
    test_pool, url, pstore = clean_csdb_fs
    pname = test_pool.poolname

    assert len(pstore._pools) == 1
    assert test_pool.poolExists(pname)
    assert test_pool.isEmpty()
    assert test_pool == pstore.getPool(0)

    pinfo = test_pool.getPoolInfo(update_hk=1)
    assert len(pinfo[pname]['_classes'].keys()) == 0
    assert len(pinfo[pname]['_tags'].keys()) == 0
    assert len(pinfo[pname]['_urns'].keys()) == 0


def test_getProductClasses(csdb_server):
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server
    clz = test_pool.getProductClasses()
    # add another prod in pool2
    pool2 = test_pool._poolname + '000'
    cls = 'TP_0X'
    if USE_SV_MODULE_NAME:
        cls_full_name = f'sv.{cls}'
    else:
        cls_full_name = Class_Module_Map[cls] + '.' + cls
    aip_ctl = add_a_prod_in_another_pool(
        pool2, urlcsdb, cls_full_name, client)

    assert len(aip_ctl) > 0
    assert all(cls_full_name not in c for c in clz)
    assert cls_full_name in aip_ctl[-1]


def test_log(csdb_server):
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server
    print(test_pool.log)
    test_pool.poolExists()
    print(test_pool.log)
    print(test_pool.log)
    test_pool.getPoolInfo()
    print(test_pool.log)


@ pytest.fixture(scope=SHORT)
def csdb_upload_7types(csdb_server, tmp_prod_types):
    """
    Returns
    -------
    list
        all full dataType names.
    """

    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server

    # get_all_prod_types(urlcsdb+'/datatype/list', ftest_pool.client)
    # 7 products
    prd_types, seri = tmp_prod_types

    asci = False

    all_7_datatypes = []
    for i, ty in enumerate(prd_types):
        cls = ty.__name__
        # make full names
        if USE_SV_MODULE_NAME:
            full_cls = f'sv.{cls}'  # cls_full_name.rsplit('.', 1)[-1]
        else:
            full_cls = Class_Module_Map[cls] + '.' + cls
        all_7_datatypes.append(full_cls)
    defns = upload_defintion(all_7_datatypes,
                             urlcsdb,
                             client=client, check=1)
    logger.debug(f'Added/updated definition for {defns}.')
    return defns


def test_upload_7types(csdb_server, tmp_prod_types,
                       csdb_upload_7types
                       ):
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server
    alltypes = get_all_prod_types(urlcsdb + '/datatype/list', client)
    clz, seri = tmp_prod_types
    prd_types = [Class_Module_Map[c.__name__] + '.' + c.__name__ for c in clz]

    defns = csdb_upload_7types

    # not-ins
    not_ins = [t for t in prd_types if t not in alltypes]
    print('upload these:', not_ins)
    assert len(prd_types) == len(defns) + len(not_ins)
    assert not not_ins


@ pytest.fixture(scope=SHORT)
def csdb_uploaded(csdb_upload_7types, csdb_server):
    return csdb_up(csdb_upload_7types, csdb_server, asyn=ASYN, ntimes=1)


@ pytest.fixture(scope=SHORT)
def csdb_uploaded_fs(csdb_upload_7types, csdb_server):
    return csdb_up(csdb_upload_7types, csdb_server, asyn=ASYN, ntimes=1)


@ pytest.fixture(scope=SHORT)
def csdb_uploaded_n(csdb_upload_7types, csdb_server):
    return csdb_up(csdb_upload_7types, csdb_server, asyn=ASYN, ntimes=N)


def csdb_up(_csdb_upload_7types, _csdb_server, ntimes, asyn=False):
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = \
        _csdb_server
    poolname = test_pool._poolname

    all7Types = _csdb_upload_7types

    cnt0 = test_pool.getCount()
    logger.info(
        f'To upload all7Types ...count={cnt0}')
    allTypes = test_pool.getDataType()
    for x in all7Types:
        if x not in allTypes:
            logger(f'{x} def missing... {allTypes}')
            assert 0
    t0 = time.time()

    uniq = str(t0)
    resPrds = []
    prds = []
    for i, full_cls in enumerate(all7Types):
        cls = full_cls.rsplit('.', 1)[1]
        ptype = Classes.mapping[cls]
        prds += [ptype(f'demo {cls} {uniq}')] * ntimes

    r = pstore.save(prds, asyn=asyn)
    # assert all(i for i in r), full_cls
    resPrds = r

    n0 = len(resPrds)
    assert n0 == len(all7Types) * ntimes
    # pinfo = test_pool.getPoolInfo()
    logger.info(
        f'Generated in {time.time()-t0} secs n0={n0}, count={test_pool.getCount()}')
    # logger.info(f'{test_pool.getDataInfo("_urns")}')
    return test_pool, uniq, resPrds, pstore



def test_csdb_the_uploaded(csdb_uploaded_fs):
    logger.info('test upload multiple products')
    test_pool, uniq, resPrds, pstore = csdb_uploaded_fs
    r = resPrds

    urninfo = test_pool.getDataInfo('urn')
    assert len(r) == 7
    assert len(urninfo) >= 7

    for ele in resPrds:
        assert csdb_pool_id in ele.urn
        assert ele.urn in urninfo
        assert uniq in ele.product.description

    urnsN7 = [ele.urn for ele in resPrds] * N
    po, pt, sn = parseUrn(urnsN7)
    po = test_pool._poolname
    ures = []
    oldCount = test_pool.getCount()
    assert len(urninfo) >= oldCount

    tags = []
    prds = []
    for n, ref in enumerate([*resPrds] * N):
        tags.append(f'{n} {pt[n]}')
        prds.append(ref.product)
    t0 = time.time()
    if not ASYN:
        for n, ref in enumerate([*resPrds] * N):
            ures.append(pstore.save(prds[n], tag=tags[n],
                        poolname=po))
    else:
        rs = pstore.save(prds, tag=tags, poolname=po, asyn=ASYN)
        ures = rs

    cnt1 = test_pool.getCount()
    assert cnt1 == oldCount + N*7
    logger.info(f'Uploaded in {time.time()-t0} {len(ures)}, curr cnt {cnt1}')


def test_csdb_load_Prd(csdb_uploaded_fs):
    logger.info('test load product')
    # test_pool, url, pstore = csdb

    test_pool, uniq, resPrds, pstore = csdb_uploaded_fs
    pinfo = test_pool.getPoolInfo()
    urns = list(r.urn for r in resPrds)
    us = list(pinfo[test_pool.poolname]['_urns'].keys())
    for u in urns:
        prd = pstore.load(u).product
        assert prd.description.endswith(uniq), 'retrieve production incorrect'


@ pytest.fixture(scope='function')
def csdb_addTag(csdb_uploaded_fs):
    logger.info('test add tag to urn')
    # test_pool, url, pstore = csdb

    test_pool, uniq, resPrds, pstore = csdb_uploaded_fs
    pinfo = test_pool.getPoolInfo(update_hk=True)
    ppu = pinfo[test_pool._poolname]['_urns']
    times = str(int(time.time()))
    tag = 'test_prd_' + times

    # get a tag-free URN
    for u, ts in reversed(ppu.items()):
        if len(ts) == 0:
            break
    urn = u

    assert not test_pool.tagExists(tag)
    test_pool.setTag(tag, urn)
    assert test_pool.tagExists(tag)
    with pytest.raises(AssertionError):
        # default is update.
        assert tag in test_pool.getTags(urn, update=False)
    assert tag in test_pool.getTags(urn)
    # pinfo = test_pool.getPoolInfo()

    # multiple tags
    tag1 = 'test_prd#1_' + times
    tag2 = ['test_prd#2', 'test_prd#3']
    # get a tag-free URn
    start = 0
    for u, ts in reversed(ppu.items()):
        # find the urn that equal to the given urn
        if not start:
            if u == urn:
                start = 1
            continue
        if len(ts) == 0:
            break
    urn2 = u
    assert not test_pool.tagExists(tag1)

    test_pool.setTag(tag1, urn2)
    test_pool.setTag(tag2, urn2)
    tagsall = [tag1] + tag2

    tu2 = test_pool.getTags(urn2)
    assert set(tu2) == set(tagsall)
    # add update=1
    tu2 = test_pool.getTags(urn2, update=True)
    assert set(tu2) == set(tagsall)
    return test_pool, tag, urn, tagsall, urn2


def test_csdb_delTag(csdb_addTag):
    logger.info('test delete a tag')

    test_pool, tag, urn, tag2, urn2 = csdb_addTag
    assert tag in test_pool.getTags(urn)
    tag_urn_map = test_pool.getTagUrnMap()
    assert tag_urn_map is not None

    test_pool.removeTag(tag)

    assert tag not in test_pool.getTags(urn)
    test_pool.getPoolInfo()
    assert tag2[0] in test_pool.getTags(urn2)
    assert tag2[1] in test_pool.getTags(urn2)

    test_pool.removeTag(tag2[1])
    test_pool.getPoolInfo()
    assert tag2[1] not in test_pool.getTags(urn2, update=True)
    assert tag2[0] in test_pool.getTags(urn2)


def test_csdb_count(csdb_uploaded):
    logger.info('test count')
    # test_pool, url, pstore = csdb

    # start with none-empty
    test_pool, uniq, resPrds, pstore = csdb_uploaded
    poolname = test_pool.poolname

    pinfo = test_pool.getPoolInfo()
    for clazz, cld in pinfo[poolname]['_classes'].items():
        cnt = test_pool.getCount(clazz, remote=False)
        assert cnt == \
            len(pinfo[poolname]['_classes'][clazz]['sn'])

    if 0:
        raise ValueError("pool i empty. can't get count()")

    # add prods again.
    prds = Class_Look_Up[clazz.rsplit('.', 1)[-1]]('getCount extra')
    resPrds2 = pstore.save([prds])
    # pinfo = test_pool.getPoolInfo()
    assert len(resPrds2) == 1

    last_cnt = len(pinfo[poolname]['_classes'][clazz]['sn'])
    count = test_pool.getCount(clazz)
    assert count - last_cnt == 1


def test_csdb_remove(csdb_uploaded):
    logger.info('test remove product')
    # test_pool, url, pstore = csdb
    test_pool, uniq, resPrds, pstore = csdb_uploaded
    poolname = test_pool.poolname
    pinfo = test_pool.getPoolInfo()
    cls = resPrds[0].getType().__name__

    # test remove with URN
    if USE_SV_MODULE_NAME:
        cls_full_name = f'sv.{cls}'
    else:
        cls_full_name = Class_Module_Map[cls] + '.' + cls
    rdIndex = pinfo[poolname]['_classes'][cls_full_name]['sn'][-1]
    urn = 'urn:' + csdb_pool_id + ':' + cls_full_name + ':' + str(rdIndex)
    res = test_pool.remove(urn)
    assert res == 0, res
    pinfo = test_pool.getPoolInfo()
    assert cls_full_name not in pinfo[poolname]['_classes'] or rdIndex not in pinfo[poolname]['_classes'][cls_full_name]['sn']
    # test pstore
    urn = list(pinfo[poolname]['_urns'])[-1]
    res = pstore.remove(urn)
    assert res == 0, res
    pinfo = test_pool.getPoolInfo()
    assert urn not in pinfo[poolname]['_urns']


NWIPE = N


@ no_wipe123
def test_csdb_wipe_(csdb_uploaded_n, csdb_server):

    logger.info('test wipe all')
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server
    test_pool, uniq, resPrds, pstore = csdb_uploaded_n
    pname = test_pool.poolname

    if 1:
        oldCount = test_pool.getCount()
        n0 = oldCount  # , NWIPE*7)
        logger.info(f'wipe setup {n0}')
        t0 = time.time()
        path = f"/{pname}"
        rec = test_pool.removeAll()

    elif 0:
        tyinfo = test_pool.getProductClasses(count=True)
        assert tyinfo
        assert isinstance(tyinfo, set), str(tyinfo)
        pinfo = test_pool.getPoolInfo(update_hk=True)
        # logger.info(list(pinfo[pname]['_urns'])[-8:])

        oldCount = sum(test_pool.getCount(typename=t, update=False)
                       for t in tyinfo)
        n0 = oldCount  # , NWIPE*7)
        logger.info(f'wipe setup, {n0}')
        t0 = time.time()

        # first not delDataTypeData
        for cls in tyinfo:
            path = f"/{pname}/{cls}"
            res = read_from_cloud('delDataTypeData', token=test_pool.token,
                                  path=path)
        # test_pool.removeAll(ignore_error=True)
    newCount = test_pool.getCount()
    assert newCount == 0
    logger.info(f'>>> {time.time()-t0} {oldCount} -> {newCount}')


@ what_wipe
def test_cmp_wipe1(csdb_server, csdb_uploaded_n):
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server
    test_pool, uniq, resPrds, pstore = csdb_uploaded_n
    
    pname = test_pool.poolname
    info = test_pool.getPoolInfo(update_hk=True)
    assert isinstance(info, dict), str(info)
    oldCount = test_pool.getCount()
    assert oldCount
    n0 = len(info[pname]['_urns'])
    logger.info(f'wipe setup {n0}, {oldCount}')
    t0 = time.time()

    for clazz, cld in info[pname]['_classes'].items():
        # all datatypes
        # types = get_all_prod_types(urllist, client)
        # assert clazz in types
        path = f'/{pname}/{clazz}'
        res = read_from_cloud('delDataTypeData', token=test_pool.token,
                              path=path)
    logger.info(
        f"delDataTypeData, >>> {time.time()-t0}, {n0}, {len(info[pname]['_urns'])}")
    assert test_pool.getCount() == 0


DTYPE = 'fdi.dataset.testproducts.TP'

ONLY_IN_test_pool = True
""" products of this type are going to be removed in test_pool, not all csdb storage."""

if ONLY_IN_test_pool:
    @ pytest.mark.skip
    def test_cmp_wipe2(csdb, csdb_client, csdb_uploaded_n):
        wipe_all(_csdb_client=csdb_client,
                 _csdb_uploaded_n=csdb_uploaded_n)
else:
    @ what_wipe
    def test_wipe_urns(csdb, csdb_client):
        wipe_all(_csdb_client=csdb_client, _csdb=csdb)


@ no_wipe123
def wipe_all(_csdb_server,_csdb_uploaded_n=None):
    # products of this type are going to be removed in csdb storage.

    if ONLY_IN_test_pool:
        test_pool, uniq, resPrds, pstore = _csdb_uploaded_n
    else:
        urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = _csdb_server
    urlc, client = _csdb_client
    if ONLY_IN_test_pool:
        pname = test_pool.poolname
        test_pool._poolname = pname
        info = test_pool.getPoolInfo()

        oldCount = test_pool.getCount()
        assert oldCount
        assert isinstance(info, dict), str(info)
        urns = info[pname]['_urns']
        assert len(urns) == oldCount
    else:
        path_part = DTYPE
        _all = get_all_in_pool(
            poolname=None, path=path_part, what='urn', urlc=urlc, client=client
        )
        urns = [u for u in _all if DTYPE in u]
        oldCount = len(urns)
    n0 = min(len(urns), NWIPE*7)
    prompt = f'wipe setup, {n0}, {lls(urns, 300)}'
    print(prompt)
    logger.info(prompt)
    pp = input(f'wipe2 {n0} URNs?')
    if len(urns) > 999:
        urns = urns[:999]
    t0 = time.time()
    res = test_pool.remove(list(urns), asyn=ASYN)
    msg = f'urn >>> {time.time()-t0}, n0={n0}, len={len(urns)}'
    logger.info(mssg)
    newCount = max(oldCount - n0, 0)
    assert test_pool.getCount() == newCount

    ##########


@ no_wipe123
def test_cmp_wipe3(csdb_server, csdb_uploaded_n):
    
    urlcsdb, client, auth, test_pool, poolurl, pstore, server_type = csdb_server
    test_pool, uniq, resPrds, pstore = csdb_uploaded_n

    pname = test_pool.poolname
    test_pool._poolname = pname
    info = test_pool.getPoolInfo()
    oldCount = test_pool.getCount()
    assert oldCount

    n0 = min(oldCount, NWIPE*7)
    logger.info(f'wipe setup, {n0}.')
    t0 = time.time()
    test_pool.ignore_error_when_delete = True
    res = test_pool.wipe()
    logger.info(
        f"'class-sn', >>> {time.time()-t0}, {n0}, {len(info[pname]['_urns'])}")
    newCount = max(oldCount - n0, 0)
    assert test_pool.getCount() == newCount
