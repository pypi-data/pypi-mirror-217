from typing import List, Type

from cleo.io.io import IO
from cleo.io.null_io import NullIO
from poetry.config.source import Source
from poetry.console.application import Application
from poetry.console.commands.command import Command
from poetry.factory import Factory
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
from poetry.repositories.repository_pool import RepositoryPool
from poetry.utils.password_manager import PasswordManager
from poetry.utils.source import source_to_table
from tomlkit.items import AoT

from appcensus.dynamic_repos import REPO_FILE_PATH
from appcensus.dynamic_repos.auth import CredentialCache, CredentialManager
from appcensus.dynamic_repos.commands import (
    RepoClearCredentials,
    RepoDisableCommand,
    RepoEnableCommand,
    RepoSetAuth,
    RepoShowCommand,
    RepoShowCredentials,
    RepoUseCommand,
)
from appcensus.dynamic_repos.models import Repo, RepoManager
from appcensus.dynamic_repos.repo_collector import RepoCollector


class DynamicRepos(Plugin):
    def _configure_source(self, poetry: Poetry, io: IO, repo: Repo) -> None:
        existing_sources = RepoCollector(poetry.pool).repositories()

        new_source = Source(
            name=repo.name, url=repo.url, default=repo.default, secondary=repo.secondary
        )

        new_sources = AoT([])

        if new_source.default and new_source.secondary:
            raise ValueError(f"Repo {repo.name} cannot be default and secondary - pick one")

        for source in existing_sources:
            if source.name == "PyPI":
                continue  # poetry will always add PyPi

            if source == new_source:
                raise ValueError(
                    f"Identical source <c1>{source.anem}</> already exists. Perhaps you have a declaration in"
                    " pyproject.toml. You should resolve the redundancy to prevent conflict."
                )

            if new_source and source.name == repo.name:
                raise ValueError(
                    f"Inconsistent source with name <c1>{repo.name}</c1> already exists."
                    " Please reconile this."
                )

            if source.default and repo.default:
                raise ValueError(
                    f"Source with name <c1>{source.name}</c1> is already set to default."
                    f" Only one default source can be configured at a time. <c1>{repo.name}</c1>"
                    " will be rejected."
                )

            new_sources.append(source_to_table(source))

        new_sources.append(source_to_table(new_source))

        # configure new source and verify it was added
        poetry._pool = RepositoryPool()
        try:
            Factory.configure_sources(poetry, new_sources, poetry.config, NullIO())
            poetry.pool.repository(repo.name)
        except ValueError as e:
            raise ValueError(f"Failed to validate <c1>{repo.name}</c1>: {e}")

    def _exceptional_error(self, io: IO, e: Exception) -> None:
        io.write_error_line(f"DynamicRepos: <error>{e}</error>")

    def activate(self, poetry: Poetry, io: IO) -> None:
        if not REPO_FILE_PATH.exists():
            return
        for name in RepoManager.entries():
            repo = RepoManager.get(name)
            if repo.enabled:
                try:
                    self._configure_source(poetry, io, repo)
                    if repo.auth:
                        try:
                            pm = PasswordManager(poetry.config)
                            CredentialManager.authorize(pm, repo)
                        finally:
                            CredentialCache.save()
                except Exception as e:
                    self._exceptional_error(io, e)
                    return


class DynamicReposApplication(ApplicationPlugin):
    @property
    def commands(self) -> List[Type[Command]]:
        return [
            RepoShowCommand,
            RepoEnableCommand,
            RepoDisableCommand,
            RepoSetAuth,
            RepoShowCredentials,
            RepoClearCredentials,
            RepoUseCommand,
        ]

    def activate(self, application: Application) -> None:
        for command in self.commands:
            assert command.name
            application.command_loader.register_factory(command.name, command)
