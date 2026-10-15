"""Pure byte-level derivation of the frozen Gameplay V0 -> V1 edit."""

import hashlib


GAMEPLAY_V0_SHA256 = "571e2a5ce3f0630972f2fbe4e9a6a3c376bcf4d1a74589d14c882b2ee0db1423"
GAMEPLAY_V1_SHA256 = "b8a2cac2c5731407c7126ae2121d28cbceffed2e065cb18488e3379282feccb8"
GAMEPLAY_V0_BYTES = 12382
GAMEPLAY_V1_BYTES = 12453
UTF8_BOM = b"\xef\xbb\xbf"

REPLACEMENTS = (
    (
        b"      Score : int\r\n      Lives : int }",
        b"      Score : int\r\n      Lives : int\r\n      BrickReward : int }",
    ),
    (
        b"          Score = 0\r\n          Lives = 0 }",
        b"          Score = 0\r\n          Lives = 0\r\n          BrickReward = 200 }",
    ),
    (
        b"                let scoring = Map.count bricksIntersected * 100",
        b"                let scoring = Map.count bricksIntersected * gameplay.BrickReward",
    ),
)


def sha256(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def newline_counts(body: bytes) -> tuple[int, int]:
    crlf = body.count(b"\r\n")
    bare_lf = body.count(b"\n") - crlf
    return crlf, bare_lf


def require_v0(body: bytes) -> None:
    if len(body) != GAMEPLAY_V0_BYTES or sha256(body) != GAMEPLAY_V0_SHA256:
        raise ValueError("Gameplay V0 byte identity differs")
    if not body.startswith(UTF8_BOM):
        raise ValueError("Gameplay V0 UTF-8 BOM is missing")
    crlf, bare_lf = newline_counts(body)
    if crlf != 305 or bare_lf != 0:
        raise ValueError(f"Gameplay V0 newline identity differs: CRLF={crlf}, bare-LF={bare_lf}")


def derive_v1(body: bytes) -> bytes:
    require_v0(body)
    derived = body
    for old, new in REPLACEMENTS:
        if derived.count(old) != 1 or derived.count(new) != 0:
            raise ValueError("Gameplay edit-anchor count differs")
        derived = derived.replace(old, new, 1)
    if len(derived) != GAMEPLAY_V1_BYTES or sha256(derived) != GAMEPLAY_V1_SHA256:
        raise ValueError("derived Gameplay V1 byte identity differs")
    if not derived.startswith(UTF8_BOM):
        raise ValueError("derived Gameplay V1 UTF-8 BOM is missing")
    crlf, bare_lf = newline_counts(derived)
    if crlf != 307 or bare_lf != 0:
        raise ValueError(f"Gameplay V1 newline identity differs: CRLF={crlf}, bare-LF={bare_lf}")
    return derived


def require_arm(body: bytes, arm: str) -> None:
    if arm == "v0":
        require_v0(body)
    elif arm == "v1":
        expected = derive_v1_source_identity(body)
        if expected != GAMEPLAY_V1_SHA256:
            raise ValueError("Gameplay V1 identity differs")
    else:
        raise ValueError(f"unknown arm {arm!r}")


def derive_v1_source_identity(body: bytes) -> str:
    if len(body) != GAMEPLAY_V1_BYTES or sha256(body) != GAMEPLAY_V1_SHA256:
        raise ValueError("Gameplay V1 byte identity differs")
    if not body.startswith(UTF8_BOM):
        raise ValueError("Gameplay V1 UTF-8 BOM is missing")
    crlf, bare_lf = newline_counts(body)
    if crlf != 307 or bare_lf != 0:
        raise ValueError(f"Gameplay V1 newline identity differs: CRLF={crlf}, bare-LF={bare_lf}")
    return sha256(body)
