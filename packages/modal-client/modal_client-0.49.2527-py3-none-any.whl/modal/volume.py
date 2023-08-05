# Copyright Modal Labs 2023
from typing import Optional

from modal_proto import api_pb2
from modal_utils.async_utils import synchronize_api
from modal_utils.grpc_utils import retry_transient_errors

from ._resolver import Resolver
from .object import _Handle, _Provider


class _VolumeHandle(_Handle, type_prefix="vo"):
    """mdmd:hidden Handle to a `Volume` object."""

    async def commit(self):
        """Commit changes to the volume and fetch any other changes made to the volume by other tasks.

        Committing always triggers a reload after saving changes.

        If successful, the changes made are now persisted in durable storage and available for other functions/tasks.

        Committing will fail if there are open files for the volume.
        """
        req = api_pb2.VolumeCommitRequest(volume_id=self.object_id)
        _ = await retry_transient_errors(self._client.stub.VolumeCommit, req)
        # Reload changes on successful commit.
        await self.reload()

    async def reload(self):
        """Make changes made by other tasks/functions visible in the volume.

        Uncommitted changes to the volume, such as new or modified files, will be preserved during reload. Uncommitted
        changes will shadow any changes made by other tasks - e.g. if you have an uncommitted modified a file that was
        also updated by another task/function you will not see the changes made by the other function/task.

        Reloading will fail if there are open files for the volume.
        """
        req = api_pb2.VolumeReloadRequest(volume_id=self.object_id)
        _ = await retry_transient_errors(self._client.stub.VolumeReload, req)


VolumeHandle = synchronize_api(_VolumeHandle)


class _Volume(_Provider[_VolumeHandle]):
    """mdmd:hidden A writeable volume that can be used to share files between one or more Modal functions.

    The contents of a volume is exposed as a filesystem. You can use it to share data between different functions, or
    to persist durable state across several instances of the same function.

    Unlike a networked filesystem, you need to explicitly reload the volume to see changes made since it was mounted.
    Similarly, you need to explicitly commit any changes you make to the volume for the changes to become visible
    outside the current task.

    Concurrent modification is supported, but concurrent modifications of the same files should be avoided! Last write
    wins in case of concurrent modification of the same file - any data the last writer didn't have when committing
    changes will be lost!

    As a result, volumes are typically not a good fit for use cases where you need to make concurrent modifications to
    the same file (nor is distributed file locking supported).

    Volumes can only be committed and reloaded if there are no open files for the volume - attempting to reload or
    commit with open files will result in an error.

    **Usage**

    ```python
    import modal

    stub = modal.Stub()
    stub.volume = modal.Volume()

    @stub.function(volumes={"/root/foo": stub.volume})
    def f():
        with open("/root/foo/bar.txt", "w") as f:
            f.write("hello")
        stub.app.volume.commit()  # Persist changes

    @stub.function(volumes={"/root/foo": stub.volume})
    def g():
        stub.app.volume.reload()  # Fetch latest changes
        with open("/root/foo/bar.txt", "r") as f:
            print(f.read())
    ```
    """

    def __init__(self) -> None:
        """Construct a new volume, which is empty by default."""

        async def _load(resolver: Resolver, existing_object_id: Optional[str]) -> _VolumeHandle:
            status_row = resolver.add_status_row()
            if existing_object_id:
                # Volume already exists; do nothing.
                return _VolumeHandle._from_id(existing_object_id, resolver.client, None)

            status_row.message("Creating volume...")
            req = api_pb2.VolumeCreateRequest(app_id=resolver.app_id)
            resp = await retry_transient_errors(resolver.client.stub.VolumeCreate, req)
            status_row.finish("Created volume.")
            return _VolumeHandle._from_id(resp.volume_id, resolver.client, None)

        rep = "Volume()"
        super().__init__(_load, rep)


Volume = synchronize_api(_Volume)
