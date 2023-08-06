# -*- coding: utf-8 -*-
from .odict import ODict
from .quantifiable import Quantifiable
from .eq import DeepEqual
from .copyable import Copyable
from .annotatable import Annotatable

from collections.abc import Container, Sized
import logging
# create logger
logger = logging.getLogger(__name__)
#logger.debug('level %d' %  (logger.getEffectiveLevel()))


class DataContainer(Annotatable, Copyable, DeepEqual, Container):
    """ A DataContainer is a composite of data and description.

    mh: note that There is no metadata.
    Implemented partly from AbstractDataWrapper.
    """

    def __init__(self, data=None, **kwds):
        """
        data: a Container. Default is None.

        Parameters
        ----------

        Returns
        -------

        """
        #print(__name__ + str(kwds))

        if 1:  # data is None:  # or issubclass(data.__class__, Container):
            super().__init__(**kwds)  # DataContainer
            self.setData(data)
        else:
            raise TypeError('DataContainer needs a Container to initialize, not ' +
                            type(data).__name__)

    @property
    def data(self):
        """
        Parameters
        ----------

        Returns
        -------

        """
        return self.getData()

    @data.setter
    def data(self, newData):
        """ Property of the data of this datawrapper object.

        Parameters
        ----------

        Returns
        -------

        """
        self.setData(newData)

    def setData(self, data):
        """ Replaces the current DataData with specified argument. 
        mh: subclasses can override this to add listener whenevery data is
        replaced.

        Parameters
        ----------

        Returns
        -------

        """
        self._data = data

    def getData(self):
        """ Returns the data in this dw

        Parameters
        ----------

        Returns
        -------
        `self._data` or `None` if '._data' is missing. e.g. subclass overriding `setData` calling `getData` from its `setData` that is called by 'this.__init__'.
        """

        return getattr(self, '_data', None)

    def hasData(self):
        """ Returns whether this data wrapper has data. 


        Parameters
        ----------

        Returns
        -------
        `False` if data does not exist or is `None` or empty, `True` if otherwise.
        """
        d = getattr(self, '_data', None)
        return bool(d)

    def __contains__(self, x):
        """
        """
        try:
            return x in self._data
        except AttributeError:
            return False

    def __len__(self, *args, **kwargs):
        """ 0 if data does not exist or is `None`, size of data if otherwise.

        """

        d = getattr(self, '_data', None)
        return len(d) if d else 0


class DataWrapper(DataContainer, Quantifiable):
    """ A DataWrapper is a composite of data, unit and description.

    mh: note that all data are in the same unit. There is no metadata.
    Implemented from AbstractDataWrapper.
    """

    def __init__(self, *args, **kwds):
        """ 
        """
        super().__init__(*args, **kwds)  # DataWrapper


class DataWrapperMapper():
    """ Object holding a map of data wrappers. """

    def __init__(self, *args, **kwds):  # DataWrapperMapper
        """ 
        """
        super().__init__(*args, **kwds)  # DataWrapperMapper

    def getDataWrappers(self):
        """ Gives the data wrappers, mapped by name.

        Parameters
        ----------

        Returns
        -------

        """
        return self._data
