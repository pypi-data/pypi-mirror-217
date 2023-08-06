#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2020-2023 NXP
#
# SPDX-License-Identifier: BSD-3-Clause
"""Module for crypto operations (certificate and key management).

Moreover, it includes SignatureProvider as an Interface for all potential signature providers.

It provides following functionality:

1. for the key management:

- generating RSA private key (size and exponent as parameter)
- generating RSA public key
- saving RSA private key to the file
- saving RSA public key to the file
- generating ECC private key (curve name as parameter)
- generating ECC public key
- saving ECC private key to the file
- saving ECC public key to the file

2. for certificate management:

- generating the x.509 certificate
- validating of a certificate
- validating of a chain of certificates
- returning public key from the given certificate
- converting a certificate into bytes
- saving a certificate into file

3. for general purpose:

- loading the public key from file
- loading the private key from file
- loading the x.509 certificate from file
"""
from typing import Union

import cryptography.hazmat.primitives.asymmetric.utils as utils_cryptography
from cryptography import x509

# Explicit import due to MYPY issue
from cryptography.exceptions import *
from cryptography.exceptions import InvalidSignature

# Explicit import due to MYPY issue
from cryptography.hazmat.backends import *
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends.openssl.rsa import *

# Explicit import due to MYPY issue
from cryptography.hazmat.primitives import *
from cryptography.hazmat.primitives import hashes, serialization

# Explicit import due to MYPY issue
from cryptography.hazmat.primitives.asymmetric import *
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa

# Explicit import due to MYPY issue
# Explicit import due to MYPY issue
from cryptography.hazmat.primitives.asymmetric.ec import *
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey,
    EllipticCurvePrivateKeyWithSerialization,
    EllipticCurvePublicKey,
    EllipticCurvePublicNumbers,
)

# Explicit import due to MYPY issue
from cryptography.hazmat.primitives.asymmetric.rsa import *  # type: ignore
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPrivateKeyWithSerialization,
    RSAPublicKey,
    RSAPublicNumbers,
)

# Explicit import due to MYPY issue
from cryptography.hazmat.primitives.serialization import *
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    load_der_private_key,
    load_der_public_key,
    load_pem_private_key,
    load_pem_public_key,
)

# Explicit import due to MYPY issue
from cryptography.x509 import *
from cryptography.x509 import (
    Certificate,
    CertificateSigningRequest,
    CRLEntryExtensionOID,
    ExtendedKeyUsageOID,
    ExtensionOID,
    NameOID,
    ObjectIdentifier,
    SignatureAlgorithmOID,
    load_der_x509_certificate,
    load_pem_x509_certificate,
)

PublicKey = Union[rsa.RSAPublicKey, ec.EllipticCurvePublicKey]
PrivateKey = Union[rsa.RSAPrivateKey, ec.EllipticCurvePrivateKey]

# These tuples are helpers for 'isinstance' checks
_PublicKeyTuple = (rsa.RSAPublicKey, ec.EllipticCurvePublicKey)
_PrivateKeyTuple = (rsa.RSAPrivateKey, ec.EllipticCurvePrivateKey)

# pylint: disable=wrong-import-position
from .certificate_management import *
from .keys_management import *

# Explicit import due to MYPY issue
from .loaders import load_certificate, load_certificate_as_bytes, load_private_key, load_public_key
