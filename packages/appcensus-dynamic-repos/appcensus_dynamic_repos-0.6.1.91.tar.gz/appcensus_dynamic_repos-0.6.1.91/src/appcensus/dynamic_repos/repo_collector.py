from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import List

from poetry.config.source import Source
from poetry.repositories.pypi_repository import PyPiRepository
from poetry.repositories.repository import Repository
from poetry.repositories.repository_pool import Priority, RepositoryPool

# Unfortunately poetry doesn't have a public API to determine the default/secondary flags.
#
# It sucks to be dependent on implmentation details, but there's not much choice here. We'll hide it
# and keep be prepared to implement different strategies for different versions.


class RepoStrategy(ABC):
    def __init__(self, pool: RepositoryPool):
        self._pool = pool

    @abstractmethod
    def repositories(self) -> List[Source]:
        pass


# In 1.2, the pool keeps an index marker for the beginning of the secondaries in a list of repos.
class IndexedRepoStrategy(RepoStrategy):
    def __init__(self, pool: RepositoryPool):
        super().__init__(pool)

    def repositories(self) -> List[Source]:
        repos = []
        secondary_start = self._pool._secondary_start_idx  # type: ignore[attr-defined]
        for rx, repo in enumerate(self._pool.repositories):
            repos.append(
                Source(
                    name=repo.name,
                    url=repo.url,  # type: ignore[attr-defined]
                    default=True if rx == 0 else False,
                    secondary=True if secondary_start and rx >= secondary_start else False,
                )
            )
        return repos


# In 1.3+, they've re-factored this a bit, and there is a notion of 'Prioritized Repositories'.
# However, the priority is discarded and a priority-ordered list is returned for .repositories.
# We mine internals for the attached priority, and set the flags appropriately.
class PrioritizedRepoStrategy(RepoStrategy):
    def __init__(self, pool: RepositoryPool):
        super().__init__(pool)

    def _get_repo_priority(self, repo: Repository) -> Priority:
        return self._pool._repositories[repo.name]  # type: ignore[return-value]

    def repositories(self) -> List[Source]:
        repos = []
        for repo in self._pool.repositories:
            if type(repo) is PyPiRepository:
                continue
            prio = self._get_repo_priority(repo)
            repos.append(
                Source(
                    name=repo.name,
                    url=repo.url,  # type: ignore[attr-defined]
                    default=(prio == Priority.DEFAULT),
                    secondary=(prio == Priority.SECONDARY),
                )
            )
        return repos


# RepoCollector is a facade that detecs and uses a strategy for mining sources from the repo pool.
class RepoCollector:
    _strategy: RepoStrategy

    def __init__(self, pool: RepositoryPool):
        if hasattr(pool, "_secondary_start_idx"):
            self._strategy = IndexedRepoStrategy(pool)
        elif hasattr(pool, "_repositories") and type(pool._repositories) is OrderedDict:
            self._strategy = PrioritizedRepoStrategy(pool)
        else:
            raise NotImplementedError(
                "Cannot find a repo strategy for a pool that does not have a secondary start index"
                " nor an OrderedDict of repositories"
            )

    def repositories(
        self,
    ) -> List[Source]:
        return self._strategy.repositories()
