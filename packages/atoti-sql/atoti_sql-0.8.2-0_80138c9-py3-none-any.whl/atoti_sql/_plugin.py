from pathlib import Path
from typing import Optional

import atoti as tt
from atoti_core import BaseSessionBound, Plugin

from ._source import infer_sql_types, load_sql


class SQLPlugin(Plugin):
    def init_session(self, session: BaseSessionBound, /) -> None:
        if not isinstance(session, tt.Session):
            return

        session._java_api.jvm.io.atoti.loading.sql.SqlPlugin.init()
        session._infer_sql_types = infer_sql_types
        session._load_sql = load_sql

    @property
    def jar_path(self) -> Optional[Path]:
        return Path(__file__).parent / "data" / "atoti-sql.jar"
