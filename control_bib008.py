# This file is part of pymarc. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution and at
# https://opensource.org/licenses/BSD-2-Clause. pymarc may be copied, modified,
# propagated, or distributed according to the terms contained in the LICENSE
# file.

"""The pymarc.leader file."""
from typing import Union
from pymarc import BadLeaderValue


class Field008(object):
    """Mutable leader.

    A class to manipulate a `Record`'s 008 control field.

    You can use the properties (`status`, `bibliographic_level`, etc.) or their
    slices/index equivalent (`leader[5]`, `leader[7]`, etc.) to read and write
    values.

    See `LoC's documentation
    <https://www.loc.gov/marc/bibliographic/bd008.html>`_
    for more info about those fields.

    .. code-block:: python
    from pymarc import MARCReader
     with open('test/marc.dat', 'rb') as fh:
        reader = MARCReader(fh)
            for record in reader:
                ct_fld = control_bib008.Field008(record['008'].data)
                print (len(str(ct_fld)))
                print (f"{ct_fld.date_entered}={ct_fld.date_type}=&&")
                print (f"{ct_fld.date1}={ct_fld.date2}=&&")
                print (f"{ct_fld.publication_place}={ct_fld.language}=&&")
                print (f"{ct_fld.modified_record}={ct_fld.cataloging_source}=&&")

                #Change values
                ct_fld.date1 = 'uuuu'
                ct_fld.date2 = 'uu??'
                print (f"{ct_fld.date1}={ct_fld.date2}=&&")

    """
    
    FIXED_LENGTH_008_LEN = 40
    
    def __init__(self, field008: str) -> None:
        """Field008 is initialized with a string."""
        if len(field008) != 40 : #FIXED_LENGTH_008_LEN:
            #raise RecordLeaderInvalid
            raise "Error in 008 length"
        self.field008 = field008

    def __getitem__(self, item: Union[str, int, slice]) -> str:
        """Get values using position, slice or properties.

        field008[:4] == field008.length
        """
        if isinstance(item, slice) or isinstance(item, int):
            return self.field008[item]
        return getattr(self, item)

    def __setitem__(self, item: str, value: str) -> None:
        """Set values using position, slice or properties.

        field008[6] = "a"
        field008[0:6] = "0000"
        field008.date_entered = "202412"
        """
        if isinstance(item, slice):
            self._replace_values(position=item.start, value=value)
        elif isinstance(item, int):
            self._replace_values(position=item, value=value)
        else:
            setattr(self, item, value)

    def __str__(self) -> str:
        """A string representation of the leader."""
        return self.field008

    def _replace_values(self, position: int, value: str) -> None:
        """Replaces the values in the leader at `position` by `value`."""
        if position < 0:
            raise IndexError("Position must be positive")
        after = position + len(value)
        if after > 40: #FIXED_LENGTH_008_LEN:
            raise (f"{value} is too long to be inserted at {position}")
        self.field008 = self.field008[:position] + value + self.field008[after:]

    @property
    def date_entered(self) -> str:
        """Record length (00-04)."""
        return self.field008[:6]

    @date_entered.setter
    def date_entered(self, value: str) -> None:
        """date_entered (00-05)."""
        if len(value) != 6:
            raise BadLeaderValue(f"Date Entered is 6 char field, got {value}")
        self._replace_values(position=0, value=value)

    @property
    def date_type(self) -> str:
        """Type of date/publication status (06)."""
        return self.field008[6]

    @date_type.setter
    def date_type(self, value: str) -> None:
        """Type of date/publication status (06)."""
        if len(value) != 1:
            raise BadLeaderValue(f"Date Type is 1 char field, got {value}")
        self._replace_values(position=6, value=value)

    @property
    def date1(self) -> str:
        """Date 1 (07-10)."""
        return self.field008[7:11]

    @date1.setter
    def date1(self, value: str) -> None:
        """Date 1 (07-10)."""
        if len(value) != 4:
            raise BadLeaderValue(f"Date 1 is 4 char field, got {value}")
        self._replace_values(position=7, value=value)

    @property
    def date2(self) -> str:
        """Date 2 (11-14)."""
        return self.field008[11:15]

    @date2.setter
    def date2(self, value: str) -> None:
        """Date 2 (11-14)."""
        if len(value) != 4:
            raise BadLeaderValue(f"Date 2 is 4 char field, got {value}")
        self._replace_values(position=11, value=value)

    @property
    def publication_place(self) -> str:
        """Place of publication (15-17)."""
        return self.field008[15:18]

    @publication_place.setter
    def publication_place(self, value: str) -> None:
        """Type of control (08)."""
        if len(value) != 3:
            raise BadLeaderValue(f"Place of publication is 3 char field, got {value}")
        self._replace_values(position=15, value=value)

    @property
    def language(self) -> str:
        """Language code (35-37)."""
        return self.field008[35:38]

    @language.setter
    def language(self, value: str) -> None:
        """language coding scheme (35-37)."""
        if len(value) != 3:
            raise BadLeaderValue(
                f"Language coding scheme is 3 char field, got {value}"
            )
        self._replace_values(position=35, value=value)

    @property
    def modified_record(self) -> str:
        """modified record (38)."""
        return self.field008[38]

    @modified_record.setter
    def modified_record(self, value: str) -> None:
        """modified record (38)."""
        if len(value) != 1:
            raise BadLeaderValue(f"Modified record is 1 char field, got {value}")
        self._replace_values(position=38, value=value)

    @property
    def cataloging_source(self) -> str:
        """Cataloging source (39)."""
        return self.field008[39]

    @cataloging_source.setter
    def cataloging_source(self, value: str) -> None:
        """Subfield code count (39)."""
        if len(value) != 1:
            raise BadLeaderValue(f"Cataloging source is 1 char field, got {value}")
        self._replace_values(position=39, value=value)
