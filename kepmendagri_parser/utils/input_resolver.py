import hashlib
import logging
import tempfile
import urllib.parse
from pathlib import Path
from urllib.request import urlopen

from tqdm import tqdm


logger = logging.getLogger(__name__)
CHUNK_SIZE = 8192


def is_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return parsed.scheme in ("http", "https")


def download_file(
    url: str,
    expected_sha256: str | None = None,
    debug_level: int = 0,
) -> Path:
    """
    Download PDF from URL into a temporary directory with progress bar.
    """

    if debug_level >= 1:
        logger.info("Downloading source PDF from URL")
        logger.info("URL: %s", url)

    tmp_dir = Path(tempfile.mkdtemp(prefix="kepmendagri_"))
    target = tmp_dir / "source.pdf"

    if debug_level >= 2:
        logger.debug("Temporary directory created: %s", tmp_dir)
        logger.debug("Writing PDF to: %s", target)

    h = hashlib.sha256()
    total_bytes = 0

    with urlopen(url) as r:
        content_length = r.headers.get("Content-Length")
        total_size = int(content_length) if content_length else None

        with open(target, "wb") as f, tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc="Downloading PDF",
            disable=False,  # tqdm auto-disable on non-TTY
        ) as pbar:
            while True:
                chunk = r.read(CHUNK_SIZE)
                if not chunk:
                    break
                f.write(chunk)
                h.update(chunk)
                chunk_size = len(chunk)
                total_bytes += chunk_size
                pbar.update(chunk_size)

    if debug_level >= 1:
        logger.info("Download completed (%d bytes)", total_bytes)

    if expected_sha256:
        actual = h.hexdigest()

        if debug_level >= 1:
            logger.info("Verifying SHA256 checksum")

        if actual != expected_sha256:
            logger.error(
                "SHA256 mismatch: expected=%s actual=%s",
                expected_sha256,
                actual,
            )
            raise ValueError(
                f"SHA256 mismatch: expected {expected_sha256}, got {actual}"
            )

        if debug_level >= 1:
            logger.info("SHA256 checksum verified")

    return target
