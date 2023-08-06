import typing as t
from contextlib import asynccontextmanager
from contextlib import suppress
from dataclasses import dataclass
from functools import lru_cache

from gcloud.aio.storage import Blob
from gcloud.aio.storage.bucket import Bucket
from gcloud.aio.storage.storage import Storage
from google.api_core.exceptions import BadRequest
from . import AsyncBlob
from . import AsyncBucket
from . import AsyncBucketClient
from . import AsyncBucketEntry
from . import AsyncPathy

from . import AsyncPurePathy
from . import register_client


class BucketEntryGCS(AsyncBucketEntry):
    bucket: "Bucket"
    raw: Blob


@dataclass
class BlobGCS(AsyncBlob):
    async def delete(self) -> None:
        await self.raw.delete()

    async def exists(self) -> bool:
        return await self.raw.exists()


class BucketClientGCS(AsyncBucketClient):
    client: Storage
    configs: dict

    @lru_cache
    def get_client(self):
        return Storage(**self.configs)

    @asynccontextmanager
    async def session(self) -> Storage:
        async with self.get_client() as client:
            yield client

    @property
    def client_params(self) -> dict:
        return dict(client=self.client)

    def __init__(self, **kwargs: t.Any) -> None:
        self.configs = kwargs
        self.recreate()

    def recreate(self) -> None:
        creds = self.configs["credentials"] if "credentials" in self.configs else None
        if creds is not None:
            self.configs["project"] = creds.project_id
        self.get_client()

    def make_uri(self, path: AsyncPurePathy) -> str:
        return str(path)

    async def create_bucket(self, path: AsyncPurePathy) -> Bucket:
        async with self.session() as session:
            return await session.create_bucket(path.root)

    async def delete_bucket(self, path: AsyncPurePathy) -> None:
        async with self.session() as client:
            bucket = client.get_bucket(path.root)
            await bucket.delete()

    async def exists(self, path: AsyncPurePathy) -> bool:
        # Because we want all the parents of a valid blob (e.g. "directory" in
        # "directory/foo.file") to return True, we enumerate the blobs with a prefix
        # and compare the object names to see if they match a substring of the path
        key_name = str(path.key)
        async for blob in self.list_blobs(path):
            if blob.name.startswith(key_name + path._flavour.sep):
                return True
        return False

    async def lookup_bucket(self, path: AsyncPurePathy) -> t.Optional["BucketGCS"]:
        try:
            return await self.get_bucket(path)
        except FileNotFoundError:
            return None

    async def get_bucket(self, path: AsyncPurePathy) -> "BucketGCS":
        async with self.session() as client:
            native_bucket: t.Any = client.bucket(path.root)
            with suppress(BadRequest):
                if await native_bucket.exists():
                    return BucketGCS(str(path.root), bucket=native_bucket)
            raise FileNotFoundError(f"Bucket {path.root} does not exist!")

    async def list_blobs(
        self,
        path: AsyncPurePathy,
        prefix: t.Optional[str] = None,
        delimiter: t.Optional[str] = None,
    ) -> t.AsyncGenerator[BlobGCS, None]:
        async with self.session() as client:
            bucket = self.lookup_bucket(path)
            if bucket is None:
                return
            response: t.Any = await client.list_objects(
                path.root, prefix=prefix, delimiter=delimiter
            )
            for page in response.pages:
                for item in page:
                    yield BlobGCS(
                        bucket=bucket,
                        owner=item.owner,
                        name=item.name,
                        raw=item,
                        size=item.size,
                        updated=item.updated.timestamp(),
                    )

    async def scandir(
        self,
        path: AsyncPathy,
        prefix: t.Optional[str] = None,
        delimiter: t.Optional[str] = None,
    ) -> t.AsyncGenerator[BucketEntryGCS, None]:
        sep = path._flavour.sep
        async with self.session() as client:
            bucket = await client.lookup_bucket(path)
            if bucket is None:
                return
            response = await client.client.list_blobs(
                bucket.name, prefix=prefix, delimiter=sep
            )
            for page in response.pages:
                folder: str
                for folder in list(page.prefixes):
                    full_name = folder[:-1] if folder.endswith(sep) else folder
                    name = full_name.split(sep)[-1]
                    if name:
                        yield BucketEntryGCS(name, is_dir=True, raw=None)
                item: t.Any
                for item in page:
                    name = item.name.split(sep)[-1]
                    if name:
                        yield BucketEntryGCS(
                            name=name,
                            is_dir=False,
                            size=item.size,
                            last_modified=item.updated.timestamp(),
                            raw=item,
                        )


@dataclass
class BucketGCS(AsyncBucket):
    name: str
    bucket: Bucket

    async def get_blob(self, blob_name: str) -> t.Optional[BlobGCS]:
        if not isinstance(blob_name, str):
            raise TypeError("expected str blob name, but found: {type(blob_name)}")
        native_blob: Blob = await self.bucket.get_blob(blob_name)
        if native_blob is None:
            return None
        return BlobGCS(
            bucket=self.bucket,
            owner=native_blob.owner,  # type:ignore
            name=native_blob.name,
            raw=native_blob,
            size=native_blob.size,
            updated=int(native_blob.updated.timestamp()),  # type:ignore
        )

    async def copy_blob(
        self, blob: BlobGCS, target: BlobGCS, name: str
    ) -> t.Optional[BlobGCS]:
        if blob.raw is None:
            raise FileNotFoundError("raw storage. Blob instance required")
        native_blob: Blob = self.bucket.copy(
            blob.raw, target.bucket, name
        )  # type:ignore
        return BlobGCS(
            bucket=self.bucket,
            owner=native_blob.owner,  # type:ignore
            name=native_blob.name,
            raw=native_blob,
            size=native_blob.size,
            updated=int(native_blob.updated.timestamp()),  # type:ignore
        )

    async def delete_blob(self, blob: AsyncBlob) -> None:
        return await self.bucket.delete_blob(blob.name)  # type: ignore

    async def delete_blobs(self, blobs: t.AsyncGenerator[AsyncBlob, None]) -> None:
        return await self.bucket.delete_blobs(blobs)  # type: ignore

    async def exists(self) -> bool:
        return await self.bucket.exists()  # type: ignore


register_client("gs", BucketClientGCS)
