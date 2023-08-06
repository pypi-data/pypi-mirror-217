# -*- coding: utf-8 -*-

from .productpool import PoolNotFoundError
from ..utils.common import pathjoin, trbk, find_all_files, wipeLocal
from .dicthk import HKDBS
from .urn import makeUrn, Urn, parseUrn
from ..dataset.deserialize import deserialize
from .managedpool import ManagedPool, MetaData_Json_Start, MetaData_Json_End


import tarfile
from functools import lru_cache
import sys
import mmap
import io
import os
from os import path as op
import logging
# create logger
logger = logging.getLogger(__name__)
# logger.debug('level %d' %  (logger.getEffectiveLevel()))

if sys.version_info[0] >= 3:  # + 0.1 * sys.version_info[1] >= 3.3:
    PY3 = True
    strset = str
    from urllib.parse import urlparse, quote, unquote
else:
    PY3 = False
    strset = (str, unicode)
    from urlparse import urlparse, quote, unquote


class LocalPool(ManagedPool):
    """ the pool will save all products in local computer.

    Parameters
    ----------
        makenew : bool
             when the pool does not exist, make a new directory (`True`;
             default) or throws `PoolNotFoundError` (`False`).

    """

    def __init__(self, **kwds):
        """ creates data structure structure if there isn't one. if there is, read and populate house-keeping records. create persistent files if not exist.


        """
        # print(__name__ + str(kwds))
        super().__init__(**kwds)

    def setup(self):
        """ Sets up LocalPool interals.

        Make sure that self._poolname and self._poolurl are present.
        """

        if super().setup():
            return True

        real_poolpath = self.real_poolpath = self.transformpath(self._poolname)
        #print('%%%%%%%%%%%% '+real_poolpath+str(self._make_new))

        self.make_new()
        
        if not op.exists(real_poolpath):
            raise PoolNotFoundError(
                'poolname: %r poolurl: %r real_poolpath: %r' % (
                    self._poolname, self._poolurl, real_poolpath))

        self._files = {}
        self._atimes = {}
        self._cached_files = {}

        dTypes, dTags = tuple(self.readHK().values())

        logger.debug(
            f'created {self.__class__.__name__} {self._poolname}at {real_poolpath} HKs read.')

        # new ####
        if len(self._dTypes) or len(self._dTags):
            raise ValueError('self._dTypes or self._dTags not empty %s %s' % (
                str(self._dTypes), str(self._dTags)))

        self._dTypes.update(dTypes)
        self._dTags.update(dTags)
        # /new ###

        if any(not op.exists(op.join(real_poolpath, hk+'.jsn'))
               for hk in HKDBS):
            self.writeHK()
        return False

    def readmmap(self, filename, start=None, end=None, close=False, check_time=False):
        fp = op.abspath(filename)
        if check_time:
            sr = os.stat(fp)
            if fp in self._atimes and (sr.st_mtime_ns <= self._atimes[fp]):
                # file hasnot changed since last time we read/wrote it.
                return None
        try:
            if 1:  # if fp not in self._files or self._files[fp] is None:
                file_obj = open(fp, mode="r+", encoding="utf-8")
                mmap_obj = mmap.mmap(
                    file_obj.fileno(), length=0, access=mmap.ACCESS_READ)
                fo = mmap_obj
            else:
                fo = self._files[fp]
            if start is None:
                js = fo.read()
            else:
                fo.seek(start)
                js = fo.read(end - start)
        except Exception as e:
            msg = 'Error in HK reading. file: %s. exc: %s trbk: %s.' % (
                fp, str(e), trbk(e))
            logging.error(msg)
            raise KeyError(msg)
        if 1:  # close:
            fo.close()
            if fp in self._files:
                del self._files[fp]
        else:
            self._files[fp] = fo
        if check_time:
            # save the mtime as the self atime
            self._atimes[fp] = sr.st_mtime_ns
        return js.decode('ascii')

    def readHK(self, hktype=None, serialize_out=False, all_versions=True):
        """
        loads and returns the housekeeping data, or empty `dict` if not found.

        hktype: one of the mappings listed in `dicthk.HKDBS`.
        serialize_out: if True return serialized form. Default is false.
        """
        if hktype is None:
            # some new ####
            hks = HKDBS
        else:
            hks = [hktype]
        fp0 = self.transformpath(self._poolname)

        hk = {}
        for hkdata in hks:
            fp = op.abspath(pathjoin(fp0, hkdata + '.jsn'))
            if op.exists(fp) and (all_versions or ('dT' in fp)):
                js = self.readmmap(fp, check_time=True)
                if js:
                    if serialize_out:
                        r = js
                    else:
                        from ..dataset.deserialize import deserialize
                        r = deserialize(js, int_key=True)
                    self._cached_files[fp] = js
                else:
                    # the file hasnot changed since last time we r/w it.
                    r = self._cached_files[fp] if serialize_out else \
                        self.__getattribute__('_' + hkdata)
            else:
                if serialize_out:
                    r = '{}'  # '{"_STID":"ODict"}'
                else:
                    from ..dataset.odict import ODict
                    r = {}  # ODict()
            hk[hkdata] = r
        logger.debug('HK read from ' + fp0)
        if serialize_out:
            return '{%s}' % ', '.join(('"%s": %s' % (k, v) for k, v in hk.items())) if hktype is None else hk[hktype]
        else:
            return hk if hktype is None else hk[hktype]

    def writeJsonmmap(self, fp, data, serialize_in=True, serialize_out=False, close=False, check_time=False, meta_location=False, **kwds):
        """ write data in JSON from mmap file at fp.

        register the file. Leave file open by default `close`.
        data: to be serialized and saved.
        serialize_out: if True returns contents in serialized form.
        :check_time: to check if file has not been written since we did last time. Default `False`.
        :meta_location: return the start and end offsets of metadata in data JSON.  Default `False`.
        :return:
        int bytes written. If `meta_location` is ```True```, adding int int start and end point offsets of metadata in seriaized data.
        """
        from ..dataset.serializable import serialize
        js = serialize(data, **kwds) if serialize_in else data
        # start = end = None
        if meta_location:
            # locate metadata
            start = js.find(MetaData_Json_Start, 0)
            # make end relative to file start
            end = js.find(MetaData_Json_End, start) + start
            start += len(MetaData_Json_Start)
            end += len(MetaData_Json_End)

        fp = op.abspath(fp)
        if 1:  # fp not in self._files or self._files[fp] is None:
            file_obj = open(fp, mode="w+", encoding="utf-8")
            # with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
        else:
            file_obj = self._files[fp]
        file_obj.seek(0)

        # file_obj.resize(len(js))
        file_obj.truncate(0)
        file_obj.write(js)
        # file_obj.flush()
        close = 1
        if close:
            file_obj.close()
            if fp in self._files:
                del self._files[fp]
        else:
            self._files[fp] = file_obj
        if check_time:
            # save the mtime as the self atime
            sr = os.stat(fp)
            os.utime(fp, ns=(sr.st_atime_ns, sr.st_mtime_ns))
            self._atimes[fp] = sr.st_mtime_ns
            self._cached_files[fp] = js
        l = len(js)
        logger.debug('JSON saved to: %s %d bytes' % (fp, l))
        if meta_location:
            return l, start, end
        else:
            return l

    def writeHK(self, fp0=None, all_versions=True):
        """ save the housekeeping data to disk
        """

        if fp0 is None:
            fp0 = self.transformpath(self._poolname)
        l = 0
        for hkdata in HKDBS:
            if not all_versions and not 'dT' in hkdata:
                continue
            fp = pathjoin(fp0, hkdata + '.jsn')
            l += self.writeJsonmmap(fp, self.__getattribute__('_' + hkdata),
                                    check_time=True)
        logger.debug('=== '+str(self._dTypes))
        return l

    def make_new(self, path=None):
        """ make a new directory.

        Parameters
        ----------
            path: str
                default `real_poolpath`
        """
        if path is None:
            path = self.real_poolpath
        os.makedirs(path, mode=0o755, exist_ok=True)
        # print(os.stat(self.real_poolpath))
        # assert os.stat(path)
        
    def setMetaByUrn(self, start, end, urn=None, datatype=None, sn=None):
        """
        Sets the location of the meta data of the specified data to the given URN or a pair of data type and serial number.

        :data: usually serialized Product.
        """
        u, datatype, sn = self.get_missing(
            urn=urn, datatype=datatype, sn=sn, no_check=True)
        # char offset of the start and end points of metadata
        if start >= 0 and end > 0:
            mt = [start, end]
        else:
            mt = [None, None]
        # new ##
        self._dTypes[datatype]['sn'][sn]['meta'] = mt
        # self._urns[u]['meta'] = mt

    @ lru_cache(maxsize=1024)
    def getMetaByUrnJson(self, urn, resourcetype, index):
        """ like `getMetaByUrn` but returns un-deserialized form."""

        urn, datatype, sn = self.get_missing(
            urn=urn, datatype=resourcetype, sn=index)
        # deserialize(prd[start+len(MetaData_Json_Start):end+len(MetaData_Json_End)])
        try:
            # new ##
            # assert tuple(self._urns[urn]['meta']) == \
            # tuple(self._dTypes[datatype]['sn'][sn]['meta'])
            start, end = tuple(self._dTypes[datatype]['sn'][sn]['meta'])
            # start, end = tuple(self._urns[urn]['meta'])
        except KeyError as e:
            msg = f"Trouble with {self._poolname}...['meta']"
            logger.debug(msg)
            raise
        js = self.schematicLoad(resourcetype=datatype,
                                index=sn, start=start, end=end,
                                serialize_out=True)

        return js

    def getCacheInfo(self):
        info = super().getCacheInfo()
        for i in ['getMetaByUrnJson']:
            info[i] = getattr(self, i).cache_info()

        return info

    def getMetaByUrn(self, urn, resourcetype=None, index=None):
        """ 
        Get all of the meta data belonging to a product of a given URN or a pair of data type and serial number.

        mh: returns an iterator.
        """
        m = self.getMetaByUrnJson(urn, resourcetype=resourcetype,
                                  index=index)
        return deserialize(m)  # self._urns[urn]['meta']

    def doSave(self, resourcetype, index, data, tags=None, serialize_in=True, **kwds):
        """
        does the media-specific saving.

        index: int
        """

        fp0 = self.transformpath(self._poolname)
        fp = pathjoin(fp0, quote(resourcetype) + '_' + str(index))
        try:
            # t0 = time.time()
            l, start, end = self.writeJsonmmap(
                fp, data, serialize_in=serialize_in, close=True,
                meta_location=True, **kwds)

            urn = makeUrn(self._poolname, resourcetype, index)
            self.setMetaByUrn(start, end, urn)

            l += self.writeHK(fp0)
            # print('tl %.8f %9d' % (time.time()-t0, l))
            logger.debug('HK written')
        except IOError as e:
            logger.error('Save failed. exc: %s trbk: %s.' % (str(e), trbk(e)))
            raise e  # needed for undoing HK changes
        return l, start, end

    def doLoad(self, resourcetype, index, start=None, end=None, serialize_out=False):
        """
        does the action of loading.

        serialize_out: if True returns contents in serialized form.
        """

        indexstr = str(index)
        pp = self.transformpath(self._poolname) + '/' + \
            resourcetype + '_' + indexstr
        js = self.readmmap(pp, start=start, end=end, close=True)
        if serialize_out:
            r = js
        else:
            from ..dataset.deserialize import deserialize
            r = deserialize(js)

        return r

    def doRemove(self, resourcetype, index, **kwds):
        """
        does the action of removal of product from pool.
        """

        fp0 = self.transformpath(self._poolname)
        fp1 = [op.abspath(pathjoin(fp0,  quote(r) + f'_{i}'))
               for r, i in zip(resourcetype, index)]
        res = []
        for fp in fp1:
            try:
                if fp in self._files:
                    if self._files[fp]:
                        self._files[fp].flush()
                        self._files[fp].close()
                    del self._files[fp]
                os.unlink(fp)
                self.writeHK(fp0)
                res.append(0)
            except RuntimeError as e:
                msg = f'Remove failed. exc: {e} trbk: {trbk(e)}'
                logger.debug(msg)
                if self.ignore_error_when_delete:
                    res.append(None)
                    continue
                else:
                    raise
        return res

    def doRemoveTag(self, tag, **kwds):
        """
        does the action of removal of product from pool.
        """

        l = self.writeHK()
        return

    def doWipe(self, keep=True):
        """
        does the action of remove-all
        """
        for n, f in self._files.items():
            if f:
                f.flush()
                f.close()
        self._files.clear()
        self._atimes.clear()
        self._cached_files.clear()

        # will leave a newly made pool dir
        wipeLocal(self.transformpath(self._poolname), keep=keep)
        return 0

    def getHead(self, ref):
        """ Returns the latest version of a given product, belonging
        to the first pool where the same track id is found.
        """

        raise (NotImplementedError())

    def backup(self):
        """ make a tarfile string into a string """

        fp0 = self.transformpath(self._poolname)
        logger.info('Making a gz tar file of %s for pool %s.' %
                    (fp0, self._poolname))
        with self._locks['r']:
            # Save unsaved changes
            self.writeHK(fp0)
            with io.BytesIO() as iob:
                with tarfile.open(None, 'w|gz', iob) as tf:
                    tar = tf.add(fp0, arcname='.')
                file_image = iob.getvalue()
        return file_image

    def restore(self, tar):
        """untar the input file to this pool and return the file list."""

        with self._locks['w']:
            fp0 = self.transformpath(self._poolname)
            self.doWipe()
            with io.BytesIO(tar) as iob:
                with tarfile.open(None, 'r|gz', iob) as tf:
                    tf.extractall(fp0)
            allf = find_all_files(fp0)
            # read into memory
            self._dTypes, self._dTags = tuple(
                self.readHK().values())
        logger.info('Restored from a gz tar file to %s for pool %s. %d files.' %
                    (fp0, self._poolname, len(allf)))

        return allf
