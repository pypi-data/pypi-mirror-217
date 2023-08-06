# -*- coding: utf-8 -*-
from ..pns.fdi_requests import (ServerError,
                                save_to_server,
                                read_from_server,
                                delete_from_server,
                                post_to_server
                                )
from ..dataset.serializable import serialize
from ..dataset.deserialize import deserialize, serialize_args
from ..dataset.classes import All_Exceptions
from .poolmanager import PoolManager, save_cookies
from .productref import ProductRef
from .productpool import ProductPool
from ..httppool.session import requests_retry_session

from .dicthk import HKDBS, get_missing
from ..utils.common import trbk, lls, fullname
from .urn import Urn, makeUrn

import requests

import os
import builtins
from itertools import chain
from functools import lru_cache
from os import path as op
import logging
# create logger
logger = logging.getLogger(__name__)
# logger.debug('level %d' %  (logger.getEffectiveLevel()))


def writeJsonwithbackup(fp, data):
    """ write data in JSON after backing up the existing one.
    """
    if op.exists(fp):
        os.rename(fp, fp + '.old')
    js = serialize(data)
    with open(fp, mode="w+") as f:
        f.write(js)


def toserver(self, method, *args, **kwds):
    # if method == 'select':
    #    __import__('pdb').set_trace()

    apipath = serialize_args(method, *args, not_quoted=self.not_quoted, **kwds)
    urn = 'urn:::0'  # makeUrn(self._poolname, typename, 0)

    logger.debug("toServer ==> " + urn)
    if len(apipath) < 80:
        code, res, msg = read_from_server(
            urn, self._poolurl, apipath, auth=self.auth, client=self.client)
    else:
        apipath = serialize([args, kwds])
        code, res, msg = post_to_server(apipath, urn, self._poolurl,
                                        contents=method + '__' + '/',
                                        no_serial=True,
                                        auth=self.auth, client=self.client)

    save_cookies(self.client)

    if issubclass(res.__class__, str) and 'FAILED' in res or code != 200:
        for line in chain(msg.split('.', 1)[:1], msg.split('\n')):
            excpt = line.split(':', 1)[0]
            if excpt in All_Exceptions:
                # relay the exception from server
                except_cls = All_Exceptions[excpt]
                kw = {'code': code} if issubclass(
                    except_cls, ServerError) else {}
                raise except_cls(f'SERVER: Code {code} Message: {msg}', **kw)
        raise ServerError(
            f'Executing {method} failed. SERVER: Code {code} Message: {msg}', code=code)

    return res


def toServer(method_name=None):
    """ decorator to divert local calls to server and return what comes back.

    """
    def inner(*sf):
        """ [self], fun """
        fun = sf[-1]

        def wrapper(*args, **kwds):
            return toserver(args[0],
                            method_name if method_name else fun.__name__,
                            *args[1:],
                            **kwds)
        return wrapper
    return inner


class HttpClientPool(ProductPool):
    """ the pool will save all products on a remote server.
    """

    def __init__(self, auth=None, client=None, **kwds):
        """Initialize connection to the remote server.

        Sreates file structure if there isn't one. if there is, read
        and populate house-keeping records. create persistent files on
        server if not exist.

        Parameters
        ----------
        auth : tuple, HTTPBasicAuth, or Authorization
            Authorization for remote pool.
        client : Request or Wrapper
            Mainly used for testing with mock server.
        **kwds :

        Returns
        -------


        """

        # print(__name__ + str(kwds))
        super().__init__(**kwds)
        self.not_quoted = True
        self.auth = auth
        if client is None:
            client = requests_retry_session()
        self.client = client

    def setup(self):
        """ Sets up HttpPool interals.

        Make sure that self._poolname and self._poolurl are present.
        """

        if super().setup():
            return True

        return False

    get_missing = get_missing

    # @toServer()
    def readHK(self, hktype=None, serialize_out=False):
        """
        loads and returns the housekeeping data.

        `hktype` has been taken care of by the serverside.
        """
        poolname = self._poolname
        logger.debug("READ HK FROM REMOTE===>poolurl: " + poolname)
        hk = {}
        code = None
        try:
            code, r, msg = read_from_server(
                None, self._poolurl, 'housekeeping', client=getattr(self, 'client', None))
            if r != 'FAILED' and code == 200:
                hk = r
        except Exception as e:
            msg = 'Reading %s failed. %s ' % (
                poolname, 'No code' if code is None else str(code)) + str(e) + trbk(e)
            r = 'FAILED'

        if r == 'FAILED':
            logger.error(msg)
            raise Exception(msg)
        return json.dumps(hk) if serialize_out else hk

    def schematicSave(self, products, tag=None, geturnobjs=False, serialize_out=False, asyn=False, **kwds):
        """
        does the media-specific saving to remote server.
        """

        alist = issubclass(products.__class__, list)
        if not alist:
            productlist = [products]
        else:
            productlist = products

        if len(productlist) == 0:
            return []
        # only type and poolname in the urn will be used
        urn = makeUrn(typename=fullname(productlist[0]),
                      poolname=self._poolname, index=0)
        first = True
        sized = '['
        for prd in productlist:
            sp = serialize(prd)
            sized += '%s %d, %s' % ('' if first else ',', len(sp), sp)
            first = False
        sized += ']'
        res = save_to_server(sized, urn, self._poolurl,
                             tag, no_serial=True,
                             auth=self.auth, client=self.client)
        sv = deserialize(res.text)
        if sv['result'] == 'FAILED' or res.status_code != 200:
            logger.error('Save %d products to server failed.%d Message from %s: %s' % (
                len(productlist), res.status_code, self._poolurl, sv['msg']))
            raise ServerError(sv['msg'])
        else:
            urns = sv['result']
        logger.debug('Product written to remote server successful')
        res = []
        if geturnobjs:
            if serialize_out:
                # return the URN string.
                res = urns
            else:
                res = [Urn(urn=u, poolurl=self._poolurl) for u in urns]
        else:
            for u, prd in zip(urns, productlist):
                if serialize_out:
                    rf = ProductRef(urn=Urn(urn=u, poolurl=self._poolurl),
                                    poolname=self._poolname)
                    # return without meta
                    res.append(rf)
                else:
                    # it seems that there is no better way to set meta
                    rf = ProductRef(urn=Urn(urn=u, poolurl=self._poolurl),
                                    poolname=self._poolname, meta=prd.getMeta())
                    res.append(rf)
        logger.debug('%d product(s) generated %d %s: %s.' %
                     (len(productlist), len(res), 'Urns ' if geturnobjs else 'prodRefs', lls(res, 200)))
        if alist:
            return serialize(res) if serialize_out else res
        else:
            return serialize(res[0]) if serialize_out else res[0]

    def schematicLoad(self, resourcetype, index, start=None, end=None,
                      serialize_out=False):
        """
        does the scheme-specific part of loadProduct.
        """
        indexstr = str(index)
        poolname = self._poolname
        urn = makeUrn(self._poolname, resourcetype, indexstr)
        logger.debug("READ PRODUCT FROM REMOTE===> " + urn)
        code, res, msg = read_from_server(
            urn, self._poolurl,
            auth=self.auth, client=self.client)  # TODO: start,end
        if res == 'FAILED' or code != 200:
            raise NameError('Loading ' + urn + ' failed:%d. ' % code + msg)
        return res

    def schematicRemove(self, urn=None, resourcetype=None, index=None, asyn=False, **kwds):
        """
        does the scheme-specific part of removal.

        urn or (resourcetype, index)
        """
        urn, datatype, sn = self.get_missing(
            urn, resourcetype, index, no_check=True)
        _u = urn
        if isinstance(_u, list):
            urns = _u
            alist = True
        else:
            urns = [_u]
            alist = False
        rs = []
        for u in urns:
            r, msg = delete_from_server(
                u, self._poolurl, auth=self.auth, client=self.client,
                asyn=False, **kwds)
            if r == 'FAILED':
                msg = 'Remove from server ' + self._poolname +\
                    ' failed. Caused by: ' + msg
                if getattr(self, 'ignore_error_when_delete', False):
                    logger.warning(msg)
                else:
                    raise RuntimeError(msg)
            rs.append(r)
        return rs if alist else rs[0]

    # def doWipe(self):
    #     """
    #     does the scheme-specific wiping.
    #     """

    #     res, msg = delete_from_server(
    #         None, self._poolurl, 'pool', client=self.client,
    #         asyn=asyn, **kwds)
    #     if res == 'FAILED':
    #         if getattr(self, 'ignore_error_when_delete', False):
    #             logger.warning(msg)
    #         else:
    #             raise Exception(msg)
    #     return res

    @ toServer()
    def wipe(self):
        """
        Remove all pool data (self, products) and all pool meta data (self, descriptors, indices, etc.).

        Pool is still left registered to ProductStorage and PoolManager.
        """

    removeAll = wipe

    @ toServer(method_name='select')
    def schematicSelect(self,  query, results=None):
        """
        Returns a list of references to products that match the specified query.
        """
        # return self.toserver('select', query, results=results)

    @ toServer()
    def dereference(self, ref):
        """
        Decrement the reference count of a ProductRef.
        """

        # return self.toserver('dereference', ref)

    @ toServer()
    def exists(self, urn):
        """
        Determines the existence of a product with specified URN.
        """

        # return self.toserver('exists', urn)

    @ toServer()
    def getAllUrns(self):
        """
        Return all URNs in the remote pool.
        """
        raise NotImplementedError

    @ toServer()
    def getPoolpath(self):
        """
        Returns poolpath of the server pool, if available.
        """

    @ toServer()
    def getCacheInfo(self):
        """
        Returns lru cache usage information of the server pool, if available.
        """

    @ toServer()
    def getProductClasses(self):
        """
        Returns all Product classes found in this pool.
        mh: returns an iterator.
        """
        # return self.toserver('getProductClasses')

    @ toServer()
    def getReferenceCount(self, ref):
        """
        Returns the reference count of a ProductRef.
        """
        return self.toserver('getReferenceCount', ref)

    @ toServer()
    def isAlive(self):
        """
        Test if the pool is capable of responding to commands.
        """
        # return self.toserver('isAlive')

    @ toServer()
    def isEmpty(self):
        """
        Determines if the pool is empty.
        """

        # return self.toserver('isEmpty')

    def meta(self,  urn):
        """
        Loads the meta-data belonging to the product of specified URN.
        """

        # return self.toserver('meta', urn)

    @ toServer()
    def reference(self, ref):
        """
        Increment the reference count of a ProductRef.
        """
        # return self.toserver('reference', ref)

    @ toServer()
    def getCount(self, typename=None):
        """
        Return the number of URNs for the product type.
        """
        # return self.toserver('getCount', typename)

    @ toServer()
    def getTags(self, urn=None):
        """
        Get all of the tags that map to a given URN.
        Get all known tags if urn is not specified.
        mh: returns an iterator.
        """
        raise NotImplementedError

    @ toServer()
    def getTagUrnMap(self):
        """
        Get the full tag->urn mappings.
        mh: returns an iterator
        """
        raise NotImplementedError

    @ toServer()
    def getUrn(self, tag):
        """
        Gets the URNs corresponding to the given tag. Returns an empty list if tag does not exist.
        """
        raise NotImplementedError

    @ toServer()
    def getUrnObject(self, tag):
        """
        Gets the URNobjects corresponding to the given tag.
        """
        raise NotImplementedError

    @ toServer()
    def removekey(self, key, themap, thename, othermap, othername):
        """
        Remove the given key.
        """
        raise NotImplementedError

    @ toServer()
    def removeTag(self, tag):
        """
        Remove the given tag from the tag and urn maps.
        """
        raise NotImplementedError

    @ toServer()
    def removeUrn(self, urn):
        """
        Remove the given urn from the tag and urn maps.
        """
        raise NotImplementedError

    @ toServer()
    def removeTag(self, tag):
        """
        Remove the given tag from the urn and urn maps.
        """
        raise NotImplementedError

    @ toServer()
    def setTag(self, tag,  urn):
        """
        Sets the specified tag to the given URN.
        """
        raise NotImplementedError

    @ toServer()
    def tagExists(self, tag):
        """
        Tests if a tag exists.
        """
        raise NotImplementedError

    @ toServer()
    def backup(self):
        """
        Returns a string of a tar file image of the remote pool.
        """
        raise NotImplementedError

    @ toServer()
    def restore(self, tar):
        """
        Restore the remote pool with the contents of the named tar file.
        """
        raise NotImplementedError

    @ toServer()
    def where(self, qw, prod='BaseProduct', urns=None):
        """
        AbstractQuery convenience api with 'p' for the product.
        """
        raise NotImplementedError

    @ toServer()
    def qm(self, qw, prod='BaseProduct', urns=None):
        """
        MetaQuery convenience api with 'm' for 'meta'..
        """
        raise NotImplementedError

#


def serialize_args1(*args, **kwds):
    def mkv(v):
        t = type(v).__name__
        if t in vars(builtins):
            vs = str(v) + ':' + t
        else:
            vs = serialize(v)+':' + t
        return vs
    argsexpr = list(mkv(v) for v in args)
    kwdsexpr = dict((str(k), mkv(v)) for k, v in kwds.items())
    return '/'.join(chain(('|'.join(argsexpr),), chain(*kwdsexpr)))


def parseApiArgs1(all_args, serialize_out=False):
    """ parse the command path to get positional and keywords arguments.

    all_args: a list of path segments for the args list.
    """
    lp = len(all_args)
    args, kwds = [], {}
    if lp % 2 == 1:
        # there are odd number of args+key+val
        # the first seg after ind_meth must be all the positional args
        try:
            tyargs = all_args[0].split('|')
            for a in tyargs:
                print(a)
                v, c, t = a.rpartition(':')
                args.append(mkv(v, t))
        except IndexError as e:
            code, result, msg = excp(
                e,
                msg='Bad arguement format ' + all_args[0],
                serialize_out=serialize_out)
            logger.error(msg)
            return code, result, msg
        kwstart = 1
    else:
        kwstart = 0
    # starting from kwstart are the keyword arges k1|v1 / k2|v2 / ...

    try:
        while kwstart < lp:
            v, t = all_args[kwstart].rsplit(':', 1)
            kwds[all_args[kwstart]] = mkv(v, t)
            kwstart += 2
    except IndexError as e:
        code, result, msg = excp(
            e,
            msg='Bad arguement format ' + str(all_args[kwstart:]),
            serialize_out=serialize_out)
        logger.error(msg)
        return code, result, msg

    return 200, args, kwds
