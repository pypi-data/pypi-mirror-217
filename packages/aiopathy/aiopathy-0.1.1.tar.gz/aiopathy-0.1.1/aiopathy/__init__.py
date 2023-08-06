import importlib
import os
import shutil
import typing as t
import uuid
from contextlib import asynccontextmanager
from contextlib import suppress
from dataclasses import dataclass
from dataclasses import field
from errno import EBADF
from errno import ELOOP
from errno import ENOENT
from errno import ENOTDIR
from functools import lru_cache
from io import DEFAULT_BUFFER_SIZE
from stat import S_ISBLK
from stat import S_ISCHR
from stat import S_ISFIFO
from stat import S_ISSOCK
from typing import cast

import smart_open
import smart_open.compression
from aiofiles.tempfile import TemporaryDirectory
from aiopath import AsyncPath
from aiopath import AsyncPurePath
from aiopath.flavours import _async_posix_flavour
from aiopath.flavours import _async_windows_flavour
from aiopath.flavours import _AsyncPosixFlavour

SUBCLASS_ERROR = "must be implemented in a subclass"

StreamableType = t.Any
AsyncFluidPath = t.Union["AsyncPathy", "AsyncBasePath"]
AsyncBucketType = t.TypeVar("AsyncBucketType")
AsyncBucketBlobType = t.TypeVar("AsyncBucketBlobType")

_drive_letters = [f"{(ord('a') + i)}:c" for i in range(26)]  # lower case with :


@dataclass
class ClientError(BaseException):
    message: str
    code: t.Optional[int]

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"({self.code}) {self.message}"


@dataclass
class AsyncBlobStat:
    """Stat for a bucket item"""

    name: str
    size: t.Optional[int]
    last_modified: t.Optional[int]


@dataclass
class AsyncBlob:
    bucket: t.Any
    name: str
    size: t.Optional[int]
    updated: t.Optional[int]
    owner: t.Optional[str]
    raw: t.Any

    async def delete(self) -> None:
        raise NotImplementedError(SUBCLASS_ERROR)

    async def exists(self) -> bool:
        raise NotImplementedError(SUBCLASS_ERROR)


class AsyncBucketEntry:
    """A single item returned from scanning a path"""

    name: str
    _is_dir: bool
    _stat: AsyncBlobStat
    raw: t.Optional[t.Any]

    def __init__(
        self,
        name: str,
        is_dir: bool = False,
        size: int = -1,
        last_modified: t.Optional[int] = None,
        raw: t.Optional[AsyncBlob] = None,
    ) -> None:
        self.name = name
        self.raw = raw
        self._is_dir = is_dir
        self._stat = AsyncBlobStat(name=name, size=size, last_modified=last_modified)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(name={self.name}, is_dir={self._is_dir}, "
            f"stat={self._stat})"
        )

    @staticmethod
    async def inode(*args: t.Any, **kwargs: dict[str, t.Any]) -> None:
        return None

    async def is_dir(self) -> bool:
        return self._is_dir

    async def is_file(self) -> bool:
        return not self._is_dir

    @staticmethod
    async def is_symlink() -> bool:
        return False

    async def stat(self, *, follow_symlinks: bool = True) -> AsyncBlobStat:
        return self._stat


@dataclass
class AsyncBucket:
    async def get_blob(self, blob_name: str) -> t.Optional[AsyncBlob]:
        raise NotImplementedError(SUBCLASS_ERROR)

    async def copy_blob(
        self, blob: AsyncBlob, target: "AsyncBucket", name: str
    ) -> t.Optional[AsyncBlob]:
        raise NotImplementedError(SUBCLASS_ERROR)

    async def delete_blob(self, blob: AsyncBlob) -> None:
        raise NotImplementedError(SUBCLASS_ERROR)

    async def delete_blobs(self, blobs: t.AsyncGenerator[AsyncBlob, None]) -> None:
        raise NotImplementedError(SUBCLASS_ERROR)

    async def exists(self) -> bool:
        raise NotImplementedError(SUBCLASS_ERROR)


class AsyncBucketClient:
    """Base class for a client that interacts with a bucket-based storage system."""

    # _client: t.Any

    async def get_blob(self, path: "AsyncPathy") -> t.Optional[AsyncBlob]:
        """Get the blob associated with a path or return None"""
        bucket = await self.lookup_bucket(path)
        if bucket is None:
            return None
        key_name = str(path.key)
        return await bucket.get_blob(key_name)

    def recreate(self, **kwargs: t.Any) -> None:
        """Recreate any underlying bucket client adapter with the given kwargs"""

    def open(
        self,
        path: "AsyncPathy",
        *,
        mode: str = "r",
        buffering: int = DEFAULT_BUFFER_SIZE,
        encoding: t.Optional[str] = None,
        errors: t.Optional[str] = None,
        newline: t.Optional[str] = None,
    ) -> StreamableType:
        client_params = {}
        if hasattr(self, "client_params"):
            client_params = getattr(self, "client_params")

        return smart_open.open(
            self.make_uri(path),
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            transport_params=client_params,
            # Disable de/compression based on the file extension
            compression=smart_open.compression.NO_COMPRESSION,
        )

    def make_uri(self, path: "AsyncPathy") -> t.Any:
        return path.as_uri()

    async def is_dir(self, path: "AsyncPathy") -> bool:
        return any(
            [blob async for blob in await self.list_blobs(path, prefix=path.prefix)]
        )

    async def rmdir(self, path: "AsyncPathy") -> None:
        return None

    async def exists(self, path: "AsyncPathy") -> bool:
        raise NotImplementedError(SUBCLASS_ERROR)

    async def lookup_bucket(self, path: "AsyncPathy") -> t.Optional[AsyncBucket]:
        return None

    def get_bucket(self, path: "AsyncPathy") -> AsyncBucket:
        raise NotImplementedError(SUBCLASS_ERROR)

    async def list_blobs(
        self,
        path: "AsyncPathy",
        prefix: t.Optional[str] = None,
        delimiter: t.Optional[str] = None,
    ) -> t.AsyncGenerator[AsyncBlob, None]:
        raise NotImplementedError(SUBCLASS_ERROR)

    @lru_cache
    def get_client(self):
        raise NotImplementedError(SUBCLASS_ERROR)

    @asynccontextmanager
    async def session(self) -> None:
        raise NotImplementedError(SUBCLASS_ERROR)

    async def scandir(
        self,
        path: "AsyncPathy",
        prefix: t.Optional[str] = None,
        delimiter: t.Optional[str] = None,
    ) -> t.AsyncGenerator[AsyncBucketEntry, None]:
        raise NotImplementedError(SUBCLASS_ERROR)

    async def create_bucket(self, path: "AsyncPathy") -> AsyncBucket:
        raise NotImplementedError(SUBCLASS_ERROR)

    async def delete_bucket(self, path: "AsyncPathy") -> None:
        raise NotImplementedError(SUBCLASS_ERROR)

    async def owner(self, path: "AsyncPathy") -> t.Optional[str]:
        blob: t.Optional[AsyncBlob] = await self.get_blob(path)
        return blob.owner if blob is not None else None

    async def resolve(self, path: "AsyncPathy", strict: bool = False) -> "AsyncPathy":
        path_parts = str(path).replace(path.drive, "")
        resolved = f"{path.drive}{os.path.abspath(path_parts)}"
        # On Windows the abspath normalization that happens replaces
        # / with \\ so we have to revert it here to preserve the
        # expected resolved path.
        if path.drive.lower() not in _drive_letters:
            resolved = resolved.replace("\\", "/")
        return AsyncPathy(resolved)

    async def mkdir(self, path: "AsyncPathy", mode: int = 0) -> None:
        bucket: t.Optional[AsyncBucket] = await self.lookup_bucket(path)
        if bucket is None or not (await bucket.exists()):
            await self.create_bucket(path)


class _AsyncPathyFlavour(_AsyncPosixFlavour):
    sep: str
    is_supported = True

    def parse_parts(self, parts: list[str]) -> tuple[str, str, list[str]]:
        parse_tuple: tuple[str, str, list[str]] = super().parse_parts(parts)
        drv, root, parsed = parse_tuple
        if parsed and parsed[0].endswith(":"):
            if len(parsed) < 2:
                raise ValueError("need atleast two parts")
            # Restore the
            drv = parsed[0]  # scheme:
            root = parsed[1]  # bucket_name
        for part in parsed[1:]:
            if part == "..":
                index = parsed.index(part)
                parsed.pop(index - 1)
                parsed.remove(part)
        return drv, root, parsed

    @staticmethod
    async def make_uri(path: "AsyncPathy") -> str:
        return str(path)


class AsyncPurePathy(AsyncPurePath):  # type:ignore
    """PurePath subclass for bucket storage."""

    _flavour = _AsyncPathyFlavour()
    __slots__ = ()

    @property
    def scheme(self) -> t.Any:
        """Return the scheme portion of this path. A path's scheme is the leading
        few characters. In a website you would see a scheme of "http" or "https".

        Consider a few examples:

        ```python
        assert AsyncPathy("gs://foo/bar").scheme == "gs"
        assert AsyncPathy("file:///tmp/foo/bar").scheme == "file"
        """
        # If there is no drive, return nothing
        if self.drive == "":
            return ""
        # This is an assumption of mine. I think it's fine, but let's
        # cause an error if it's not the case.
        if self.drive[-1] == ":":
            raise ValueError("drive should end with :")
        return self.drive[:-1]

    @property
    def bucket(self) -> "AsyncPathy":
        """Return a new instance of only the bucket path."""
        self._absolute_path_validation()
        return cast(AsyncPathy, type(self)(f"{self.drive}//{self.root}"))

    @property
    def key(self) -> t.Optional["AsyncPathy"]:
        """Return a new instance of only the key path."""
        self._absolute_path_validation()
        key = self._flavour.sep.join(self.parts[2:])
        if not key or len(self.parts) < 2:
            return None
        return cast(AsyncPathy, type(self)(key))

    @property
    def prefix(self) -> str:
        """Returns part of the path after the bucket-name, always ending with path.sep,
        or an empty string if there is no prefix."""
        if not self.key:
            return ""
        return f"{self.key}{self._flavour.sep}"

    def _absolute_path_validation(self) -> None:
        if not self.is_absolute():
            raise ValueError("relative paths are unsupported")

    @classmethod
    def _format_parsed_parts(cls, drv: str, root: str, parts: list[str]) -> str:
        # AsyncBucket path "gs://foo/bar"
        join_fn: t.Callable[[list[str]], str] = cls._flavour.join
        # If the scheme is file: and it's Windows, use \\ slashes to join
        if drv.lower() == "file:" and os.name == "nt":
            join_fn = "\\".join
        res: str
        if drv and root:
            res = f"{drv}//{root}/" + join_fn(parts[2:])
        # Absolute path
        elif drv or root:
            res = drv + root + join_fn(parts[1:])
        else:
            # Relative path
            res = join_fn(parts)
        return res


_SUPPORTED_OPEN_MODES = {"r", "rb", "tr", "rt", "w", "wb", "bw", "wt", "tw"}


class AsyncBasePath(AsyncPath):  # type:ignore
    # NOTE: pathlib normally takes care of this, but the logic checks
    #       for specifically "Path" type class in __new__ so we need to
    #       set the flavour manually based on the OS.
    _flavour = _async_windows_flavour if os.name == "nt" else _async_posix_flavour

    async def ls(self: t.Any) -> t.AsyncGenerator["AsyncBlobStat", None]:
        client: AsyncBucketClient = self.get_client(getattr(self, "scheme", "file"))
        blobs: t.AsyncGenerator[AsyncBucketEntry, None] = cast(
            t.AsyncGenerator, await client.scandir(self, prefix=getattr(self, "prefix"))
        )
        async for blob in blobs:
            stat = await blob.stat()
            yield AsyncBlobStat(
                name=str(blob.name), size=stat.size, last_modified=stat.last_modified
            )

    async def iterdir(self: t.Any) -> t.AsyncGenerator["AsyncBasePath", None]:
        """Iterate over the blobs found in the given bucket or blob prefix path."""
        client: AsyncBucketClient = self.get_client(getattr(self, "scheme", "file"))
        blobs: t.AsyncGenerator[AsyncBucketEntry, None] = cast(
            t.AsyncGenerator, await client.scandir(self, prefix=getattr(self, "prefix"))
        )
        async for blob in blobs:
            yield self / blob.name

    async def stat(self: "AsyncBasePath") -> AsyncBlobStat:
        """Iterate over the blobs found in the given bucket or blob prefix path."""
        stat = await super().stat()
        return AsyncBlobStat(
            name=self.name, size=stat.st_size, last_modified=int(stat.st_mtime)
        )

    # Stat helpers

    def _check_mode(self: "AsyncBasePath", mode_fn: t.Callable[[int], bool]) -> bool:
        """
        Check the mode against a stat.S_IS[MODE] function.

        This ignores OS-specific errors that are raised when a path does
        not exist, or has some invalid attribute (e.g. a bad symlink).
        """
        try:
            return mode_fn(os.stat(self).st_mode)
        except OSError as exception:
            # Ignorable error codes come from pathlib.py
            #
            error = getattr(exception, "errno", None)
            errors = (ENOENT, ENOTDIR, EBADF, ELOOP)
            win_error = getattr(exception, "winerror", None)
            win_errors = (
                21,  # ERROR_NOT_READY - drive exists but is not accessible
                123,  # ERROR_INVALID_NAME - fix for bpo-35306
                1921,  # ERROR_CANT_RESOLVE_FILENAME - broken symlink points to self
            )
            if error not in errors and win_error not in win_errors:
                raise
            return False
        except ValueError:
            return False

    async def is_dir(self: "AsyncBasePath") -> bool:
        """Whether this path is a directory."""
        return os.path.isdir(self)

    async def is_file(self: "AsyncBasePath") -> bool:
        """Whether this path is a file."""
        return os.path.isfile(self)

    async def is_mount(self: "AsyncBasePath") -> bool:
        """Check if this path is a POSIX mount point"""
        return os.path.ismount(self)

    async def is_symlink(self: "AsyncBasePath") -> bool:
        """Whether this path is a symbolic link."""
        return os.path.islink(self)

    async def is_block_device(self: "AsyncBasePath") -> bool:
        """Whether this path is a block device."""
        return self._check_mode(S_ISBLK)

    async def is_char_device(self: "AsyncBasePath") -> bool:
        """Whether this path is a character device."""
        return self._check_mode(S_ISCHR)

    async def is_fifo(self: "AsyncBasePath") -> bool:
        """Whether this path is a FIFO."""
        return self._check_mode(S_ISFIFO)

    async def is_socket(self: "AsyncBasePath") -> bool:
        """Whether this path is a socket."""
        return self._check_mode(S_ISSOCK)


class AsyncPathy(AsyncPurePathy, AsyncBasePath):
    """Subclass of `AsyncPath` that works with bucket APIs."""

    __slots__ = ()

    # _accessor: AsyncBucketsAccessor = AsyncBucketsAccessor()

    @staticmethod
    def _not_supported_message(method) -> str:
        return f"{method} is an unsupported bucket operation"

    _UNSUPPORTED_PATH = (
        "absolute file paths must be initialized using AsyncPathy.fluid(path)"
    )
    _client: t.Optional[AsyncBucketClient]

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        # Error when initializing paths without using AsyncPathy.fluid if the
        # path is an absolute system path (windows/unix)
        root = str(self)[0]  # "/tmp/path"
        drv = str(self)[:2].lower()  # C:\\tmp\\path
        if root == "/" or drv in _drive_letters:
            raise ValueError(AsyncPathy._UNSUPPORTED_PATH)

    @staticmethod
    def client(path: "AsyncPathy") -> AsyncBucketClient:
        return get_client(path.scheme)

    def __truediv__(self, key: t.Any) -> t.Any:
        return super().__truediv__(key)

    @classmethod
    def fluid(cls, path_candidate: str | AsyncFluidPath) -> AsyncFluidPath:
        """Infer either a AsyncPathy or AsyncPath from an input path or string.

        The returned type is a union of the potential `FluidPath` types and will
        type-check correctly against the minimum overlapping APIs of all the input
        types.

        If you need to use specific implementation details of a type, "narrow" the
        return of this function to the desired type, e.g.

        ```python
        from pathy import FluidPath, AsyncPathy

        fluid_path: FluidPath = AsyncPathy.fluid("gs://my_bucket/foo.txt")
        # Narrow the type to a specific class
        assert isinstance(fluid_path, AsyncPathy), "must be AsyncPathy"
        # Use a member specific to that class
        assert fluid_path.prefix == "foo.txt/"
        ```
        """
        with suppress(ValueError):
            result = AsyncPathy(path_candidate)
            if result.root != "":
                return result
        return AsyncBasePath(path_candidate)

    @classmethod
    def from_bucket(cls, bucket_name: str, scheme: str = "gs") -> "AsyncPathy":
        """Initialize a AsyncPathy from a bucket name.
        This helper adds a trailing slash and the appropriate prefix.

        ```python
        from pathy import AsyncPathy

        assert str(AsyncPathy.from_bucket("one")) == "gs://one/"
        assert str(AsyncPathy.from_bucket("two")) == "gs://two/"
        ```
        """
        return AsyncPathy(f"{scheme}://{bucket_name}/")

    @classmethod
    async def to_local(
        cls, blob_path: "AsyncPathy", recurse: bool = True
    ) -> "AsyncPath":
        """Download and cache either a blob or a set of blobs matching a prefix.

        The cache is sensitive to the file updated time, and downloads new blobs
        as their updated timestamps change."""
        cache_folder = get_fs_cache()
        if cache_folder is None:
            raise ValueError(
                'cannot get and cache a blob without first calling "use_fs_cache"'
            )

        await cache_folder.mkdir(exist_ok=True, parents=True)

        in_path: AsyncPathy
        if not isinstance(blob_path, AsyncPathy):
            in_path = AsyncPathy(blob_path)
        else:
            in_path = blob_path

        cache_blob: AsyncPath = (await cache_folder.absolute()) / in_path.root
        if in_path.key is not None:
            cache_blob /= in_path.key
        cache_time: AsyncPath = (
            (await cache_folder.absolute()) / in_path.root / f"{in_path.key}.time"
        )
        # Keep a cache of downloaded files. Fetch new ones when:
        #  - the file isn't in the cache
        #  - cached_stat.updated != latest_stat.updated
        if await cache_blob.exists() and await cache_time.exists():
            fs_time: str = await cache_time.read_text()
            gcs_stat: AsyncBlobStat = await in_path.stat()
            # If the times match, return the cached blob
            if fs_time == str(gcs_stat.last_modified):
                return cache_blob
            # remove the cache files because they're out of date
            await cache_blob.unlink()
            await cache_time.unlink()

        # If the file isn't in the cache, download it
        if not await cache_blob.exists():
            # Is a blob
            if await in_path.is_file():
                dest_folder = cache_blob.parent
                await dest_folder.mkdir(exist_ok=True, parents=True)
                await cache_blob.write_bytes(await in_path.read_bytes())
                blob_stat: AsyncBlobStat = await in_path.stat()
                await cache_time.write_text(str(blob_stat.last_modified))
            elif recurse:
                # If not a specific blob, enumerate all the blobs under
                # the path and cache them, then return the cache folder
                async for blob in in_path.rglob("*"):
                    await AsyncPathy.to_local(blob, recurse=False)
        return cache_blob

    async def ls(self: "AsyncPathy") -> t.AsyncGenerator[AsyncBlob, None]:
        """list blob names with stat information under the given path.

        This is considerably faster than using iterdir if you also need
        the stat information for the enumerated blobs.

        Yields AsyncBlobStat objects for each found blob.
        """
        yield super().ls()

    async def stat(
        self: "AsyncPathy", *, follow_symlinks: bool = True
    ) -> AsyncBlobStat:
        """Returns information about this bucket path."""
        self._absolute_path_validation()
        if not self.key:
            raise ValueError("cannot stat a bucket without a key")
        bucket = self.client(self).get_bucket(self)
        blob: t.Optional[AsyncBlob] = await bucket.get_blob(str(self.key))
        if blob is None:
            raise FileNotFoundError(self)
        return AsyncBlobStat(
            name=str(blob.name), size=blob.size, last_modified=blob.updated
        )

    async def exists(self: "AsyncPathy") -> bool:
        """Returns True if the path points to an existing bucket, blob, or prefix."""
        self._absolute_path_validation()
        client = self.client(self)
        bucket = await client.lookup_bucket(self)
        if bucket is None or not (await bucket.exists()):
            return False
        if not self.key:
            return True

        key_name = str(self.key)
        blob: t.Optional[AsyncBlob] = await bucket.get_blob(key_name)
        if blob is not None:
            return await blob.exists()
        # Determine if the path exists according to the current adapter
        return await client.exists(self)

    async def is_dir(self: "AsyncPathy") -> bool:
        """Determine if the path points to a bucket or a prefix of a given blob
        in the bucket.

        Returns True if the path points to a bucket or a blob prefix.
        Returns False if it points to a blob or the path doesn't exist.
        """
        self._absolute_path_validation()
        if self.bucket and not self.key:
            return True
        return await self.client(self).is_dir(self)

    async def is_file(self: "AsyncPathy") -> bool:
        """Determine if the path points to a blob in the bucket.

        Returns True if the path points to a blob.
        Returns False if it points to a bucket or blob prefix, or if the path doesn’t
        exist.
        """
        self._absolute_path_validation()
        if not self.bucket or not self.key:
            return False
        try:
            return bool(self.stat())
        except (ClientError, FileNotFoundError):
            return False

    async def iterdir(
        self: "AsyncPathy",
    ) -> t.AsyncGenerator["AsyncPathy", None]:
        """Iterate over the blobs found in the given bucket or blob prefix path."""
        yield cast(AsyncBlob, super().iterdir())

    async def glob(
        self: "AsyncPathy", pattern: str
    ) -> t.AsyncGenerator["AsyncPathy", None]:
        """Perform a glob match relative to this AsyncPathy instance,
        yielding all matched blobs."""
        yield cast(AsyncBlob, super().glob(pattern))

    async def rglob(
        self: "AsyncPathy", pattern: str
    ) -> t.AsyncGenerator["AsyncPathy", None]:
        """Perform a recursive glob match relative to this AsyncPathy instance, yielding
        all matched blobs. Imagine adding "**/" before a call to glob."""
        yield cast(AsyncBlob, super().rglob(pattern))

    def open(
        self: "AsyncPathy",
        mode: str = "r",
        buffering: int = DEFAULT_BUFFER_SIZE,
        encoding: t.Optional[str] = None,
        errors: t.Optional[str] = None,
        newline: t.Optional[str] = None,
    ) -> StreamableType:
        """Open the given blob for streaming. This delegates to the `smart_open`
        library that handles large file streaming for a number of bucket API
        providers."""
        self._absolute_path_validation()
        if mode not in _SUPPORTED_OPEN_MODES:
            raise ValueError(f"supported modes are {_SUPPORTED_OPEN_MODES} got {mode}")
        if buffering in (0, 1):
            raise ValueError(
                "supported buffering values are only block sizes, no 0 or 1"
            )
        if "b" in mode and encoding:
            raise ValueError("binary mode doesn't take an encoding argument")

        return self.client(self).open(
            self,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
        )

    async def owner(self: "AsyncPathy") -> t.Optional[str]:
        """Returns the name of the user that owns the bucket or blob
        this path points to. Returns None if the owner is unknown or
        not supported by the bucket API provider."""
        self._absolute_path_validation()
        if not self.is_file():
            raise FileNotFoundError(str(self))
        return await self.client(self).owner(self)

    async def resolve(self, strict: bool = False) -> "AsyncPathy":
        """Resolve the given path to remove any relative path specifiers.

        ```python
        from pathy import AsyncPathy

        path = AsyncPathy("gs://my_bucket/folder/../blob")
        assert path.resolve() == AsyncPathy("gs://my_bucket/blob")
        ```
        """
        self._absolute_path_validation()
        return await self.client(self).resolve(self, strict=strict)

    async def rename(
        self: "AsyncPathy", target: t.Union[str, AsyncPurePath]
    ) -> "AsyncPathy":
        """Rename this path to the given target.

        If the target exists and is a file, it will be replaced silently if the user
        has permission.

        If path is a blob prefix, it will replace all the blobs with the same prefix
        to match the target prefix."""
        self._absolute_path_validation()
        self_type = type(self)
        result = target if isinstance(target, self_type) else self_type(target)
        result._absolute_path_validation()

        client: AsyncBucketClient = self.client(self)
        bucket: AsyncBucket = client.get_bucket(self)
        target_bucket: AsyncBucket = client.get_bucket(result)

        # Single file
        if not await self.is_dir():
            from_blob: t.Optional[AsyncBlob] = await bucket.get_blob(str(self.key))
            if from_blob is None:
                raise FileNotFoundError(f'source file "{self}" does not exist')
            await target_bucket.copy_blob(from_blob, target_bucket, str(result.key))
            await bucket.delete_blob(from_blob)
            return self

        # Folder with objects
        sep: str = self._flavour.sep
        blobs = [
            blob
            async for blob in await client.list_blobs(
                self, prefix=self.prefix, delimiter=sep
            )
        ]

        # First rename
        for blob in blobs:
            target_key_name = blob.name.replace(str(self.key), str(result.key))
            await target_bucket.copy_blob(blob, target_bucket, target_key_name)
        # Then delete the sources
        for blob in blobs:
            await bucket.delete_blob(blob)
        return self

    async def replace(
        self: "AsyncPathy", target: t.Union[str, AsyncPurePath]
    ) -> "AsyncPathy":
        """Renames this path to the given target.

        If target points to an existing path, it will be replaced."""
        return await self.rename(target)

    async def rmdir(self: "AsyncPathy") -> None:
        """Removes this bucket or blob prefix. It must be empty."""
        self._absolute_path_validation()
        if self.is_file():
            raise NotADirectoryError()
        if not self.is_dir():
            raise FileNotFoundError()
        client: AsyncBucketClient = self.client(self)
        key_name = str(self.key) if self.key is not None else None
        bucket: AsyncBucket = client.get_bucket(self)
        blobs = await client.list_blobs(self, prefix=key_name)

        await bucket.delete_blobs(blobs)
        # The path is just the bucket
        if key_name is None:
            await client.delete_bucket(self)
        elif await client.is_dir(self):
            await client.rmdir(self)

    async def samefile(
        self: "AsyncPathy", other_path: t.Union[str, bytes, int, AsyncPath]
    ) -> bool:
        """Determine if this path points to the same location as other_path."""
        self._absolute_path_validation()
        if not isinstance(other_path, AsyncPath):
            other_path = type(self)(other_path)
        if not isinstance(other_path, AsyncPathy):
            raise AttributeError
        return (
            self.bucket == other_path.bucket
            and self.key == other_path.key
            and (await self.is_file())
        )

    async def touch(
        self: "AsyncPathy", mode: int = 0o666, exist_ok: bool = True
    ) -> None:
        """Create a blob at this path.

        If the blob already exists, the function succeeds if exist_ok is true
        (and its modification time is updated to the current time), otherwise
        FileExistsError is raised.
        """
        if await self.exists() and not exist_ok:
            raise FileExistsError()
        await self.write_text("")

    async def mkdir(
        self, mode: int = 0o777, parents: bool = False, exist_ok: bool = False
    ) -> None:
        """Create a bucket from the given path. Since bucket APIs only have implicit
        folder structures (determined by the existence of a blob with an overlapping
        prefix) this does nothing other than create buckets.

        If parents is False, the bucket will only be created if the path points to
        exactly the bucket and nothing else. If parents is true the bucket will be
        created even if the path points to a specific blob.

        The mode param is ignored.

        Raises FileExistsError if exist_ok is false and the bucket already exists.
        """
        try:
            # If the path is just the bucket, respect the result of "bucket.exists()"
            if self.key is None and not exist_ok and (await self.bucket.exists()):
                raise FileExistsError(f"Bucket {self.bucket} already exists")
            await self.client(self).mkdir(self, mode)
        except OSError:
            if not exist_ok:
                raise

    async def is_mount(self: "AsyncPathy") -> bool:
        return False

    async def is_symlink(self: "AsyncPathy") -> bool:
        return False

    async def is_socket(self: "AsyncPathy") -> bool:
        return False

    async def is_fifo(self: "AsyncPathy") -> bool:
        return False

    async def unlink(self: "AsyncPathy", **kwargs) -> None:
        """Delete a link to a blob in a bucket."""
        bucket = self.client(self).get_bucket(self)
        blob: t.Optional[AsyncBlob] = await bucket.get_blob(str(self.key))
        if blob is None:
            raise FileNotFoundError(self)
        await blob.delete()

    async def _scandir(self: "AsyncPathy") -> t.AsyncGenerator[AsyncBlob, None]:
        yield self.client(self).scandir(self, prefix=self.prefix)

    # Unsupported operations below here

    @classmethod
    async def cwd(cls) -> t.Any:
        message = cls._not_supported_message(cls.cwd.__qualname__)
        raise NotImplementedError(message)

    @classmethod
    async def home(cls) -> t.Any:
        message = cls._not_supported_message(cls.home.__qualname__)
        raise NotImplementedError(message)

    async def chmod(
        self: "AsyncPathy", mode: int, *, follow_symlinks: bool = True
    ) -> t.Any:
        message = self._not_supported_message(self.chmod.__qualname__)
        raise NotImplementedError(message)

    async def expanduser(self: "AsyncPathy") -> t.Any:
        message = self._not_supported_message(self.expanduser.__qualname__)
        raise NotImplementedError(message)

    async def lchmod(self: "AsyncPathy", mode: int) -> t.Any:
        message = self._not_supported_message(self.lchmod.__qualname__)
        raise NotImplementedError(message)

    async def group(self: "AsyncPathy") -> t.Any:
        message = self._not_supported_message(self.group.__qualname__)
        raise NotImplementedError(message)

    async def is_block_device(self: "AsyncPathy") -> t.Any:
        message = self._not_supported_message(self.is_block_device.__qualname__)
        raise NotImplementedError(message)

    async def is_char_device(self: "AsyncPathy") -> t.Any:
        message = self._not_supported_message(self.is_char_device.__qualname__)
        raise NotImplementedError(message)

    async def lstat(self: "AsyncPathy") -> t.Any:
        message = self._not_supported_message(self.lstat.__qualname__)
        raise NotImplementedError(message)

    async def symlink_to(
        self, target: str | AsyncPath, target_is_directory: bool = False
    ) -> t.Any:
        message = self._not_supported_message(self.symlink_to.__qualname__)
        raise NotImplementedError(message)


#
# File system adapter
#


class BucketEntryFS(AsyncBucketEntry):
    ...


@dataclass
class BlobFS(AsyncBlob):
    async def delete(self) -> None:
        """Delete a file-based blob."""
        file_folder: AsyncPath = self.raw.parent
        self.raw.unlink()
        # NOTE: in buckets folders only exist if a file is contained in them. Mimic
        # that behavior here by removing empty folders when the last file is removed.
        if len([path async for path in file_folder.iterdir() if (await path.is_dir())]):
            await file_folder.rmdir()

    async def exists(self) -> bool:
        return await self.raw.exists()


@dataclass
class BucketFS(AsyncBucket):
    name: str
    bucket: AsyncPath

    async def get_blob(self, blob_name: str) -> t.Optional[BlobFS]:
        native_blob = self.bucket / blob_name
        if not await native_blob.exists() or await native_blob.is_dir():
            return None
        stat = await native_blob.stat()
        # path.owner() raises KeyError if the owner's UID isn't known
        #
        # https://docs.python.org/3/library/pathlib.html#AsyncPath.owner
        owner: t.Optional[str]
        try:
            # path.owner() raises NotImplementedError on windows
            owner = await native_blob.owner()  # type:ignore
        except (KeyError, NotImplementedError):
            owner = None
        return BlobFS(
            bucket=self,
            owner=owner,
            name=blob_name,
            raw=native_blob,
            size=stat.st_size,
            updated=int(round(stat.st_mtime)),
        )

    async def copy_blob(  # type:ignore[override]
        self, blob: BlobFS, target: "BucketFS", name: str
    ) -> None:
        in_file = blob.bucket.bucket / blob.name
        out_file = target.bucket / name
        await out_file.write_bytes(in_file.read_bytes())

    async def delete_blob(self, blob: AsyncBlob) -> None:
        await blob.delete()

    async def delete_blobs(self, blobs: list[AsyncBlob]) -> None:
        for blob in blobs:
            await blob.delete()

    async def exists(self) -> bool:
        return await self.bucket.exists()


@dataclass
class BucketClientFS(AsyncBucketClient):
    # Root to store file-system buckets as children of
    root: AsyncPath = field(
        default_factory=lambda: AsyncPath(f"/tmp/pathy-{uuid.uuid4().hex}/")
    )

    async def full_path(self, path: AsyncPathy) -> AsyncPath:
        full_path = (await self.root.absolute()) / path.root
        if path.key is not None:
            full_path = full_path / path.key
        return full_path

    async def exists(self, path: AsyncPathy) -> bool:
        """Return True if the path exists as a file or folder on disk"""
        full_path = await self.full_path(path)
        return await full_path.exists()

    async def is_dir(self, path: AsyncPathy) -> bool:
        full_path = await self.full_path(path)
        return await full_path.is_dir()

    async def rmdir(self, path: AsyncPathy) -> None:
        full_path = await self.full_path(path)
        return shutil.rmtree(str(full_path))

    async def mkdir(self, path: "AsyncPathy", mode: int = 0) -> None:
        full_path = await self.full_path(path)
        await AsyncPath.mkdir(full_path, parents=True, exist_ok=True)

    async def open(
        self,
        path: AsyncPathy,
        *,
        mode: str = "r",
        buffering: int = DEFAULT_BUFFER_SIZE,
        encoding: t.Optional[str] = None,
        errors: t.Optional[str] = None,
        newline: t.Optional[str] = None,
    ) -> StreamableType:
        if self.lookup_bucket(path) is None:
            raise ClientError(message=f'bucket "{path.root}" does not exist', code=404)

        full_path = await self.full_path(path)
        if not await full_path.exists():
            if full_path.name != "":
                full_path = full_path.parent
            await full_path.mkdir(parents=True, exist_ok=True)
        return super().open(
            path,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
        )

    async def make_uri(self, path: AsyncPurePathy) -> str:
        if not path.root:
            raise ValueError(f"cannot make a URI to an invalid bucket: {path.root}")
        full_path = (await self.root.absolute()) / path.root
        if path.key is not None:
            full_path /= path.key
        result = f"file://{full_path}"
        return result

    async def create_bucket(self, path: AsyncPurePathy) -> AsyncBucket:
        if not path.root:
            raise ValueError(f"Invalid bucket name: {path.root}")
        bucket_path: AsyncPath = self.root / path.root
        if await bucket_path.exists():
            raise FileExistsError(f"Bucket already exists at: {bucket_path}")
        await bucket_path.mkdir(parents=True, exist_ok=True)
        return BucketFS(str(path.root), bucket=bucket_path)

    async def delete_bucket(self, path: AsyncPurePathy) -> None:
        bucket_path: AsyncPath = self.root / str(path.root)
        if await bucket_path.exists():
            shutil.rmtree(bucket_path)

    async def lookup_bucket(self, path: AsyncPurePathy) -> BucketFS:
        if path.root:
            bucket_path: AsyncPath = self.root / path.root
            if await bucket_path.exists():
                return BucketFS(str(path.root), bucket=bucket_path)

    async def get_bucket(self, path: AsyncPurePathy) -> BucketFS:
        if not path.root:
            raise ValueError(f"path has an invalid bucket_name: {path.root}")
        bucket_path: AsyncPath = self.root / path.root
        if await bucket_path.is_dir():
            return BucketFS(str(path.root), bucket=bucket_path)
        raise FileNotFoundError(f"Bucket {path.root} does not exist!")

    async def list_blobs(
        self,
        path: AsyncPurePathy,
        prefix: t.Optional[str] = None,
        delimiter: t.Optional[str] = None,
    ) -> t.AsyncGenerator[BlobFS, None]:
        if path.root is None:
            raise AttributeError
        bucket = self.get_bucket(path)
        scan_path = self.root / path.root
        if prefix is not None:
            scan_path = scan_path / prefix

        # AsyncPath to a file
        if await scan_path.exists() and not await scan_path.is_dir():
            stat = await scan_path.stat()
            file_size = stat.st_size
            updated = int(round(stat.st_mtime_ns * 1000))
            yield BlobFS(
                bucket,
                name=str(scan_path),
                size=file_size,
                updated=updated,
                owner=None,
                raw=scan_path,
            )

        # Yield blobs for each file
        async for file_path in scan_path.rglob("*"):
            if file_path.is_dir():
                continue
            stat = await file_path.stat()
            file_size = stat.st_size
            updated = int(round(stat.st_mtime_ns * 1000))
            name = file_path.name
            if prefix:
                name = prefix + name
            yield BlobFS(
                bucket,
                name=f"{prefix if prefix is not None else ''}{file_path.name}",
                size=file_size,
                updated=updated,
                owner=None,
                raw=file_path,
            )

    async def scandir(
        self,
        path: AsyncPathy,
        prefix: t.Optional[str] = None,
        delimiter: t.Optional[str] = None,
    ) -> t.AsyncGenerator["BucketEntryFS", None]:
        scan_path = self.root / path.root
        async with self.session() as client:
            if isinstance(path, AsyncBasePath) and not isinstance(path, AsyncPathy):
                scan_path = client.root / path.root if not path.is_absolute() else path
            if prefix is not None:
                scan_path = scan_path / prefix
            async for dir_entry in scan_path.glob("*"):
                if await dir_entry.is_dir():
                    yield BucketEntryFS(dir_entry.name, is_dir=True, raw=None)
                else:
                    file_path = AsyncPath(dir_entry)
                    stat = await file_path.stat()
                    file_size = stat.st_size
                    updated = int(round(stat.st_mtime))
                    blob: BlobFS = BlobFS(
                        client.get_bucket(path),
                        name=dir_entry.name,
                        size=file_size,
                        updated=updated,
                        owner=None,
                        raw=file_path,
                    )
                    yield BucketEntryFS(
                        name=dir_entry.name,
                        is_dir=False,
                        size=file_size,
                        last_modified=updated,
                        raw=blob,
                    )


#
# Client Registration
#

# The only built-in client is the file-system one
_client_registry: dict[str, t.Type[AsyncBucketClient]] = {
    "": BucketClientFS,
    "file": BucketClientFS,
}
# t.Optional clients that we attempt to dynamically load when encountering
# a AsyncPathy object with a matching scheme
_optional_clients: dict[str, str] = {
    "gcs": "pathy.gcs",
    "s3": "pathy.s3",
    "azure": "pathy.azure",
}
AsyncBucketClientType = t.TypeVar("AsyncBucketClientType", bound=AsyncBucketClient)

# Hold given client args for a scheme
_client_args_registry: dict[str, t.Any] = {}
_instance_cache: dict[str, t.Any] = {}
_fs_client: t.Optional["BucketClientFS"] = None
_fs_cache: t.Optional[AsyncPath] = None


def register_client(scheme: str, type: t.Type[AsyncBucketClient]) -> None:
    """Register a bucket client for use with certain scheme AsyncPathy objects"""
    global _client_registry
    _client_registry[scheme] = type


def get_client(scheme: str) -> t.Any:
    """Retrieve the bucket client for use with a given scheme"""
    global _client_registry, _instance_cache, _fs_client  # noqa: FURB154
    global _optional_clients, _client_args_registry  # noqa: FURB154
    if _fs_client is not None:
        return _fs_client
    if scheme in _instance_cache:
        return _instance_cache[scheme]

    # Attempt to dynamically load optional clients if we find a matching scheme
    if scheme not in _client_registry and scheme in _optional_clients:
        importlib.import_module(_optional_clients[scheme])

    # Create the client from the known registry
    if scheme in _client_registry:
        kwargs: dict[str, t.Any] = (
            _client_args_registry[scheme] if scheme in _client_args_registry else {}
        )
        _instance_cache[scheme] = _client_registry[scheme](**kwargs)  # type:ignore
        return _instance_cache[scheme]

    raise ValueError(f'There is no client registered to handle "{scheme}" paths')


def set_client_params(scheme: str, **kwargs: t.Any) -> None:
    """Specify args to pass when instantiating a service-specific Client
    object. This allows for passing credentials in whatever way your underlying
    client library prefers."""
    global _client_registry, _instance_cache, _client_args_registry
    _client_args_registry[scheme] = kwargs
    if scheme in _instance_cache:
        _instance_cache[scheme].recreate(**_client_args_registry[scheme])
    return None


async def use_fs(
    root: t.Optional[t.Union[str, AsyncPath, bool]] = None
) -> t.Optional[BucketClientFS]:
    """Use a path in the local file-system to store blobs and buckets.

    This is useful for development and testing situations, and for embedded
    applications."""
    global _fs_client
    # False - disable adapter
    if root is False:
        _fs_client = None
        return None

    # None or True - enable FS adapter with default root
    if root is None or root is True:
        # Look up "data" folder of pathy package similar to spaCy
        client_root = AsyncPath(__file__).parent / "data"
    else:
        if not isinstance(root, (str, AsyncPath)):
            raise AttributeError("root is not a known type: {type(root)}")
        client_root = AsyncPath(root)
    if not await client_root.exists():
        await client_root.mkdir(parents=True)
    _fs_client = BucketClientFS(root=client_root)
    return _fs_client


def get_fs_client() -> t.Optional[BucketClientFS]:
    """Get the file-system client (or None)"""
    global _fs_client
    if _fs_client is not None or not isinstance(_fs_client, BucketClientFS):
        raise TypeError("invalid root type")
    return _fs_client


async def use_fs_cache(
    root: t.Optional[str | AsyncPath | bool] = None,
) -> t.Optional[AsyncPath]:
    """Use a path in the local file-system to cache blobs and buckets.

    This is useful for when you want to avoid fetching large blobs multiple
    times, or need to pass a local file path to a third-party library."""
    global _fs_cache
    # False - disable adapter
    if root is False:
        _fs_cache = None
        return None

    # None or True - enable FS cache with default root
    if root is None or root is True:
        # Use a temporary folder. Cache will be removed according to OS policy
        async with TemporaryDirectory() as tmp_dir:
            cache_root = AsyncPath(tmp_dir)
    else:
        if not isinstance(root, (str, AsyncPath)):
            raise TypeError("root is not a known type: {type(root)}")
        cache_root = AsyncPath(root)
    if not await cache_root.exists():
        await cache_root.mkdir(parents=True)
    _fs_cache = cache_root
    return cache_root


def get_fs_cache() -> t.Optional[AsyncPath]:
    """Get the folder that holds file-system cached blobs and timestamps."""
    global _fs_cache
    if _fs_cache is None or isinstance(_fs_cache, AsyncPath):
        raise TypeError("invalid root type")
    return _fs_cache


async def clear_fs_cache(force: bool = False) -> None:
    """Remove the existing file-system blob cache folder."""
    cache_path = get_fs_cache()
    if cache_path is None:
        raise FileNotFoundError("no cache to clear")
    resolved = await cache_path.resolve()
    if str(resolved) == "/":
        raise ValueError(f"refusing to remove a root path: {resolved}")
    shutil.rmtree(str(resolved))
