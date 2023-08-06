from abc import abstractmethod
from datetime import datetime, timedelta
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union

import tomli
import tomlkit
from cryptography.hazmat.primitives.hashes import SHA256, Hash
from pydantic import BaseModel, Field
from pytz import UTC
from tomlkit.items import KeyType, SingleKey, Table

from appcensus.dynamic_repos import REPO_FILE_PATH


class Auth(BaseModel):
    authtype: str
    cache: bool = False
    timeout: Optional[int] = None

    def to_table(self) -> Table:
        table = tomlkit.table(is_super_table=True)
        table.add("authtype", self.authtype)
        table.add("cache", self.cache)
        if self.timeout:
            table.add("timeout", self.timeout)
        return table


class BasicAuth(Auth):
    authtype: Literal["basic"] = "basic"
    cache: bool = True


class CodeArtifactAuth(Auth):
    authtype: Literal["codeartifact"] = "codeartifact"
    domain: str
    owner: str
    region: Optional[str] = None
    profile: Optional[str] = None

    def to_table(self) -> Table:
        table = super().to_table()
        table.add("domain", self.domain)
        table.add("owner", self.owner)
        if self.region:
            table.add("region", self.region)
        if self.profile:
            table.add("profile", self.profile)
        return table


class RepoCredentials(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        ignored_types = (cached_property,)

    authtype: str

    @cached_property
    @abstractmethod
    def fingerprint(self) -> str:
        raise NotImplementedError()


class BasicRepoCredentials(RepoCredentials):
    username: str
    password: str

    def valid(self) -> bool:
        return True

    @cached_property
    def fingerprint(self) -> str:
        if not self.username or not self.password:
            raise ValueError("Cannot fingerprint empty credentials")
        digest = Hash(SHA256())
        digest.update(bytes(f"{self.username}:{self.password}".encode()))
        return digest.finalize().hex()


class CachedCredentialSet(BaseModel):
    VALID_WINDOW: int = 30

    authtype: str
    expires: Optional[datetime] = None
    fingerprint: str

    def valid(self) -> bool:
        """Ensures that a set of credentials is valid for at least VALID_WINDOW seconds"""
        if not self.expires:
            return True
        return (datetime.now() + timedelta(seconds=self.VALID_WINDOW)).astimezone(
            UTC
        ) < self.expires.astimezone(UTC)

    def to_table(self) -> tomlkit.items.Item:
        table = tomlkit.table(is_super_table=True)
        table.append("authtype", self.authtype)
        table.append("fingerprint", self.fingerprint)
        if self.expires:
            table.append("expires", self.expires)
        return table


class Repo(BaseModel):
    name: str
    url: str
    auth: Union[None, CodeArtifactAuth, BasicAuth] = Field(None, discriminator="authtype")
    enabled: bool
    default: bool
    secondary: bool

    def to_table(self) -> Table:
        table = tomlkit.table(is_super_table=True)
        table.append("enabled", self.enabled)
        table.append("url", self.url)
        if self.auth:
            auth_table = self.auth.to_table()
            for key in dict.keys(auth_table):
                table.append(SingleKey(f"auth.{key}", KeyType.Bare), auth_table.get(key))
            # table.append("auth", auth_table)
        table.append("default", self.default)
        table.append("secondary", self.secondary)
        return table


class RepoManager:
    _repos: Dict[str, Repo] = {}

    @classmethod
    def entries(cls) -> List[str]:
        return list(cls._repos.keys())

    @classmethod
    def get(cls, name: str) -> Optional[Repo]:
        if name in cls._repos.keys():
            return cls._repos[name]
        return None

    @classmethod
    def load(self, file_path: Path = REPO_FILE_PATH) -> None:
        self._repos = {}
        if file_path.exists():
            with file_path.open("r") as fh:
                doc = tomli.loads(fh.read())
                if "repo" not in doc.keys():
                    raise ValueError(f"No repos declared in {file_path}")
                for repo_id, repo_attrs in doc["repo"].items():
                    repo_attrs["name"] = repo_id
                    repo = Repo(**repo_attrs)
                    self._repos[repo.name] = repo

    @classmethod
    def save(cls, file_path: Path = REPO_FILE_PATH) -> None:
        doc = tomlkit.document()

        repos = tomlkit.table(is_super_table=True)
        for key in cls._repos.keys():
            entry = cls._repos[key]
            repos.add(key, entry.to_table())
        doc.add("repo", repos)

        with file_path.open("w+") as fh:
            tomlkit.dump(doc, fh, sort_keys=False)


RepoManager.load()
