# -*- coding: utf-8 -*-

from .indexed import Indexed
from .ndprint import ndprint
from .odict import ODict
from ..utils.common import wls
from .dataset import make_title_meta_l0, CompositeDataset
from .shaped import Shaped
from .metadata import MetaData

try:
    from .tabledataset_datamodel import Model
except ImportError:
    Model = {'metadata': {}}


import sys
from collections.abc import Sequence
from collections import OrderedDict
import itertools
from copy import copy

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

import logging
# create logger
logger = logging.getLogger(__name__)
# logger.debug('level %d' %  (logger.getEffectiveLevel()))


class TableModel():
    """ to interrogate a tabular data model
    """

    def __init__(self, **kwds):
        """

        """
        super().__init__(**kwds)

    def getColumnClass(self, columnIndex):
        """ Returns the class for the first cell
        values in the column.
        """
        return self.getColumn(columnIndex)[0].__class__

    def getColumnCount(self):
        """ Returns the number of columns in the model. """
        return len(self.getData())

    def getColumnName(self, columnIndex):
        """ Returns the name of the column at columnIndex.

        returns a set of columns if key  is a slice.
        """

        return self.getColumnNames()[columnIndex]

    def getColumnNames(self):
        """ Returns the column names. """
        return list(self.getData().keys())

    def getRowCount(self):
        """ Returns the number of rows in the model. """
        return len(self.getColumn(0))

    def getValueAt(self, rowIndex, columnIndex):
        """ Returns the value for the cell at columnIndex and rowIndex. """
        return self.getColumn(columnIndex).data[rowIndex]

    def isCellEditable(self, rowIndex, columnIndex):
        """ Returns true if the cell at rowIndex and columnIndex
        is editable. """
        return True

    def setValueAt(self, value, rowIndex, columnIndex):
        """Sets the value in the cell at columnIndex and rowIndex
        to Value.
        """
        self.getColumn(columnIndex).data[rowIndex] = value


def maybe2rows(header_names, units=None, col_width=None, sep='.', one_row=False, linebreak='\n'):
    """ makes one-row or two-row column headers
    :units: will not show line if all blank.
    :sep: a string of separator characters to split header into two fragments. a header only uses the first matching char from left. Grouping does not distinguish which sep-char was used to split a header. Example: '.' (default), '._/'
    :one_row: Force one row but add line breaks at sep

    """
    if col_width is None:
        col_width = -1

    found_repeat = False
    hd, hd2 = [], []
    last = None
    for x in header_names:
        try:
            # only test if there is '.'
            if not any(s in x for s in sep):
                raise ValueError()
            f = float(x)
            hd.append(x)
            hd2.append('')
            if not found_repeat:
                last = ''
        except ValueError:
            # 'a.b', 'a.c' -> ('a','b'), ('a','c')
            r = str(x)
            # try splitting with all sep chars until the first successful split to get the right-most fragment

            for s in sep:
                p = r.rsplit(s, 1)
                if len(p) > 1:
                    break
            # p0 is the group. p1 the sub-name
            if len(p) > 1:
                # 'foo.'.rsplit('.') == ['foo','']
                p0 = p[0]
                p1 = p[1]
            else:
                # 'bar'.rsplit('.') == ['bar']
                p0 = ''
                p1 = r
            hd.append(p1)
            hd2.append(p0)
            # repeat is never found if one row
            if not one_row and not found_repeat:
                if p0 != '' and p0 == last:
                    found_repeat = True
                last = p0

    # [(column name, unit), ...]. Widths of column head is limited
    hdr1 = [wls(x.replace('.', '.\n') if one_row else x,
                width=col_width, linebreak=linebreak)
            for x in (hd if found_repeat else header_names)]
    # name and unit rows.
    if any(units):
        hdr = list('%s%s(%s)' % (nu[0], linebreak, nu[1])
                   for nu in zip(hdr1, units))
    else:
        hdr = hdr1

    if 0:  # one_row:
        return list(linebreak.join(hd2, hdr))
    if found_repeat:
        # if there is found_repeat. use 2-row header
        return list(zip(hd2, hdr))
    else:
        return hdr


MdpInfo = Model['metadata']


class TableDataset(CompositeDataset, TableModel, Shaped):
    """  Special dataset that contains a single Array Data object.
    A TableDataset is a tabular collection of Columns. It is optimized to work on array data..
    The column-wise approach is convenient in many cases. For example, one has an event list, and each algorithm is adding a new field to the events (i.e. a new column, for example a quality mask).

    Although mechanisms are provided to grow the table row-wise, one should use these with care especially in performance driven environments as this orthogonal approach (adding rows rather than adding columns) is expensive.

    General Note:

    For reasons of flexibility, memory consumption and performance, this class is not checking whether all columns are of the same length: this is the responsibility of the user/developer. See also the library documentation for more information about this.

    Note on column names:

    If a column is added without specifying a name, the name ColumnX is created, where X denotes the index of that column.
    Column name duplicity is not allowed.

    Developers:

    See "Writing special datasets or products" at the developer's documentation also.


    Please see also this selection example.
    """

    def __init__(self, data=None,
                 description=None,
                 typ_=None,
                 version=None,
                 zInfo=None,
                 alwaysMeta=True,
                 **kwds):
        """
        """

        self._list = []

        # collect MDPs from args-turned-local-variables.
        metasToBeInstalled = copy(locals())
        metasToBeInstalled.pop('__class__', None)
        metasToBeInstalled.pop('kwds', None)
        metasToBeInstalled.pop('self', None)
        metasToBeInstalled.pop('zInfo', None)

        global Model
        if zInfo is None:
            zInfo = Model

        super().__init__(zInfo=zInfo, **metasToBeInstalled,
                         **kwds)  # initialize data, meta, unit
        self.updateShape()

    # def getData(self):
    #     """ Optimized for _data being an ``ODict/dict`` implemented with ``DataContaier``.

    #     """

    #     return self._data

    def setData(self, data):
        """ sets name-column pairs from data.

        Valid formd include: {str:Column, ...} or [(str, [num, ...], str)]
        or [(str, Column), ...] or [[num ...],  [num ...], ...]

        [{'name':str,'column':Column}] form is deprecated.

        Existing data will be discarded except when the provided data is a list of lists, where existing column names and units will remain but data replaced, and extra data items will form new columns named 'column'+index (index counting from 1) with unit None.
        """
        # logging.debug(data.__class__)

        if data is None:
            super(TableDataset, self).setData(ODict())
            self.updateShape()
            return

        current_data = self.getData()
        # list of keys of current data
        curdk = list(current_data.keys()) if current_data else []
        super(TableDataset, self).setData(ODict())
        if issubclass(data.__class__, seqlist):
            from .arraydataset import Column
            for ind, x in enumerate(data):
                if issubclass(x.__class__, maplist) \
                   and 'name' in x and 'column' in x:
                    raise DeprecationWarning(
                        'Do not use [{"name":name, "column":column}...]. Use {name:column, ...} instead.')
                if issubclass(x.__class__, (list, tuple)):
                    # check out string-started columns (2-col not included
                    if len(x) > 1 and issubclass(x[0].__class__, str) and not issubclass(x[1].__class__, str):
                        if issubclass(x[1].__class__, (list, tuple)):
                            u = x[2] if len(x) > 2 else ''
                            self.setColumn(x[0], Column(data=x[1], unit=u))
                        elif issubclass(x[1].__class__, Column):
                            self.setColumn(x[0], x[1])
                        else:
                            raise ValueError(
                                '[[str, [], str]...], [[str, []]...], [[str, Column]...] needed.')
                    else:
                        # x is not string-started
                        # e.g. [[1, 2, 3], [4, 5, 6]]
                        if current_data is None or len(current_data) <= ind:
                            # update the data of the ind-th column
                            self.setColumn('', Column(data=x, unit=None))
                        else:
                            colname = curdk[ind]
                            current_data[colname].data = x
                            self.setColumn(colname, current_data[colname])
                else:
                    raise ValueError(
                        'Cannot extract name and column from list member ' + str(x))
        elif issubclass(data.__class__, maplist):
            # [Column, ... ]
            for k, v in data.items():
                self.setColumn(k, v)
        else:
            raise TypeError('must be a Sequence or a Mapping. ' +
                            data.__class__.__name__ + ' found.')
        self.updateShape()

    def addColumn(self, name, column, col_des=True):
        """ Adds the specified column to this table, and attaches a name
        to it.

        If the name is null, a dummy name "column"+column_count+1 is created, such that it can be accessed by getColumn(str).

        If column name exists the corresponding column is substituted.

        Parameters:
        name - column name.
        column - column to be added.
        col_des - if True (default) and if column description is 'UNKNOWN' or `None`, set to column name.
        """

        d = self.getData()
        if d is None:
            d = ODict()

        if name == '' or name is None:
            idx = self.getColumnCount()
            name = 'column' + str(idx+1)
            self._list.append(column.getData())
        else:
            try:
                self._list[self.indexOf(name)] = column.getData()
            except ValueError as e:
                self._list.append(column.getData())
        des = column.getDescription()
        if col_des and des == 'UNKNOWN' or des is None:
            column.setDescription(name)
        d[name] = column

        self.updateShape()

    def removeColumn(self, key):
        """ Removes the columns specified by ``key``.

        ref. ``getColumnMap`` on ``key`` usage.
        """

        for name in self.getColumnMap(key).keys():
            self._list.pop(self.indexOf(name))
            del (self.data[name])
        self.updateShape()

    def indexOf(self, key):
        """ Returns the index of specified column.

        if the key is a Column,
        it looks for equal references (same column objects), not for
        equal values.
        If the key is a string, Returns the index of specified Column name.
        """
        from .arraydataset import Column
        if issubclass(key.__class__, str):
            ks = list(self.getData().keys())
            k = key
        elif issubclass(key.__class__, Column):
            ks = list(id(v) for v in self.getData().values())
            k = id(key)
        else:
            raise "key must be string or Column, not %s." % type(key).__name__

        self.updateShape()
        return ks.index(k)

    def addRow(self, row, rows=False):
        """ Adds the specified map as a new row to this table.

        row: row is a dict with names as keys and row data as values.
        rows: append each element in row if the row data is a list.
        """

        d = self.getData()
        if len(row) < len(d):
            msg = 'row width d% should be %d.' % (len(row), len(d))
            raise ValueError(msg)

        for c in d.keys():
            if rows:
                d[c].data.extend(row[c])
            else:
                d[c].data.append(row[c])
            if hasattr(d[c], 'updateShape'):
                d[c].updateShape()
        self.updateShape()

    def getRowMap(self, rowIndex):
        """ Returns a dict of column-names as the keys and the objects located at a particular row(s) as the values.

        rowIndex: return the following as the value for each key-value pair:
* int: the int-th row's elements;
* ``Slice`` object, a list of rows from slicing the column. Example ``a.getRow(Slice(3,,))``;
* list of integers: they are used as the row index to select the rows.
* list of booleans: rows where the corresponding boolean is True are chosen.
        """
        cl = rowIndex.__class__
        d = self.getData()
        if issubclass(cl, (int, slice)):
            return {n: c.getData()[rowIndex] for n, c in d.items()}
        if issubclass(cl, list):
            if type(rowIndex[0]) == int:
                return {n: [c.getData()[i] for i in rowIndex] for n, c in d.items()}
            if type(rowIndex[0]) == bool:
                # if len(rowIndex) != len(n):
                # logger.info('%s Selection length %d should be %d.' %
                #        (name, len(rowIndex), len(n)))
                return {n: [x for x, s in zip(c.getData(), rowIndex) if s] for n, c in d.items()}
        else:
            raise ValueError(
                'RowIndex must be an int, a slice, or a list of ints or bools.')

    def getRow(self, rowIndex):
        """ Returns a list containing the objects located in a particular row, or a list of rows.

        rowIndex: ref ``getRowMap()``
* int: return the int-th row in a list of elements;
* ``Slice`` object, list of integers, list of booleans: return a list of rows each represented by a tuple. Example ``a.getRow(Slice(3,,))``, ``[2,4]``, ``[True, False...]``.
        """

        it = self.getRowMap(rowIndex).values()
        if issubclass(rowIndex.__class__, int):
            # return a list of row elements
            return list(it)
        # return transposed in a list
        return list(zip(*it))

    def select(self, selection):
        """ Select a number of rows from this table dataset and
        return a new TableDataset object containing only the selected rows.

        selection:  to form a new Tabledataset with ref ``getRowMap()``
        """

        d = ODict()
        if issubclass(selection.__class__, int):
            for name, data in self.getRowMap(selection).items():
                d[name] = Column(
                    data=[data], unit=self.getColumn(name).getUnit())
                return TableDataset(data=d)

        from .arraydataset import Column
        for name, data in self.getRowMap(selection).items():
            d[name] = Column(data=data, unit=self.getColumn(name).getUnit())
        return TableDataset(data=d)

    def removeRow(self, rowIndex):
        """ Removes a row with specified index from this table.

        rowIndex: int or a ``Slice`` object. Example ``a.removeRow(Slice(3,,))``.
        return: removed row data.
        """
        if issubclass(rowIndex.__class__, slice):
            ret = []
            for x in self.getData().values():
                ret.append(x.data[rowIndex])
                del x.data[rowIndex]
                x.updateShape()
            self.updateShape()
            return ret
        r = []
        for x in self.getData().values():
            r.append(x.data.pop(rowIndex))
            x.updateShape()

        self.updateShape()
        return r

    @ property
    def rowCount(self):
        return self.getRowCount()

    @ rowCount.setter
    def rowCount(self, newRowCount):
        self.setRowCount(newRowCount)

    def setRowCount(self, rowCount):
        """ cannot do this.
        """
        raise ValueError('Cannot set row count.')

    @ property
    def columnCount(self):
        return self.getColumnCount()

    @ columnCount.setter
    def columnCount(self, newColumnCount):
        self.setColumnCount(newColumnCount)

    def setColumnCount(self, columnCount):
        """ cannot do this.
        """
        raise ValueError('Cannot set column count.')

    @ property
    def list(self):
        return self._list

    @ list.setter
    def list(self, l):
        raise NotImplemented

    def getColumnMap(self, key=None):
        """ Returns a dict of column-names as the keys and the column(s) as the values.

        key: return the following as the value for each key-value pair:
* int: name-value where value is the int-th column.
* ``Slice`` object, a list of name-columns from slicing the column index. Example ``a.getColumn(Slice(3,,))``;
* Sequence of integers/strings: they are used as the column index/name to select the columns.
* Sequence of booleans: columns where the corresponding boolean is True are chosen.
Default is to return all columns.
        """
        d = self.getData()
        try:
            if d is None or key is None or len(d) == 0:
                return d
        except TypeError:
            pass

        cl = key.__class__
        if issubclass(cl, int):
            t = list(d.items())[key]
            return {t[0]: t[1]}       # {str:Column}
        if issubclass(cl, slice):
            return ODict(list(d.items())[key])  # {str:Column, ...}
        if issubclass(cl, str):
            return {key: d[key]}      # {str:Column}

        if issubclass(cl, Sequence):
            if type(key[0]) == int:
                # {str:Column, ...}
                return ODict(list(d.items())[i] for i in key)
            if type(key[0]) == str:
                return {n: d[n] for n in key}  # {str:Column, ...}
            if type(key[0]) == bool:
                # {str:Column, ...}
                return ODict(x for x, s in zip(d.items(), key) if s)
        else:
            raise ValueError(
                '``key`` must be an int, a string, a slice, or a list of ints, strings, or bools.')

    def getColumn(self, key):
        """ Returns the particular column, or a list of columns.

        key: ref ``getColumnMap()``
* int/str: return the int-th/named column;
* ``Slice`` object, list of columns of sliced column indices;
* list of integers/strings: return a list of columns corresponding to the given column index/name, or where key is True. Example ``a.getColumn(Slice(3,,))``, ``[2, 4]``, ``['time', ``energy']``.
* list of booleans: return a list of columns  where key is True. Example ``[True, False...]``.
        """

        it = self.getColumnMap(key).values()
        if len(it) == 0:
            return []
        if issubclass(key.__class__, (int, str)):
            # return a list of row elements
            return list(it)[0]
        # return transposed in a list
        return list(it)

    def setColumn(self, key, value):
        """ Replaces a column in this table with specified name to specified column if key is a string and exists, or if the key is an integer in 0 to the number of columns, insert at column-index=key, with the name 'column'+key, else add a new coolumn.
        """

        if self.getData() is None:
            key = ''
        elif type(key) == int:
            nms = self.getColumnNames()
            if 0 <= key and key < len(nms):
                key = nms[key]
            else:
                key = ''
        self.addColumn(name=key, column=value)

        self.updateShape()

    def __iter__(self):
        for x in self.getData():
            yield x

    def items(self):
        """ for k,v in tabledataset.items()
        """
        return self.getData().items()

    def __getitem__(self, key):
        """ return colmn of given key.

        ref. ``getColumn()``.
        """
        return self.getColumn(key)

    def __setitem__(self, key, value):
        """
        """
        self.setColumn(key, value)

    def __delitem__(self, key):
        """ delete colmn of given key.

        ref. ``removeColumn()``.
        """
        return self.removeColumn(key)

    keys = TableModel.getColumnNames

    # __len__ = TableModel.getColumnCount

    # def __contains__(self, name):
    #     """ if 'name` is found in column names.
    #     """
    #     return name in self.getData()

    def __repr__(self):
        return self.toString(level=2)

    def toString(self, level=0, extra=False, param_widths=None,
                 tablefmt='grid', tablefmt1='simple', tablefmt2='plain',
                 width=0, matprint=None, trans=True, no_meta=False,
                 heavy=True, center=-1, **kwds):
        """
        tablefmt2: format of 2D data, others see `MetaData.toString`.
        """

        if matprint is None:
            matprint = ndprint

        cn = self.__class__.__name__
        if level > 1:
            s = cn + '('
            if not no_meta:
                s += self.meta.toString(
                    level=level, extra=extra,  param_widths=param_widths,
                    tablefmt=tablefmt, tablefmt1=tablefmt1, tablefmt2=tablefmt2,
                    width=width,
                    **kwds) + 'data= '
            return s + '{' + \
                ', '.join('"%s": %s' % (k, v.toString(
                    level=level, extra=extra,  param_widths=param_widths,
                    tablefmt=tablefmt, tablefmt1=tablefmt1, tablefmt2=tablefmt,
                    width=width, heavy=heavy, **kwds))
                    for k, v in self.getColumnMap().items()) + \
                '})'

        html = 'html' in tablefmt.lower() or 'html' in tablefmt2.lower()
        br = '<br>' if html else '\n'
        if html:
            tablefmt = tablefmt2 = 'unsafehtml'
        s, last = make_title_meta_l0(self, level=level, extra=extra, param_widths=param_widths,
                                     tablefmt=tablefmt, tablefmt1=tablefmt1,
                                     tablefmt2=tablefmt2, center=center,
                                     width=width, heavy=heavy,
                                     html=html, excpt=['description'],
                                     no_meta=no_meta,
                                     **kwds)
        width = len(last)-1
        if level == 0 and not no_meta:
            if html:
                d = '<center><u>%s</u></center>\n' % 'DATA'
            else:
                d = 'DATA'.center(width) + '\n' + '----'.center(width) + '\n'
        else:
            d = ''
        rowlimit = 2 if level > 1 else 20 if level == 1 else None

        cols = self.getData().values()
        # This is obsolete for tabulate >= 0.8.10:
        # widest width in all of default and in param_widths
        # w = MetaData.MaxDefWidth if param_widths == -1 or \
        #    param_widths is None else \
        #    max(MetaData.MaxDefWidth, max(param_widths.values()))
        # if html:
        #     w = w
        w = MetaData.MaxDefWidth
        coldata = [list(itertools.islice(x.data, rowlimit)) for x in cols]
        # table headers
        hdr = maybe2rows(self.getData().keys(),
                         (str(x.unit) for x in cols),
                         col_width=w, one_row=html,
                         linebreak=br)
        dtab = matprint(coldata, trans=trans, headers=hdr,
                        tablefmt=tablefmt, tablefmt1=tablefmt1,
                        tablefmt2=tablefmt2, center=center,
                        mdim=2, param_widths=param_widths,
                        maxElem=sys.maxsize, **kwds)
        table_width = max(len(x) for x in dtab[:600].split('\n'))
        shift = ' ' * ((width - table_width) // 2)
        shift1 = '\n%s' % shift
        d += shift + dtab[:-1].replace('\n', shift1) + dtab[-1]
        collen = self.getRowCount()
        if level and rowlimit is not None and rowlimit < collen:
            d += '(Only display %d rows of %d for level=%d.)' % (rowlimit, collen, level)
        return f'{d}{last}\n' if no_meta else f'{s}\n{d}{last}\n'

    string = toString
    txt = toString

    def __getstate__(self):
        """ Can be encoded with serializableEncoder """
        return OrderedDict(
            _ATTR_meta=getattr(self, '_meta', None),
            **self.getData())


class IndexedTableDataset(Indexed, TableDataset):
    """ TableDataset with an index table for efficient row look-up.

    """

    def __init__(self, **kwds):
        """
        """
        self._indexCols = [0]
        self._rowIndexTable = {}
        super().__init__(**kwds)  # initialize data, meta, unit

    def getColumnsToLookup(self):
        """ returns an iterator that gives a number of sequences to looking up over.
        """

        # list of Column's arrays
        return [x.data for x in self.getColumn(self._indexPattern)]

    def setData(self, data):
        """  sets name-column pairs from data and updates index if needed

        """

        d = self.getData()
        if d:
            reindex = False
            lcd = len(d)
            if issubclass(data.__class__, seqlist):
                for ind, x in enumerate(data):
                    if lcd > ind:
                        if reindex == False and ind in self._indexPattern:
                            reindex = True
        else:
            reindex = True
        super().setData(data)
        if reindex:
            self.updateToc()

    def vLookUp(self, key, return_index=True, multiple=False):
        """ Similar to Excel VLOOKUP, return all records (rows) that match the key.
        key: taken as a dictionary key unless ``multiple`` is True.
        return_index: if True (default) return index in the array of columns.
        multiple: if True (default is False) loop through key as a sequence of keys and return a sequece.
        """

        if multiple:
            if return_index:
                toc = self._tableOfContent
                return [toc[k] for k in key]
            else:
                toc = self._tableOfContent
                # return [[c[toc[k]] for c in self._list] for k in key]
                return list(zip(*((c[toc[k]] for k in key) for c in self._list)))
        else:
            if return_index:
                return self._tableOfContent[key]
            else:
                rec_ind = self._tableOfContent[key]
                return [c[rec_ind] for c in self._list]

    def hashx(self):
        s = self.__getstate__().values()
        l = []
        return super().hash(hash_list=self.data.values())

    def __getstate__(self):
        """ Can be encoded with serializableEncoder """
        # try:
        #     description = self.description
        # except (AttributeError, KeyError):
        #     description = None
        return Indexed.__getstate__(self).update(
            _ATTR_meta=getattr(self, '_meta', None),
            **self.getData())
