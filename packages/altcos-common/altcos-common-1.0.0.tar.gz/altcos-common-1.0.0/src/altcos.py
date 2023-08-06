from __future__ import annotations

import dataclasses
import datetime
import enum
import pathlib

import gi

gi.require_version("OSTree", "1.0")

from gi.repository import Gio, OSTree


class OSName(enum.StrEnum):
    ALTCOS = "altcos"


class Arch(enum.StrEnum):
    X86_64 = "x86_64"


class Branch(enum.StrEnum):
    SISYPHUS = "sisyphus"
    P10 = "p10"


@dataclasses.dataclass
class Stream:
    streams_root: str
    osname: OSName
    arch: Arch
    branch: Branch
    name: str | None = None

    def base_stream(self) -> Stream:
        """
        :return: экземпляр "Stream" без поля name
        """
        return Stream(self.streams_root,
                      self.osname,
                      self.arch,
                      self.branch)

    def like_ostree_ref(self) -> str:
        """
        :return: строка вида: "altcos/x86_64/p10", "altcos/x86_64/P10/k8s"
        """
        return str(pathlib.Path(self.osname,
                                self.arch,
                                self.branch.value.title() if self.name else self.branch.value,
                                self.name or ""))

    @classmethod
    def from_ostree_ref(cls, streams_root: str, ref: str) -> Stream:
        """
        :param streams_root: путь до хранилища потоков
        :param ref: ветка вида: "altcos/x86_64/Sisyphus/k8s"
        :return: экземпляр "Stream"
        """
        if len(parts := ref.lower().split("/")) not in [3, 4]:
            raise ValueError(f"Invalid reference format :: \"{ref}\".")

        return Stream(streams_root,
                      OSName(parts[0]),
                      Arch(parts[1]),
                      Branch(parts[2]),
                      parts[3] if len(parts) == 4 else None)

    @property
    def stream_dir(self) -> pathlib.Path:
        """
        :return: корень потока
        """
        return pathlib.Path(self.streams_root,
                            self.branch,
                            self.arch,
                            self.name or "")

    @property
    def rootfs_dir(self) -> pathlib.Path:
        """
        :return: путь до хранилища rootfs-образов, полученых при помощи mkimage-profiles
        """
        return self.base_stream().stream_dir.joinpath("rootfs")

    @property
    def ostree_bare_dir(self) -> pathlib.Path:
        """
        :return: путь до OSTree-репозитория в режиме bare
        """
        return self.base_stream().stream_dir.joinpath("ostree", "bare")

    @property
    def ostree_archive_dir(self) -> pathlib.Path:
        """
        :return: путь до OSTree-репозитория в режиме archive
        """
        return self.base_stream().stream_dir.joinpath("ostree", "archive")

    @property
    def vars_dir(self) -> pathlib.Path:
        """
        :return: путь к директории версий пользовательского слоя (относящиеся к OSTree-коммитам)
        """
        return self.stream_dir.joinpath("vars")

    @property
    def work_dir(self) -> pathlib.Path:
        """
        содержит необходимые директории для работы в overlay-режиме
        :return: путь до рабочей директории
        """
        return self.stream_dir.joinpath("work")

    @property
    def merged_dir(self) -> pathlib.Path:
        """
        :return: путь до директории, примонтированной в overlay-режиме
        """
        return self.work_dir.joinpath("merged")


class Repository:
    class Mode(enum.StrEnum):
        BARE = "bare"
        ARCHIVE = "archive"

    def __init__(self, stream: Stream, mode: Repository.Mode = Mode.BARE) -> None:
        self.stream = stream
        match mode:
            case Repository.Mode.BARE:
                path = stream.ostree_bare_dir
            case Repository.Mode.ARCHIVE:
                path = stream.ostree_archive_dir
            case _:
                raise ValueError(f"Invalid mode: \"{mode}\". "
                                 f"Allowed only: {' '.join(*Repository.Mode)}.")
        self.storage: OSTree.Repo = OSTree.Repo.new(Gio.file_new_for_path(str(path)))

    def open(self) -> Repository:
        self.storage.open(None)
        return self

    def last_commit(self) -> Commit:
        hashsum = self.storage.resolve_rev(self.stream.like_ostree_ref(), False)[1]
        return Commit(self, hashsum)

    def commit_by_version(self, version: Version, commit: Commit = None) -> Commit | None:
        if commit is None:
            commit = self.last_commit()

        if commit.version().full_version == version.full_version:
            return commit

        if (parent := commit.parent()) is None:
            return None

        return self.commit_by_version(version, parent)

    def list_streams(self) -> list[Stream]:
        return [Stream.from_ostree_ref(self.stream.streams_root, ref)
                for ref in self.storage.list_refs()[1]]


class Version:
    def __init__(self,
                 major: int,
                 minor: int,
                 branch: Branch,
                 name: str | None = None,
                 date: str | None = None):
        self.major = major
        self.minor = minor
        self.branch = branch
        self.name = name
        self.date = date or datetime.datetime.now().strftime("%Y%m%d")

    def __str__(self) -> str:
        """
        :return: строка версии вида: "20220101.1.0"
        """
        return f"{self.date}.{self.major}.{self.minor}"

    @property
    def full_version(self) -> str:
        """
        :return: строка версии вида: "p10_k8s.20220101.1.0"
        """
        return f"{self.branch}_{self.name or 'base'}.{self}"

    @property
    def like_path(self) -> pathlib.Path:
        return pathlib.Path(self.date, str(self.major), str(self.minor))

    @classmethod
    def from_str(cls, version: str) -> Version:
        """
        :param version: e.g. "p10_base.20230101.0.0"
        :return: экземпляр "Version"
        """
        if len(parts := version.split(".")) != 4:
            raise ValueError(f"Invalid version format \"{version}\".")

        if len(prefix := parts[0].split("_")) != 2:
            raise ValueError(f"Invalid version prefix format \"{version}\".")

        [branch, name] = Branch(prefix[0]), prefix[1]
        [date, major, minor] = parts[1], *map(int, parts[2:])

        if name == "base":
            name = None

        return Version(major, minor, branch, name, date)


class Commit:
    def __init__(self, repo: Repository, hashsum: str) -> None:
        self.repo = repo
        self.hashsum = hashsum

    def __str__(self) -> str:
        return self.hashsum

    def open(self) -> Commit:
        self.repo.storage.load_commit(self.hashsum)
        return self

    def version(self) -> Version:
        content = self.repo.storage.load_commit(self.hashsum)
        return Version.from_str(content[1][0]["version"])

    def description(self) -> str:
        return self.repo.storage.load_commit(self.hashsum)[1][4]

    def parent(self) -> Commit | None:
        content = self.repo.storage.load_commit(self.hashsum)
        parent_hashsum = OSTree.commit_get_parent(content[1])

        return Commit(self.repo, parent_hashsum) \
            if parent_hashsum \
            else None


class Platform(enum.StrEnum):
    QEMU = "qemu"
    METAL = "metal"


class Format(enum.StrEnum):
    QCOW2 = "qcow2"
    ISO = "iso"
    RAW = "raw"


@dataclasses.dataclass
class Artifact:
    location: str | None = None
    signature: str | None = None
    uncompressed: str | None = None
    uncompressed_signature: str | None = None


@dataclasses.dataclass
class Build:
    platform: Platform
    fmt: Format
    disk: Artifact | None = None
    kernel: Artifact | None = None
    initrd: Artifact | None = None
    rootfs: Artifact | None = None


ALLOWED_BUILDS = {
    Platform.QEMU: {
        Format.QCOW2,
    },
    Platform.METAL: {
        Format.ISO,
        Format.RAW,
    }
}


