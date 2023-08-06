#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2019-2023 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Boot Image V2.0, V2.1."""

import logging
import os
from datetime import datetime
from typing import Iterator, List, Optional

from spsdk import SPSDKError
from spsdk.apps.utils import get_key
from spsdk.crypto.loaders import load_certificate_as_bytes
from spsdk.crypto.signature_provider import SignatureProvider
from spsdk.exceptions import SPSDKUnsupportedOperation
from spsdk.utils.crypto import CertBlockV2, Counter, crypto_backend
from spsdk.utils.crypto.abstract import BaseClass
from spsdk.utils.crypto.backend_internal import internal_backend
from spsdk.utils.crypto.certificate import Certificate
from spsdk.utils.crypto.common import calc_cypher_block_count
from spsdk.utils.misc import find_first, load_text, write_file

from . import sb_21_helper as elf2sb_helper21
from . import sly_bd_parser as bd_parser
from .commands import CmdHeader
from .headers import ImageHeaderV2
from .sections import BootSectionV2, CertSectionV2

logger = logging.getLogger(__name__)


class SBV2xAdvancedParams:
    """The class holds advanced parameters for the SB file encryption.

    These parameters are used for the tests; for production, use can use default values (random keys + current time)
    """

    @staticmethod
    def _create_nonce() -> bytes:
        """Return random nonce."""
        nonce = bytearray(crypto_backend().random_bytes(16))
        # clear nonce bit at offsets 31 and 63
        nonce[9] &= 0x7F
        nonce[13] &= 0x7F
        return bytes(nonce)

    def __init__(
        self,
        dek: Optional[bytes] = None,
        mac: Optional[bytes] = None,
        nonce: Optional[bytes] = None,
        timestamp: Optional[datetime] = None,
    ):
        """Initialize SBV2xAdvancedParams.

        :param dek: DEK key
        :param mac: MAC key
        :param nonce: nonce
        :param timestamp: fixed timestamp for the header; use None to use current date/time
        :raises SPSDKError: Invalid dek or mac
        :raises SPSDKError: Invalid length of nonce
        """
        self._dek: bytes = dek if dek else crypto_backend().random_bytes(32)
        self._mac: bytes = mac if mac else crypto_backend().random_bytes(32)
        self._nonce: bytes = nonce if nonce else SBV2xAdvancedParams._create_nonce()
        if timestamp is None:
            timestamp = datetime.now()
        self._timestamp = datetime.fromtimestamp(int(timestamp.timestamp()))
        if len(self._dek) != 32 and len(self._mac) != 32:
            raise SPSDKError("Invalid dek or mac")
        if len(self._nonce) != 16:
            raise SPSDKError("Invalid length of nonce")

    @property
    def dek(self) -> bytes:
        """Return DEK key."""
        return self._dek

    @property
    def mac(self) -> bytes:
        """Return MAC key."""
        return self._mac

    @property
    def nonce(self) -> bytes:
        """Return NONCE."""
        return self._nonce

    @property
    def timestamp(self) -> datetime:
        """Return timestamp."""
        return self._timestamp


########################################################################################################################
# Secure Boot Image Class (Version 2.0)
########################################################################################################################
class BootImageV20(BaseClass):
    """Boot Image V2.0 class."""

    # Image specific data
    # size of the MAC key
    HEADER_MAC_SIZE = 32
    # AES encrypted DEK and MAC, including padding
    DEK_MAC_SIZE = 32 + 32 + 16

    KEY_BLOB_SIZE = 80

    def __init__(
        self,
        signed: bool,
        kek: bytes,
        *sections: BootSectionV2,
        product_version: str = "1.0.0",
        component_version: str = "1.0.0",
        build_number: int = 0,
        advanced_params: SBV2xAdvancedParams = SBV2xAdvancedParams(),
    ) -> None:
        """Initialize Secure Boot Image V2.0.

        :param signed: True if image is signed, False otherwise
        :param kek: key for wrapping DEK and MAC keys
        :param product_version: The product version (default: 1.0.0)
        :param component_version: The component version (default: 1.0.0)
        :param build_number: The build number value (default: 0)
        :param advanced_params: Advanced parameters for encryption of the SB file, use for tests only
        :param sections: Boot sections
        :raises SPSDKError: Invalid dek or mac
        """
        self._kek = kek
        # Set Flags value
        self._signed = signed
        self._signature_provider: Optional[SignatureProvider] = None
        flags = 0x08 if self.signed else 0x04
        # Set private attributes
        self._dek: bytes = advanced_params.dek
        self._mac: bytes = advanced_params.mac
        if (
            len(self._dek) != self.HEADER_MAC_SIZE and len(self._mac) != self.HEADER_MAC_SIZE
        ):  # pragma: no cover # condition checked in SBV2xAdvancedParams constructor
            raise SPSDKError("Invalid dek or mac")
        self._header = ImageHeaderV2(
            version="2.0",
            product_version=product_version,
            component_version=component_version,
            build_number=build_number,
            flags=flags,
            nonce=advanced_params.nonce,
            timestamp=advanced_params.timestamp,
        )
        self._cert_section: Optional[CertSectionV2] = None
        self._boot_sections: List[BootSectionV2] = []
        # Generate nonce
        if self._header.nonce is None:
            nonce = bytearray(crypto_backend().random_bytes(16))
            # clear nonce bit at offsets 31 and 63
            nonce[9] &= 0x7F
            nonce[13] &= 0x7F
            self._header.nonce = bytes(nonce)
        # Sections
        for section in sections:
            self.add_boot_section(section)

    @property
    def header(self) -> ImageHeaderV2:
        """Return image header."""
        return self._header

    @property
    def dek(self) -> bytes:
        """Data encryption key."""
        return self._dek

    @property
    def mac(self) -> bytes:
        """Message authentication code."""
        return self._mac

    @property
    def kek(self) -> bytes:
        """Return key for wrapping DEK and MAC keys."""
        return self._kek

    @property
    def signature_provider(self) -> Optional[SignatureProvider]:
        """Signature provider instance to sign the final image.

        None if not assigned yet.
        """
        return self._signature_provider

    @signature_provider.setter
    def signature_provider(self, value: SignatureProvider) -> None:
        """Signature provider setter.

        :param value: Signature provider to sign final image
        """
        self._signature_provider = value

    @property
    def signed(self) -> bool:
        """Check whether sb is signed + encrypted or only encrypted."""
        return self._signed

    @property
    def cert_block(self) -> Optional[CertBlockV2]:
        """Return certificate block; None if SB file not signed or block not assigned yet."""
        cert_sect = self._cert_section
        if cert_sect is None:
            return None

        return cert_sect.cert_block

    @cert_block.setter
    def cert_block(self, value: Optional[CertBlockV2]) -> None:
        """Setter.

        :param value: block to be assigned; None to remove previously assigned block
        :raises SPSDKError: When certificate block is used when SB file is not signed
        """
        if value is not None:
            if not self.signed:
                raise SPSDKError("Certificate block cannot be used unless SB file is signed")
        self._cert_section = CertSectionV2(value) if value else None

    @property
    def cert_header_size(self) -> int:
        """Return image raw size (not aligned) for certificate header."""
        size = ImageHeaderV2.SIZE + self.HEADER_MAC_SIZE + self.KEY_BLOB_SIZE
        for boot_section in self._boot_sections:
            size += boot_section.raw_size
        return size

    @property
    def raw_size_without_signature(self) -> int:
        """Return image raw size without signature, used to calculate image blocks."""
        # Header, HMAC and KeyBlob
        size = ImageHeaderV2.SIZE + self.HEADER_MAC_SIZE + self.KEY_BLOB_SIZE
        # Certificates Section
        if self.signed:
            size += self.DEK_MAC_SIZE
            cert_block = self.cert_block
            if not cert_block:
                raise SPSDKError("Certification block not present")
            size += cert_block.raw_size
        # Boot Sections
        for boot_section in self._boot_sections:
            size += boot_section.raw_size
        return size

    @property
    def raw_size(self) -> int:
        """Return image raw size."""
        size = self.raw_size_without_signature

        if self.signed:
            cert_block = self.cert_block
            if not cert_block:  # pragma: no cover # already checked in raw_size_without_signature
                raise SPSDKError("Certificate block not present")
            size += cert_block.signature_size

        return size

    def __len__(self) -> int:
        return len(self._boot_sections)

    def __getitem__(self, key: int) -> BootSectionV2:
        return self._boot_sections[key]

    def __setitem__(self, key: int, value: BootSectionV2) -> None:
        self._boot_sections[key] = value

    def __iter__(self) -> Iterator[BootSectionV2]:
        return self._boot_sections.__iter__()

    def update(self) -> None:
        """Update boot image."""
        if self._boot_sections:
            self._header.first_boot_section_id = self._boot_sections[0].uid
            # calculate first boot tag block
            data_size = self._header.SIZE + self.HEADER_MAC_SIZE + self.KEY_BLOB_SIZE
            if self._cert_section is not None:
                data_size += self._cert_section.raw_size
            self._header.first_boot_tag_block = calc_cypher_block_count(data_size)
        # ...
        self._header.flags = 0x08 if self.signed else 0x04
        self._header.image_blocks = calc_cypher_block_count(self.raw_size_without_signature)
        self._header.header_blocks = calc_cypher_block_count(self._header.SIZE)
        self._header.max_section_mac_count = 0
        if self.signed:
            self._header.offset_to_certificate_block = (
                self._header.SIZE + self.HEADER_MAC_SIZE + self.KEY_BLOB_SIZE
            )
            self._header.offset_to_certificate_block += CmdHeader.SIZE + CertSectionV2.HMAC_SIZE * 2
            self._header.max_section_mac_count = 1
        for boot_sect in self._boot_sections:
            boot_sect.is_last = True  # this is unified with elftosb
            self._header.max_section_mac_count += boot_sect.hmac_count
        # Update certificates block header
        cert_blk = self.cert_block
        if cert_blk is not None:
            cert_blk.header.build_number = self._header.build_number
            cert_blk.header.image_length = self.cert_header_size

    def info(self) -> str:
        """Return text description of the instance."""
        self.update()
        nfo = "\n"
        nfo += ":::::::::::::::::::::::::::::::::: IMAGE HEADER ::::::::::::::::::::::::::::::::::::::\n"
        nfo += self._header.info()
        if self._cert_section is not None:
            nfo += "::::::::::::::::::::::::::::::: CERTIFICATES BLOCK ::::::::::::::::::::::::::::::::::::\n"
            nfo += self._cert_section.info()
        nfo += "::::::::::::::::::::::::::::::::::: BOOT SECTIONS ::::::::::::::::::::::::::::::::::::\n"
        for index, section in enumerate(self._boot_sections):
            nfo += f"[ SECTION: {index} | UID: 0x{section.uid:08X} ]\n"
            nfo += section.info()
        return nfo

    def add_boot_section(self, section: BootSectionV2) -> None:
        """Add new Boot section into image.

        :param section: Boot section
        :raises SPSDKError: Raised when section is not instance of BootSectionV2 class
        :raises SPSDKError: Raised when boot section has duplicate UID
        """
        if not isinstance(section, BootSectionV2):
            raise SPSDKError("Section is not instance of BootSectionV2 class")
        duplicate_uid = find_first(self._boot_sections, lambda bs: bs.uid == section.uid)
        if duplicate_uid is not None:
            raise SPSDKError(f"Boot section with duplicate UID: {str(section.uid)}")
        self._boot_sections.append(section)

    def export(self, padding: Optional[bytes] = None) -> bytes:
        """Serialize image object.

        :param padding: header padding (8 bytes) for testing purpose; None to use random values (recommended)
        :return: exported bytes
        :raises SPSDKError: Raised when there are no boot sections or is not signed or private keys are missing
        :raises SPSDKError: Raised when there is invalid dek or mac
        :raises SPSDKError: Raised when certificate data is not present
        :raises SPSDKError: Raised when there is invalid certificate block
        :raises SPSDKError: Raised when there is invalid length of exported data
        """
        if len(self.dek) != 32 or len(self.mac) != 32:
            raise SPSDKError("Invalid dek or mac")
        # validate params
        if not self._boot_sections:
            raise SPSDKError("No boot section")
        if self.signed and (self._cert_section is None):
            raise SPSDKError("Certificate section is required for signed images")
        # update internals
        self.update()
        # Add Image Header data
        data = self._header.export(padding=padding)
        # Add Image Header HMAC data
        data += crypto_backend().hmac(self.mac, data)
        # Add DEK and MAC keys
        data += crypto_backend().aes_key_wrap(self.kek, self.dek + self.mac)
        # Add Padding
        data += padding if padding else crypto_backend().random_bytes(8)
        # Add Certificates data
        if not self._header.nonce:
            raise SPSDKError("There is no nonce in the header")
        counter = Counter(self._header.nonce)
        counter.increment(calc_cypher_block_count(len(data)))
        if self._cert_section is not None:
            cert_sect_bin = self._cert_section.export(dek=self.dek, mac=self.mac, counter=counter)
            counter.increment(calc_cypher_block_count(len(cert_sect_bin)))
            data += cert_sect_bin
        # Add Boot Sections data
        for sect in self._boot_sections:
            data += sect.export(dek=self.dek, mac=self.mac, counter=counter)
        # Add Signature data
        if self.signed:
            if self.signature_provider is None:
                raise SPSDKError("Signature provider is not assigned, cannot sign the image.")
            if self.cert_block is None:
                raise SPSDKError("Certificate block is not assigned.")

            public_key = self.cert_block.certificates[-1].public_key
            try:
                result = self.signature_provider.verify_public_key(public_key.dump())
                if not result:
                    raise SPSDKError(
                        "Signature verification failed, public key does not match to certificate"
                    )
                logger.debug("The verification of private key pair integrity has been successful.")
            except SPSDKUnsupportedOperation:
                logger.warning(
                    "Signature provider could not verify the integrity of private key pair."
                )

            data += self.signature_provider.sign(data)

        if len(data) != self.raw_size:
            raise SPSDKError("Invalid length of exported data")
        return data

    # pylint: disable=too-many-locals
    @classmethod
    def parse(cls, data: bytes, offset: int = 0, kek: bytes = bytes()) -> "BootImageV20":
        """Parse image from bytes.

        :param data: Raw data of parsed image
        :param offset: The offset of input data
        :param kek: The Key for unwrapping DEK and MAC keys (required)
        :return: parsed image object
        :raises SPSDKError: raised when header is in wrong format
        :raises SPSDKError: raised when there is invalid header version
        :raises SPSDKError: raised when signature is incorrect
        :raises SPSDKError: Raised when kek is empty
        :raises SPSDKError: raised when header's nonce is not present
        """
        if not kek:
            raise SPSDKError("kek cannot be empty")
        index = offset
        header_raw_data = data[index : index + ImageHeaderV2.SIZE]
        index += ImageHeaderV2.SIZE
        header_mac_data = data[index : index + cls.HEADER_MAC_SIZE]
        index += cls.HEADER_MAC_SIZE
        key_blob = data[index : index + cls.KEY_BLOB_SIZE]
        index += cls.KEY_BLOB_SIZE
        key_blob_unwrap = crypto_backend().aes_key_unwrap(kek, key_blob[:-8])
        dek = key_blob_unwrap[:32]
        mac = key_blob_unwrap[32:]
        header_mac_data_calc = crypto_backend().hmac(mac, header_raw_data)
        if header_mac_data != header_mac_data_calc:
            raise SPSDKError("Invalid header MAC data")
        # Parse Header
        header = ImageHeaderV2.parse(header_raw_data)
        if header.version != "2.0":
            raise SPSDKError(f"Invalid Header Version: {header.version} instead 2.0")
        image_size = header.image_blocks * 16
        # Initialize counter
        if not header.nonce:
            raise SPSDKError("Header's nonce not present")
        counter = Counter(header.nonce)
        counter.increment(calc_cypher_block_count(index - offset))
        # ...
        signed = header.flags == 0x08
        adv_params = SBV2xAdvancedParams(
            dek=dek, mac=mac, nonce=header.nonce, timestamp=header.timestamp
        )
        obj = cls(
            signed,
            kek=kek,
            product_version=str(header.product_version),
            component_version=str(header.component_version),
            build_number=header.build_number,
            advanced_params=adv_params,
        )
        # Parse Certificate section
        if header.flags == 0x08:
            cert_sect = CertSectionV2.parse(data, index, dek=dek, mac=mac, counter=counter)
            obj._cert_section = cert_sect
            index += cert_sect.raw_size
            # Check Signature
            if not cert_sect.cert_block.verify_data(
                data[offset + image_size :], data[offset : offset + image_size]
            ):
                raise SPSDKError("Parsing Certification section failed")
        # Parse Boot Sections
        while index < (image_size + offset):
            boot_section = BootSectionV2.parse(data, index, dek=dek, mac=mac, counter=counter)
            obj.add_boot_section(boot_section)
            index += boot_section.raw_size
        return obj


########################################################################################################################
# Secure Boot Image Class (Version 2.1)
########################################################################################################################
class BootImageV21(BaseClass):
    """Boot Image V2.1 class."""

    # Image specific data
    HEADER_MAC_SIZE = 32
    KEY_BLOB_SIZE = 80
    SHA_256_SIZE = 32

    # defines
    FLAGS_SHA_PRESENT_BIT = 0x8000  # image contains SHA-256
    FLAGS_ENCRYPTED_SIGNED_BIT = 0x0008  # image is signed and encrypted

    def __init__(
        self,
        kek: bytes,
        *sections: BootSectionV2,
        product_version: str = "1.0.0",
        component_version: str = "1.0.0",
        build_number: int = 0,
        advanced_params: SBV2xAdvancedParams = SBV2xAdvancedParams(),
        flags: int = FLAGS_SHA_PRESENT_BIT | FLAGS_ENCRYPTED_SIGNED_BIT,
    ) -> None:
        """Initialize Secure Boot Image V2.1.

        :param kek: key to wrap DEC and MAC keys

        :param product_version: The product version (default: 1.0.0)
        :param component_version: The component version (default: 1.0.0)
        :param build_number: The build number value (default: 0)

        :param advanced_params: optional advanced parameters for encryption; it is recommended to use default value
        :param flags: see flags defined in class.
        :param sections: Boot sections
        """
        self._kek = kek
        self._signature_provider: Optional[
            SignatureProvider
        ] = None  # this should be assigned for export, not needed for parsing
        self._dek = advanced_params.dek
        self._mac = advanced_params.mac
        self._header = ImageHeaderV2(
            version="2.1",
            product_version=product_version,
            component_version=component_version,
            build_number=build_number,
            flags=flags,
            nonce=advanced_params.nonce,
            timestamp=advanced_params.timestamp,
        )
        self._cert_block: Optional[CertBlockV2] = None
        self.boot_sections: List[BootSectionV2] = []
        # ...
        for section in sections:
            self.add_boot_section(section)

    @property
    def header(self) -> ImageHeaderV2:
        """Return image header."""
        return self._header

    @property
    def dek(self) -> bytes:
        """Data encryption key."""
        return self._dek

    @property
    def mac(self) -> bytes:
        """Message authentication code."""
        return self._mac

    @property
    def kek(self) -> bytes:
        """Return key to wrap DEC and MAC keys."""
        return self._kek

    @property
    def signature_provider(self) -> Optional[SignatureProvider]:
        """Signature provider instance to sign the final image.

        None if not assigned yet.
        """
        return self._signature_provider

    @signature_provider.setter
    def signature_provider(self, value: SignatureProvider) -> None:
        """Signature provider setter.

        :param value: Signature provider to sign final image
        """
        self._signature_provider = value

    @property
    def cert_block(self) -> Optional[CertBlockV2]:
        """Return certificate block; None if SB file not signed or block not assigned yet."""
        return self._cert_block

    @cert_block.setter
    def cert_block(self, value: CertBlockV2) -> None:
        """Setter.

        :param value: block to be assigned; None to remove previously assigned block
        """
        assert isinstance(value, CertBlockV2)
        self._cert_block = value
        self._cert_block.alignment = 16

    @property
    def signed(self) -> bool:
        """Return flag whether SB file is signed."""
        return True  # SB2.1 is always signed

    @property
    def cert_header_size(self) -> int:
        """Return image raw size (not aligned) for certificate header."""
        size = ImageHeaderV2.SIZE + self.HEADER_MAC_SIZE
        size += self.KEY_BLOB_SIZE
        # Certificates Section
        cert_blk = self.cert_block
        if cert_blk:
            size += cert_blk.raw_size
        return size

    @property
    def raw_size(self) -> int:
        """Return image raw size (not aligned)."""
        # Header, HMAC and KeyBlob
        size = ImageHeaderV2.SIZE + self.HEADER_MAC_SIZE
        size += self.KEY_BLOB_SIZE
        # Certificates Section
        cert_blk = self.cert_block
        if cert_blk:
            size += cert_blk.raw_size
            if not self.signed:  # pragma: no cover # SB2.1 is always signed
                raise SPSDKError("Certificate block is not signed")
            size += cert_blk.signature_size
        # Boot Sections
        for boot_section in self.boot_sections:
            size += boot_section.raw_size
        return size

    def __len__(self) -> int:
        return len(self.boot_sections)

    def __getitem__(self, key: int) -> BootSectionV2:
        return self.boot_sections[key]

    def __setitem__(self, key: int, value: BootSectionV2) -> None:
        self.boot_sections[key] = value

    def __iter__(self) -> Iterator[BootSectionV2]:
        return self.boot_sections.__iter__()

    def update(self) -> None:
        """Update BootImageV21."""
        if self.boot_sections:
            self._header.first_boot_section_id = self.boot_sections[0].uid
            # calculate first boot tag block
            data_size = self._header.SIZE + self.HEADER_MAC_SIZE + self.KEY_BLOB_SIZE
            cert_blk = self.cert_block
            if cert_blk is not None:
                data_size += cert_blk.raw_size
                if not self.signed:  # pragma: no cover # SB2.1 is always signed
                    raise SPSDKError("Certificate block is not signed")
                data_size += cert_blk.signature_size
            self._header.first_boot_tag_block = calc_cypher_block_count(data_size)
        # ...
        self._header.image_blocks = calc_cypher_block_count(self.raw_size)
        self._header.header_blocks = calc_cypher_block_count(self._header.SIZE)
        self._header.offset_to_certificate_block = (
            self._header.SIZE + self.HEADER_MAC_SIZE + self.KEY_BLOB_SIZE
        )
        # Get HMAC count
        self._header.max_section_mac_count = 0
        for boot_sect in self.boot_sections:
            boot_sect.is_last = True  # unified with elftosb
            self._header.max_section_mac_count += boot_sect.hmac_count
        # Update certificates block header
        cert_clk = self.cert_block
        if cert_clk is not None:
            cert_clk.header.build_number = self._header.build_number
            cert_clk.header.image_length = self.cert_header_size

    def info(self) -> str:
        """Return text description of the instance."""
        self.update()
        nfo = "\n"
        nfo += ":::::::::::::::::::::::::::::::::: IMAGE HEADER ::::::::::::::::::::::::::::::::::::::\n"
        nfo += self._header.info()
        if self.cert_block is not None:
            nfo += "::::::::::::::::::::::::::::::: CERTIFICATES BLOCK ::::::::::::::::::::::::::::::::::::\n"
            nfo += self.cert_block.info()
        nfo += "::::::::::::::::::::::::::::::::::: BOOT SECTIONS ::::::::::::::::::::::::::::::::::::\n"
        for index, section in enumerate(self.boot_sections):
            nfo += f"[ SECTION: {index} | UID: 0x{section.uid:08X} ]\n"
            nfo += section.info()
        return nfo

    def add_boot_section(self, section: BootSectionV2) -> None:
        """Add new Boot section into image.

        :param section: Boot section to be added
        :raises SPSDKError: Raised when section is not instance of BootSectionV2 class
        """
        if not isinstance(section, BootSectionV2):
            raise SPSDKError("Section is not instance of BootSectionV2 class")
        self.boot_sections.append(section)

    # pylint: disable=too-many-locals
    def export(
        self, padding: Optional[bytes] = None, dbg_info: Optional[List[str]] = None
    ) -> bytes:
        """Serialize image object.

        :param padding: header padding (8 bytes) for testing purpose; None to use random values (recommended)
        :param dbg_info: optional list, where debug info is exported in text form
        :return: exported bytes
        :raises SPSDKError: Raised when there is no boot section to be added
        :raises SPSDKError: Raised when certificate is not assigned
        :raises SPSDKError: Raised when private key is not assigned
        :raises SPSDKError: Raised when private header's nonce is invalid
        :raises SPSDKError: Raised when private key does not match certificate
        :raises SPSDKError: Raised when there is no debug info
        """
        # validate params
        if not self.boot_sections:
            raise SPSDKError("At least one Boot Section must be added")
        if self.cert_block is None:
            raise SPSDKError("Certificate is not assigned")
        if self.signature_provider is None:
            raise SPSDKError("Signature provider is not assigned, cannot sign the image")
        # Update internals
        if dbg_info is not None:
            dbg_info.append("[sb_file]")
        bs_dbg_info: Optional[List[str]] = [] if dbg_info else None
        self.update()
        # Export Boot Sections
        bs_data = bytes()
        bs_offset = (
            ImageHeaderV2.SIZE
            + self.HEADER_MAC_SIZE
            + self.KEY_BLOB_SIZE
            + self.cert_block.raw_size
            + self.cert_block.signature_size
        )
        if self.header.flags & self.FLAGS_SHA_PRESENT_BIT:
            bs_offset += self.SHA_256_SIZE

        if not self._header.nonce:
            raise SPSDKError("Invalid header's nonce")
        counter = Counter(self._header.nonce, calc_cypher_block_count(bs_offset))
        for sect in self.boot_sections:
            bs_data += sect.export(
                dek=self.dek, mac=self.mac, counter=counter, dbg_info=bs_dbg_info
            )
        # Export Header
        signed_data = self._header.export(padding=padding)
        if dbg_info:
            dbg_info.append("[header]")
            dbg_info.append(signed_data.hex())
        #  Add HMAC data
        first_bs_hmac_count = self.boot_sections[0].hmac_count
        hmac_data = bs_data[CmdHeader.SIZE : CmdHeader.SIZE + (first_bs_hmac_count * 32) + 32]
        hmac = crypto_backend().hmac(self.mac, hmac_data)
        signed_data += hmac
        if dbg_info:
            dbg_info.append("[hmac]")
            dbg_info.append(hmac.hex())
        # Add KeyBlob data
        key_blob = crypto_backend().aes_key_wrap(self.kek, self.dek + self.mac)
        key_blob += b"\00" * (self.KEY_BLOB_SIZE - len(key_blob))
        signed_data += key_blob
        if dbg_info:
            dbg_info.append("[key_blob]")
            dbg_info.append(key_blob.hex())
        # Add Certificates data
        signed_data += self.cert_block.export()
        if dbg_info:
            dbg_info.append("[cert_block]")
            dbg_info.append(self.cert_block.export().hex())
        # Add SHA-256 of Bootable sections if requested
        if self.header.flags & self.FLAGS_SHA_PRESENT_BIT:
            signed_data += internal_backend.hash(bs_data)

        # Add Signature data
        public_key = self.cert_block.certificates[-1].public_key
        try:
            result = self.signature_provider.verify_public_key(public_key.dump())
            if not result:
                raise SPSDKError(
                    "Signature verification failed, public key does not match to certificate"
                )
            logger.debug("The verification of private key pair integrity has been successful.")
        except SPSDKUnsupportedOperation:
            logger.warning("Signature provider could not verify the integrity of private key pair.")

        signature = self.signature_provider.sign(signed_data)
        if dbg_info:
            dbg_info.append("[signature]")
            dbg_info.append(signature.hex())
            dbg_info.append("[boot_sections]")
            if not bs_dbg_info:
                raise SPSDKError("No debug information")
            dbg_info.extend(bs_dbg_info)
        return signed_data + signature + bs_data

    # pylint: disable=too-many-locals
    @classmethod
    def parse(
        cls,
        data: bytes,
        offset: int = 0,
        kek: bytes = bytes(),
        plain_sections: bool = False,
    ) -> "BootImageV21":
        """Parse image from bytes.

        :param data: Raw data of parsed image
        :param offset: The offset of input data
        :param kek: The Key for unwrapping DEK and MAC keys (required)
        :param plain_sections: Sections are not encrypted; this is used only for debugging,
            not supported by ROM code
        :return: BootImageV21 parsed object
        :raises SPSDKError: raised when header is in incorrect format
        :raises SPSDKError: raised when signature is incorrect
        :raises SPSDKError: Raised when kek is empty
        :raises SPSDKError: raised when header's nonce not present"
        """
        if not kek:
            raise SPSDKError("kek cannot be empty")
        index = offset
        header_raw_data = data[index : index + ImageHeaderV2.SIZE]
        index += ImageHeaderV2.SIZE
        # Not used right now: hmac_data = data[index: index + cls.HEADER_MAC_SIZE]
        index += cls.HEADER_MAC_SIZE
        key_blob = data[index : index + cls.KEY_BLOB_SIZE]
        index += cls.KEY_BLOB_SIZE
        key_blob_unwrap = crypto_backend().aes_key_unwrap(kek, key_blob[:-8])
        dek = key_blob_unwrap[:32]
        mac = key_blob_unwrap[32:]
        # Parse Header
        header = ImageHeaderV2.parse(header_raw_data)
        if header.offset_to_certificate_block != (index - offset):
            raise SPSDKError("Invalid offset")
        # Parse Certificate Block
        cert_block = CertBlockV2.parse(data, index)
        index += cert_block.raw_size

        # Verify Signature
        signature_index = index
        # The image may contain SHA, in such a case the signature is placed
        # after SHA. Thus we must shift the index by SHA size.
        if header.flags & BootImageV21.FLAGS_SHA_PRESENT_BIT:
            signature_index += BootImageV21.SHA_256_SIZE
        result = cert_block.verify_data(
            data[signature_index : signature_index + cert_block.signature_size],
            data[offset:signature_index],
        )

        if not result:
            raise SPSDKError("Verification failed")
        # Check flags, if 0x8000 bit is set, the SB file contains SHA-256 between
        # certificate and signature.
        if header.flags & BootImageV21.FLAGS_SHA_PRESENT_BIT:
            bootable_section_sha256 = data[index : index + BootImageV21.SHA_256_SIZE]
            index += BootImageV21.SHA_256_SIZE
        index += cert_block.signature_size
        # Check first Boot Section HMAC
        # Not implemented yet
        # hmac_data_calc = crypto_backend().hmac(mac, data[index + CmdHeader.SIZE: index + CmdHeader.SIZE + ((2) * 32)])
        # if hmac_data != hmac_data_calc:
        #    raise SPSDKError("HMAC failed")
        if not header.nonce:
            raise SPSDKError("Header's nonce not present")
        counter = Counter(header.nonce)
        counter.increment(calc_cypher_block_count(index - offset))
        boot_section = BootSectionV2.parse(
            data, index, dek=dek, mac=mac, counter=counter, plain_sect=plain_sections
        )
        if header.flags & BootImageV21.FLAGS_SHA_PRESENT_BIT:
            computed_bootable_section_sha256 = internal_backend.hash(
                data[index:], algorithm="sha256"
            )

            if bootable_section_sha256 != computed_bootable_section_sha256:
                raise SPSDKError(
                    desc=(
                        "Error: invalid Bootable section SHA."
                        f"Expected {bootable_section_sha256.decode('utf-8')},"
                        f"got {computed_bootable_section_sha256.decode('utf-8')}"
                    )
                )
        adv_params = SBV2xAdvancedParams(
            dek=dek, mac=mac, nonce=header.nonce, timestamp=header.timestamp
        )
        obj = cls(
            kek=kek,
            product_version=str(header.product_version),
            component_version=str(header.component_version),
            build_number=header.build_number,
            advanced_params=adv_params,
        )
        obj.cert_block = cert_block
        obj.add_boot_section(boot_section)
        return obj


def generate_SB21(  # pylint: disable=invalid-name
    bd_file_path: str,
    key_file_path: str,
    signature_provider: SignatureProvider,
    signing_certificate_file_paths: List[str],
    root_key_certificate_paths: List[str],
    hoh_out_path: str,
    external_files: List[str],
) -> bytes:
    """Generate SecureBinary image from BD command file.

    :param bd_file_path: path to BD file.
    :param key_file_path: path to key file.
    :param signature_provider: Signature provider to sign final image
    :param signing_certificate_file_paths: signing certificate chain.
    :param root_key_certificate_paths: paths to root key certificate(s) for
        verifying other certificates. Only 4 root key certificates are allowed,
        others are ignored. One of the certificates must match the first certificate
        passed in signing_certificate_file_paths.
    :param hoh_out_path: output path to hash of hashes of root keys. If set to
        None, 'hash.bin' is created under working directory.
    :param external_files: external files referenced from BD file.

    :raises SPSDKError: If incorrect bd file is provided
    """
    # Create lexer and parser, load the BD file content and parse it for
    # further execution - the parsed BD file is a dictionary in JSON format
    bd_file_content = load_text(bd_file_path)

    parser = bd_parser.BDParser()

    parsed_bd_file = parser.parse(text=bd_file_content, extern=external_files)
    if parsed_bd_file is None:
        raise SPSDKError("Invalid bd file, secure binary file generation terminated")

    # The dictionary contains following content:
    # {
    #   options: {
    #       opt1: value,...
    #   },
    #   sections: [
    #       {section_id: value, options: {}, commands: {}},
    #       {section_id: value, options: {}, commands: {}}
    #   ]
    # }
    # TODO check, that section_ids differ in sections???

    # we need to encrypt and sign the image, let's check, whether we have
    # everything we need
    # It appears, that flags option in BD file are irrelevant for 2.1 secure
    # binary images regarding encryption/signing - SB 2.1 must be encrypted
    # and signed.
    # However, bit 15 represents, whether the final SB 2.1 must include a
    # SHA-256 of the bootable section.
    flags = parsed_bd_file["options"].get(
        "flags", BootImageV21.FLAGS_SHA_PRESENT_BIT | BootImageV21.FLAGS_ENCRYPTED_SIGNED_BIT
    )
    if (
        signature_provider is None
        or signing_certificate_file_paths is None
        or root_key_certificate_paths is None
    ):
        raise SPSDKError(
            "error: Signed image requires private key with -s option, "
            "one or more certificate(s) using -S option and one or more root key "
            "certificates using -R option"
        )

    # Versions and build number are up to the user. If he doesn't provide any,
    # we set these to following values.
    product_version = parsed_bd_file["options"].get("productVersion", "")
    component_version = parsed_bd_file["options"].get("componentVersion", "")
    build_number = parsed_bd_file["options"].get("buildNumber", -1)

    if not product_version:
        product_version = "1.0.0"
        logger.warning("Production version not defined, defaults to '1.0.0'")

    if not component_version:
        component_version = "1.0.0"
        logger.warning("Component version not defined, defaults to '1.0.0'")

    if build_number == -1:
        build_number = 1
        logger.warning("Build number not defined, defaults to '1.0.0'")

    if key_file_path is None:
        # Legacy elf2sb doesn't report no key provided, but this should
        # be definitely reported to tell the user, what kind of key is being
        # used
        logger.warning("No KEK key provided, using a zero KEK key")
        sb_kek = bytes.fromhex("0" * 64)
    else:
        sb_kek = get_key(key_file_path, expected_size=32)

    # validate keyblobs and perform appropriate actions
    keyblobs = parsed_bd_file.get("keyblobs", [])

    # Based on content of parsed BD file, create a BootSectionV2 and assign
    # commands to them.
    # The content of section looks like this:
    # sections: [
    #   {
    #       section_id: <number>,
    #       options: {}, this is left empty for now...
    #       commands: [
    #           {<cmd1>: {<param1>: value, ...}},
    #           {<cmd2>: {<param1>: value, ...}},
    #           ...
    #       ]
    #   },
    #   {
    #       section_id: <number>,
    #       ...
    #   }
    # ]
    sb_sections = []
    bd_sections = parsed_bd_file["sections"]
    for bd_section in bd_sections:
        section_id = bd_section["section_id"]
        commands = []
        for cmd in bd_section["commands"]:
            for key, value in cmd.items():
                # we use a helper function, based on the key ('load', 'erase'
                # etc.) to create a command object. The helper function knows
                # how to handle the parameters of each command.
                cmd_fce = elf2sb_helper21.get_command(key)
                if key in ("keywrap", "encrypt"):
                    keyblob = {"keyblobs": keyblobs}
                    value.update(keyblob)
                cmd = cmd_fce(value)
                commands.append(cmd)

        sb_sections.append(BootSectionV2(section_id, *commands))

    # We have a list of sections and their respective commands, lets create
    # a boot image v2.1 object
    secure_binary = BootImageV21(
        sb_kek,
        *sb_sections,
        product_version=product_version,
        component_version=component_version,
        build_number=build_number,
        flags=flags,
    )

    # create certificate block
    cert_block = CertBlockV2(build_number=build_number)
    for cert_path in signing_certificate_file_paths:
        cert_data = load_certificate_as_bytes(str(cert_path))
        cert_block.add_certificate(cert_data)
    for cert_idx, cert_path in enumerate(root_key_certificate_paths):
        cert_data = load_certificate_as_bytes(str(cert_path))
        cert_block.set_root_key_hash(cert_idx, Certificate(cert_data))

    # We have our secure binary, now we attach to it the certificate block and
    # the private key content
    secure_binary.cert_block = cert_block
    secure_binary.signature_provider = signature_provider

    if hoh_out_path is None:
        hoh_out_path = os.path.join(os.getcwd(), "hash.bin")

    write_file(secure_binary.cert_block.rkht, hoh_out_path, mode="wb")

    return secure_binary.export()
