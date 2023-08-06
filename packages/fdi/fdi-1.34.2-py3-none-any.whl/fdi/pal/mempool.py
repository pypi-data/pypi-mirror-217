# -*- coding: utf-8 -*-
from .managedpool import ManagedPool
from .urn import makeUrn
from .dicthk import HKDBS
import logging
# create logger
logger = logging.getLogger(__name__)
# logger.debug('level %d' %  (logger.getEffectiveLevel()))


class MemPool(ManagedPool):
    """ the pool will save all products in memory.
    """

    def __init__(self, **kwds):
        """ creates data structure if there isn't one. if there is, read and populate house-keeping records. create persistent files if not exist.
        """

        super(MemPool, self).__init__(**kwds)

    def setup(self):
        """ Sets up MemPool interals.

        make sure that self._poolname and self._poolurl are present.
        """

        if super().setup():
            return True

        self._MemPool = {}
        # if self._poolname not in self._MemPool:
        #      self._MemPool[self._poolname] = {}
        # some new ####
        dTypes, dTags = tuple(self.readHK().values())

        logger.debug('created ' + self.__class__.__name__ +
                     ' ' + self._poolname + ' HK read.')
        # new ####
        self._dTypes.update(dTypes)
        self._dTags.update(dTags)
        # /new ###

        return False

    def getPoolSpace(self):
        """ returns the map of this memory pool.
        """
        return self._MemPool
        # if self._poolname in self._MemPool:
        #     return self._MemPool[self._poolname]
        # else:
        #     return None

    def readHK(self, hktype=None, serialize_in=True, serialize_out=False):
        """
        loads and returns the housekeeping data

        hktype: one of 'classes', 'tags', 'urns' to return. default is None to return alldirs
        serialize_out: if True return serialized form. Default is false.
        """

        if serialize_out:
            raise NotImplementedError
        if hktype is None:
            # some new ####
            hks = HKDBS
        else:
            hks = [hktype]
        hk = {}
        myspace = self.getPoolSpace()
        for hkdata in hks:
            if len(myspace) == 0 or not ('dT' in hkdata):
                r = {}
            else:
                r = myspace[hkdata]
            hk[hkdata] = r
        logger.debug('HK read from ' + self._poolname)
        return hk if hktype is None else hk[hktype]

    def writeHK(self):
        """
           save the housekeeping data to mempool
        """

        myspace = self.getPoolSpace()
        # new ####
        myspace['dTypes'] = self._dTypes
        myspace['dTags'] = self._dTags
        # /new ###

    def doSave(self, resourcetype, index, data, tags=None, serialize_in=True, **kwds):
        """ 
        does the media-specific saving
        """
        resourcep = resourcetype + '_' + str(index)
        myspace = self.getPoolSpace()
        myspace[resourcep] = data
        urn = makeUrn(self._poolname, resourcetype, index)
        self.setMetaByUrn(data, urn)
        self.writeHK()
        logger.debug('HK written')

    def setMetaByUrn(self, data, urn, resourcetype=None, index=None):
        """
        Sets the location of the meta data of the specified data to the given URN.

        :data: usually unserialized Product.
        """
        urn, datatype, sn = self.get_missing(
            urn=urn, datatype=resourcetype, sn=index, no_check=True)
        # new ###
        self._dTypes[datatype]['sn'][sn]['meta'] = data._meta
        # self._urns[urn]['meta'] = data._meta

    def getMetaByUrn(self, urn, resourcetype=None, index=None):
        """ 
        Get all of the meta data belonging to a product of a given URN.

        """
        urn, datatype, sn = self.get_missing(
            urn=urn, datatype=resourcetype, sn=index)
        # new ##
        # assert self._urns[urn]['meta'] == self._dTypes[datatype]['sn'][sn]['meta']
        # return self._urns[urn]['meta']
        return self._dTypes[datatype]['sn'][sn]['meta']

    def make_new(self):
        """ make a new directory.

        """
        pass


    
    def doLoad(self, resourcetype, index, start=0, end=0, serialize_out=False):
        """
        does the action of loadProduct.
        note that the index is given as a string.
        """
        if serialize_out:
            raise NotImplementedError
        indexstr = str(index)
        resourcep = resourcetype + '_' + indexstr
        myspace = self.getPoolSpace()
        return myspace[resourcep]

    def doRemove(self, resourcetype, index, asyn=False):
        """
        does the action of removal.
        """

        myspace = self.getPoolSpace()
        for r in [f'{r}_{i}' for r, i in zip(resourcetype, index)]:
            del myspace[r]
        self.writeHK()
        return [0]

    def doWipe(self, keep=True):
        """
        does the action of remove-all
        """

        # logger.debug()
        p = self.getPoolSpace()
        p.clear()

        # del p will only delete p in current namespace, not anything in _MemPool
        # this wipes all mempools
        # pools = [x for x in self._MemPool]
        # for x in pools:
        #    del self._MemPool[x]
        # if self._poolname in self._MemPool:
        #    del self._MemPool[self._poolname]
        return 0

    def doRemoveTag(self, tag, asyn=False):
        """
        does the action of tag removal.
        """
        pass

    def getHead(self, ref):
        """ Returns the latest version of a given product, belonging
        to the first pool where the same track id is found.
        """
        raise NotImplementedError
