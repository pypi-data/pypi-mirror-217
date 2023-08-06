#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2019-2023 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Module for base abstract classes."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from spsdk.crypto import PrivateKey


########################################################################################################################
# Abstract Class for Security Backend
########################################################################################################################
class BackendClass(ABC):
    """Abstract Class for Security Backend."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Backend Name."""

    @property
    @abstractmethod
    def version(self) -> str:
        """Backend Version."""

    @abstractmethod
    def random_bytes(self, length: int) -> bytes:
        """Return a random byte string with specified length.

        :param length: The length in bytes
        """

    @abstractmethod
    def hash(self, data: bytes, algorithm: str = "sha256") -> bytes:
        """Return a HASH from input data with specified algorithm.

        :param data: Input data in bytes
        :param algorithm: Algorithm type for HASH function
        """

    @abstractmethod
    def hmac(self, key: bytes, data: bytes, algorithm: str = "sha256") -> bytes:
        """Return a HMAC from data with specified key and algorithm.

        :param key: The key in bytes format
        :param data: Input data in bytes format
        :param algorithm: Algorithm type for HASH function (sha256, sha384, sha512, ...)
        """

    @abstractmethod
    def aes_key_wrap(self, kek: bytes, key_to_wrap: bytes) -> bytes:
        """Wraps a key using a key-encrypting key (KEK).

        :param kek: The key-encrypting key
        :param key_to_wrap: Plain data
        """

    @abstractmethod
    def aes_key_unwrap(self, kek: bytes, wrapped_key: bytes) -> bytes:
        """Unwraps a key using a key-encrypting key (KEK).

        :param kek: The key-encrypting key
        :param wrapped_key: Encrypted data
        """

    @abstractmethod
    def aes_ctr_encrypt(self, key: bytes, plain_data: bytes, nonce: bytes) -> bytes:
        """Encrypt plain data with AES in CTR mode.

        :param key: The key for data encryption
        :param plain_data: Input data
        :param nonce: Nonce data with counter value
        """

    @abstractmethod
    def aes_ctr_decrypt(self, key: bytes, encrypted_data: bytes, nonce: bytes) -> bytes:
        """Decrypt encrypted data with AES in CTR mode.

        :param key: The key for data decryption
        :param encrypted_data: Input data
        :param nonce: Nonce data with counter value
        """

    @abstractmethod
    def aes_xts_encrypt(self, key: bytes, plain_data: bytes, tweak: bytes) -> bytes:
        """Encrypt plain data with AES in XTS mode.

        :param key: The key for data encryption
        :param plain_data: Input data
        :param tweak: The tweak is a 16 byte value
        """

    @abstractmethod
    def aes_xts_decrypt(self, key: bytes, encrypted_data: bytes, tweak: bytes) -> bytes:
        """Decrypt encrypted data with AES in XTS mode.

        :param key: The key for data decryption
        :param encrypted_data: Input data
        :param tweak: The tweak is a 16 byte value
        """

    @abstractmethod
    def aes_cbc_encrypt(
        self, key: bytes, plain_data: bytes, iv_data: Optional[bytes] = None
    ) -> bytes:
        """Encrypt plain data with AES in CBC mode.

        :param key: The key for data encryption
        :param plain_data: Input data
        :param iv_data: Initialization vector data
        """

    @abstractmethod
    def aes_cbc_decrypt(
        self, key: bytes, encrypted_data: bytes, iv_data: Optional[bytes] = None
    ) -> bytes:
        """Decrypt encrypted data with AES in CBC mode.

        :param key: The key for data decryption
        :param encrypted_data: Input data
        :param iv_data: Initialization vector data
        """

    @abstractmethod
    def rsa_sign(self, private_key: bytes, data: bytes, algorithm: str = "sha256") -> bytes:
        """Sign input data.

        :param private_key: The private key
        :param data: Input data
        :param algorithm: Used algorithm
        """

    @abstractmethod
    def rsa_verify(
        self,
        pub_key_mod: int,
        pub_key_exp: int,
        signature: bytes,
        data: bytes,
        algorithm: str = "sha256",
    ) -> bool:
        """Verify input data.

        :param pub_key_mod: The private key modulus
        :param pub_key_exp: The private key exponent
        :param signature: The signature of input data
        :param data: Input data
        :param algorithm: Used algorithm
        """

    @abstractmethod
    def rsa_public_key(self, modulus: int, exponent: int) -> Any:
        """Create RSA public key object from modulus and exponent.

        :param modulus: The RSA public key modulus
        :param exponent: The RSA public key exponent
        """

    @abstractmethod
    def ecc_sign(self, private_key: bytes, data: bytes, algorithm: Optional[str] = None) -> bytes:
        """Sign data using (EC)DSA.

        :param private_key: ECC private key
        :param data: Data to sign
        :param algorithm: Hash algorithm, if None the hash length is determined from ECC curve size
        :return: Signature, r and s coordinates as bytes
        """

    @abstractmethod
    def ecc_verify(
        self, public_key: bytes, signature: bytes, data: bytes, algorithm: Optional[str] = None
    ) -> bool:
        """Verify (EC)DSA signature.

        :param public_key: ECC public key
        :param signature: Signature to verify, r and s coordinates as bytes
        :param data: Data to validate
        :param algorithm: Hash algorithm, if None the hash length is determined from ECC curve size
        :return: True if the signature is valid
        :raises SPSDKError: Signature length is invalid
        """

    @staticmethod
    @abstractmethod
    def sign_size(key: PrivateKey) -> int:
        """Get size of signature for loaded private key.

        :param key: Private key used to sign data.
        :return: Size of signature in bytes for the private key.
        :raises SPSDKError: Invalid key type.
        """


########################################################################################################################
# Abstract Class for Data Classes
########################################################################################################################
# TODO Refactor: this class should not be part of crypto module
class BaseClass(ABC):
    """Abstract Class for Data Classes."""

    def __eq__(self, obj: Any) -> bool:
        """Check object equality."""
        return isinstance(obj, self.__class__) and vars(obj) == vars(self)

    def __ne__(self, obj: Any) -> bool:
        return not self.__eq__(obj)

    def __str__(self) -> str:
        """Object description in string format."""
        return self.info()

    @abstractmethod
    def info(self) -> str:
        """Object description in string format."""

    @abstractmethod
    def export(self) -> bytes:
        """Serialize object into bytes array."""

    @classmethod
    @abstractmethod
    def parse(cls, data: bytes, offset: int = 0) -> "BaseClass":
        """Deserialize object from bytes array."""
