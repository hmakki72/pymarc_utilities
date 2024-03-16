# This file is part of pymarc. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution and at
# https://opensource.org/licenses/BSD-2-Clause. pymarc may be copied, modified,
# propagated, or distributed according to the terms contained in the LICENSE
# file.

"""The pymarc.leader file."""
from typing import Union

#from controlfields_constants.py import FIXED_LENGTH_008_LEN
from pymarc import BadLeaderValue


class Field008(object):
    """Mutable leader.

    A class to manipulate a `Record`'s 008 control field.

    You can use the properties (`status`, `bibliographic_level`, etc.) or their
    slices/index equivalent (`leader[5]`, `leader[7]`, etc.) to read and write
    values.

    See `LoC's documentation
    <https://www.loc.gov/marc/bibliographic/bd008.html>`_
    for more infos about those fields.

    .. code-block:: python
    import control_auth008
    from pymarc import MARCReader
     with open('test/marc.dat', 'rb') as fh:
        reader = MARCReader(fh)
            for record in reader:
                print(record['008'].data)   
                fld = record['008']
                ct_fld = control_auth008.Field008(record['008'].data)
                print (len(str(ct_fld)))
                print (f"{ct_fld.date_entered}=&&")
                #Change values
                ct_fld.date_entered = '123456'
                print (f"{ct_fld.date_entered}&&")

               
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
            raise BadLeaderValue(f"Date Entered is 6 chars field, got {value}")
        self._replace_values(position=0, value=value)

    @property
    def geographic_subdivision(self) -> str:
        """Type of date/publication status (06)."""
        return self.field008[6]

    @geographic_subdivision.setter
    def geographic_subdivision(self, value: str) -> None:
        """Type of date/publication status (06)."""
        if len(value) != 1:
            raise BadLeaderValue(f"Geographic subdivision is 1 char field, got {value}")
        self._replace_values(position=6, value=value)

    @property
    def romanization_scheme(self) -> str:
        """Date 1 (07-10)."""
        return self.field008[7]

    @romanization_scheme.setter
    def romanization_scheme(self, value: str) -> None:
        """romanization_scheme (07)."""
        if len(value) != 1:
            raise BadLeaderValue(f"romanization_scheme is 1 char 1 field, got {value}")
        self._replace_values(position=7, value=value)

    @property
    def catalog_language(self) -> str:
        """language (08)."""
        return self.field008[8]

    @catalog_language.setter
    def catalog_language(self, value: str) -> None:
        """catalog_language (08)."""
        if len(value) != 1:
            raise BadLeaderValue(f"Catalog language is 1 char field, got {value}")
        self._replace_values(position=8, value=value)

    @property
    def record_kind(self) -> str:
        """record_kind (09)."""
        return self.field008[9]

    @record_kind.setter
    def record_kind(self, value: str) -> None:
        """record_kind (09)."""
        if len(value) != 1:
            raise BadLeaderValue(f"Record kind is 1 chars field, got {value}")
        self._replace_values(position=9, value=value)

    @property
    def cataloging_rule(self) -> str:
        """cataloging_rule code (10)."""
        return self.field008[10]

    @cataloging_rule.setter
    def cataloging_rule(self, value: str) -> None:
        """cataloging_rule coding scheme (10)."""
        if len(value) != 1:
            raise BadLeaderValue(
                f"Cataloging_rule scheme is 1 char field, got {value}"
            )
        self._replace_values(position=10, value=value)

    @property
    def subject_system(self) -> str:
        """subject_system  (11)."""
        return self.field008[11]

    @subject_system.setter
    def subject_system(self, value: str) -> None:
        """subject_system  (11)."""
        if len(value) != 1:
            raise BadLeaderValue(f"Subject system is 1 char field, got {value}")
        self._replace_values(position=11, value=value)

    @property
    def series_type(self) -> str:
        """series_type  (12)."""
        return self.field008[12]

    @series_type.setter
    def series_type(self, value: str) -> None:
        """Subfield code count (12)."""
        if len(value) != 1:
            raise BadLeaderValue(f"Series type is 1 char field, got {value}")
        self._replace_values(position=12, value=value)
#
    @property
    def series_numbering(self) -> str:
        """series_numbering  (13)."""
        return self.field008[12]

    @series_numbering.setter
    def series_numbering(self, value: str) -> None:
        """series_numbering (13)."""
        if len(value) != 1:
            raise BadLeaderValue(f"Series_numbering is 1 char field, got {value}")
        self._replace_values(position=13, value=value)

    @property
    def heading_use(self) -> str:
        """Date 1 (14)."""
        return self.field008[14]

    @romanization_scheme.setter
    def heading_use(self, value: str) -> None:
        """heading_use (14)."""
        if len(value) != 1:
            raise BadLeaderValue(f"heading_use is char 1 field, got {value}")
        self._replace_values(position=14, value=value)

    @property
    def heading_use_suject(self) -> str:
        """heading_use_suject (15)."""
        return self.field008[15]

    @heading_use_suject.setter
    def heading_use_suject(self, value: str) -> None:
        """heading_use_suject (15)."""
        if len(value) != 1:
            raise BadLeaderValue(f"Heading_use_suject is 1 char field, got {value}")
        self._replace_values(position=15, value=value)

    @property
    def heading_use_series(self) -> str:
        """heading_use_series (16)."""
        return self.field008[16]

    @heading_use_series.setter
    def heading_use_series(self, value: str) -> None:
        """heading_use_series (16)."""
        if len(value) != 1:
            raise BadLeaderValue(f"Heading_use_series is 1 chars field, got {value}")
        self._replace_values(position=16, value=value)

    @property
    def subject_subdivision(self) -> str:
        """subject_subdivision code (17)."""
        return self.field008[17]

    @subject_subdivision.setter
    def subject_subdivision(self, value: str) -> None:
        """subject_subdivision coding scheme (17)."""
        if len(value) != 1:
            raise BadLeaderValue(
                f"subject_subdivision scheme is 1 char field, got {value}"
            )
        self._replace_values(position=17, value=value)

    @property
    def undefined(self) -> str:
        """undefined  (18-27)."""
        return self.field008[18:28]

    @undefined.setter
    def modified_record(self, value: str) -> None:
        """undefined  (18-27)."""
        if len(value) != 10:
            raise BadLeaderValue(f"undefined is 10 char field, got {value}")
        self._replace_values(position=18, value=value)

    @property
    def government_agency(self) -> str:
        """government_agency  (28)."""
        return self.field008[28]

    @government_agency.setter
    def government_agency(self, value: str) -> None:
        """Subfield code count (28)."""
        if len(value) != 1:
            raise BadLeaderValue(f"government_agency is 1 char field, got {value}")
        self._replace_values(position=28, value=value)
#2
    @property
    def reference_evalution(self) -> str:
        """reference_evalution  (29)."""
        return self.field008[29]

    @reference_evalution.setter
    def reference_evalution(self, value: str) -> None:
        """Subfield code count (29)."""
        if len(value) != 1:
            raise BadLeaderValue(f"reference_evalution is 1 char field, got {value}")
        self._replace_values(position=29, value=value)

    @property
    def undefined_30(self) -> str:
        """undefined_30  (30)."""
        return self.field008[30]

    @undefined_30.setter
    def undefined_30(self, value: str) -> None:
        """Subfield code count (30)."""
        if len(value) != 1:
            raise BadLeaderValue(f"undefined_30 is 1 char field, got {value}")
        self._replace_values(position=30, value=value)

    @property
    def record_update(self) -> str:
        """record_update  (31)."""
        return self.field008[31]

    @record_update.setter
    def record_update(self, value: str) -> None:
        """Subfield code count (31)."""
        if len(value) != 1:
            raise BadLeaderValue(f"record_update is 1 char field, got {value}")
        self._replace_values(position=31, value=value)

    @property
    def undefined_personal_name(self) -> str:
        """undefined_personal_name (32)."""
        return self.field008[32]

    @undefined_personal_name.setter
    def undefined_personal_name(self, value: str) -> None:
        """Subfield code count (32)."""
        if len(value) != 1:
            raise BadLeaderValue(f"undefined_personal_name is 1 char field, got {value}")
        self._replace_values(position=32, value=value)

    @property
    def establishment_level(self) -> str:
        """establishment_level (33)."""
        return self.field008[33]

    @establishment_level.setter
    def establishment_level(self, value: str) -> None:
        """establishment_level (33)."""
        if len(value) != 1:
            raise BadLeaderValue(f"establishment_level is 1 char field, got {value}")
        self._replace_values(position=33, value=value)

    @property
    def undefined_34(self) -> str:
        """undefined_34  (34)."""
        return self.field008[34:38]

    @undefined_34.setter
    def undefined_34(self, value: str) -> None:
        """Subfield code count (34-37)."""
        if len(value) != 4:
            raise BadLeaderValue(f"undefined_34 is 4 chars field, got {value}")
        self._replace_values(position=34, value=value)

    @property
    def modified_record(self) -> str:
        """modified_record  (38)."""
        return self.field008[38]

    @modified_record.setter
    def modified_record(self, value: str) -> None:
        """modified_record (38)."""
        if len(value) != 1:
            raise BadLeaderValue(f"modified_record is 1 char field, got {value}")
        self._replace_values(position=38, value=value)

    @property
    def cataloging_source(self) -> str:
        """cataloging_source  (39)."""
        return self.field008[39]

    @cataloging_source.setter
    def cataloging_source(self, value: str) -> None:
        """cataloging_source   (39)."""
        if len(value) != 1:
            raise BadLeaderValue(f"cataloging_source is 1 char field, got {value}")
        self._replace_values(position=39, value=value)
