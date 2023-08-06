# -*- coding: utf-8 -*-

from ..utils.common import mstr, bstr
from .listener import MetaDataListener
from .serializable import Serializable
from .typed import Typed
from .odict import ODict
from .attributable import Attributable
from .abstractcomposite import AbstractComposite
from .datawrapper import DataContainer, DataWrapper
from .eq import DeepEqual
from .copyable import Copyable
from .annotatable import Annotatable


from collections import OrderedDict
import logging
import sys
import shutil
import os

if sys.version_info[0] + 0.1 * sys.version_info[1] >= 3.3:
    PY33 = True
    from collections.abc import Container, Sequence, Mapping
    seqlist = Sequence
    maplist = Mapping
else:
    assert 0, 'python 3'
    PY33 = False
    from .collectionsMockUp import ContainerMockUp as Container
    from .collectionsMockUp import SequenceMockUp as Sequence
    from .collectionsMockUp import MappingMockUp as Mapping
    seqlist = (tuple, list, Sequence, str)
    # ,types.XRangeType, types.BufferType)
    maplist = (dict, Mapping)

# create logger
logger = logging.getLogger(__name__)
# logger.debug('level %d' %  (logger.getEffectiveLevel()))

# from .composite import


class Dataset(Attributable, DataContainer, Serializable, MetaDataListener):
    """ Attributable and annotatable information data container
    that can be be part of a Product.

    developer notes:
    The intent is that developers do not derive from this interface

    directly. Instead, they should inherit from one of the generic
    datasets that this package provides:

    mh: GenericDataset, UnstructuredDataset
    ArrayDataset.
    TableDataset or
    CompositeDataset.
    """

    def __init__(self, **kwds):
        """
        Parameter
        ---------

        Returns
        -------
        """
        super().__init__(**kwds)

    def accept(self, visitor):
        """ Hook for adding functionality to object
        through visitor pattern.
        Parameter
        ---------

        Returns
        -------
        """
        visitor.visit(self)

    def toString(self, level=0,
                 tablefmt='grid', tablefmt1='simple', tablefmt2='psql',
                 param_widths=None, width=0, matprint=None, trans=True,
                 heavy=True, center=-1, **kwds):
        """ matprint: an external matrix print function
        trans: print 2D matrix transposed. default is True.
        Parameter
        ---------

        Returns
        -------

        """
        cn = self.__class__.__name__
        if level > 1:
            return cn + \
                '{ %s, description = "%s", meta = %s }' % \
                (str(self.data), str(self.description), self.meta.toString(
                    tablefmt=tablefmt, tablefmt1=tablefmt1, tablefmt2=tablefmt2,
                    level=level, width=width, param_widths=param_widths,
                    matprint=matprint, trans=trans, heavy=heavy, **kwds))
        html = 'html' in tablefmt.lower() or 'html' in tablefmt2.lower()
        br = '<br>' if html else '\n'

        s, last = make_title_meta_l0(self, level=level, width=width, heavy=heavy,
                                     tablefmt=tablefmt, tablefmt1=tablefmt1,
                                     tablefmt2=tablefmt2, center=center,
                                     param_widths=param_widths,
                                     html=html, excpt=['description'])
        width = len(last) - 1
        if html:
            d = '<center><u>%s</u></center>\n' % 'DATA'
        else:
            d = 'DATA'.center(width) + '\n' + '----'.center(width) + '\n'

        d += bstr(self.data, level=level, heavy=heavy, center=center,
                  tablefmt=tablefmt, tablefmt1=tablefmt1, tablefmt2=tablefmt2,
                  yaml=True, param_widths=param_widths, html=html,
                  **kwds) if matprint is None else \
            matprint(self.data, level=level, trans=False, headers=[],
                     tablefmt2='rst', heavy=heavy,
                     **kwds)
        return f'{s}\n{d}\n{last}\n'

    string = toString
    txt = toString

    def __getstate__(self):
        """ Can be encoded with serializableEncoder.


        Parameter
        ---------

        Returns
        -------
        """

        s = OrderedDict(description=self.description,
                        meta=self._meta,
                        data=self.data)
        return s


def make_title_meta_l0(self, level=0,
                       heavy=True, center=0, html=False, no_meta=False,
                       **kwds):
    """ make toString title and metadata.

    :heavy: use bold symbols for separaters.
    :center: 0 for no centering;  -1 for centering with metadata table; other  for ``str.center(<center>``.
    """
    # title
    cn = self.__class__.__name__
    desc = self.meta.get('description', '')
    if desc:
        desc = desc.value
    t = ('*** <b>%s (%s)</b> ***' if html else '*** %s (%s) ***') % (cn, desc)
    tw = len(t)
    # make the table and find out the width first
    table = '' if no_meta else mstr(self._meta, level=level, html=html, **kwds)
    table_width = max(len(x) for x in table[:600].split('\n'))
    if center and not html:
        # max separation between consequitive '\n' s
        if center == -1:
            try:
                tt = os.get_terminal_size()
                width, height = tt
                shift = ' ' * ((width - table_width) // 2)
                shift1 = '\n%s' % shift
                table = shift + table.replace('\n', shift1)
            except OSError:
                width = table_width

        else:
            width = center
    else:
        width = tw

    if heavy:
        # beginning of a stand-alone dataset
        l = ('*' if level else '*') * tw
    else:
        # beginning of a dataset that is a component of a another
        l = '_' * tw

    br = '<br>' if html else '\n'
    if center:
        if html:
            t = '<center>%s</center>' % t
            l = '<center>%s</center>' % l
            m = '' if no_meta else '<center><u>%s</u></center>' % 'META'
        else:
            t = t.center(width)
            l = l.center(width)
            m = '' if no_meta else 'META'.center(width)
    else:
        m = '' if no_meta else 'META%s----%s' % (br, br)
    t += '\n'
    l += '\n'

    if center:
        s = t if level else (l + t + m)
    else:
        s = l + t + ('' if level else l + m)
    s += table
    if html:
        last = '<hr size="3">' if heavy else '<hr>'
    else:
        last = "=" * width if heavy else "~" * width
    last += br

    return s, last


class GenericDataset(Dataset, Typed, DataWrapper):
    """ mh: Contains one typed data item with a unit and a typecode.
    """

    def __init__(self, **kwds):
        """
        """
        super().__init__(**kwds)  # initialize data, meta, unit

    def __iter__(self):
        for x in self.getData():
            yield x


class CompositeDataset(MetaDataListener, AbstractComposite):
    """  An CompositeDataset is a Dataset that contains zero or more
    named Datasets. It allows to build arbitrary complex dataset
    structures.

    It also defines the iteration ordering of its children, which is
    the order in which the children were inserted into this dataset.
    """

    def __init__(self, **kwds):
        """
        Parameter
        ---------

        Returns
        -------

        """
        super(CompositeDataset, self).__init__(
            **kwds)  # initialize _sets, meta, unit

    def __getstate__(self):
        """ Can be encoded with serializableEncoder

        Parameter
        ---------

        Returns
        -------

        """
        return OrderedDict(  # description=self.description,
            _ATTR_meta=self._meta,
            **self._data)
