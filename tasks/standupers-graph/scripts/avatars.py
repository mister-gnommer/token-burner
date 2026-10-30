import hashlib
from datetime import datetime, timezone
from io import BytesIO
from http.client import HTTPException
from pathlib import Path
from shutil import copyfile
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from PIL import Image, ImageOps

PLACEHOLDER = Path(__file__).resolve().parents[1] / "graph/assets/laughing-person.svg"
MAX_BYTES = 5 * 1024 * 1024


def prepare_avatar(performer, output, fetch=True):
    assets = output / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    fallback = assets / "laughing-person.svg"
    if not fallback.exists():
        copyfile(PLACEHOLDER, fallback)
    raw_url = performer.get("image_url")
    url = urljoin(performer.get("profile_url") or "https://standup.pl/", raw_url) if raw_url else None
    avatar = {"path": "assets/laughing-person.svg", "source_url": url, "status": "placeholder"}
    if not url:
        avatar["reason"] = "no profile image"
        return avatar
    if urlparse(url).scheme != "https":
        avatar["reason"] = "profile image must use HTTPS"
        return avatar
    cached = assets / ("avatar-" + hashlib.sha256(url.encode()).hexdigest()[:20] + ".png")
    if cached.exists():
        try:
            with Image.open(cached) as image:
                image.verify()
            return {"path": f"assets/{cached.name}", "source_url": url, "status": "photo",
                    "retrieved_at": datetime.fromtimestamp(cached.stat().st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        except (OSError, ValueError, Image.DecompressionBombError):
            pass
    if not fetch:
        avatar["reason"] = "image not cached; render to download"
        return avatar
    try:
        request = Request(url, headers={"User-Agent": "standupers-graph/1.0"})
        with urlopen(request, timeout=5) as response:
            content = response.read(MAX_BYTES + 1)
        if len(content) > MAX_BYTES:
            raise ValueError("profile image exceeds 5 MiB")
        with Image.open(BytesIO(content)) as image:
            if image.width * image.height > 16_000_000:
                raise ValueError("profile image exceeds 16 megapixels")
            thumbnail = ImageOps.fit(ImageOps.exif_transpose(image).convert("RGB"), (160, 160))
            thumbnail.save(cached, "PNG")
        return {"path": f"assets/{cached.name}", "source_url": url, "status": "photo",
                "retrieved_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    except (OSError, ValueError, HTTPException, Image.DecompressionBombError) as error:
        avatar["reason"] = str(error)
        return avatar
