from pathlib import Path
from typing import Optional

import atoti as tt
from atoti_core import BaseSessionBound, Plugin


class GCPPlugin(Plugin):
    def init_session(self, session: BaseSessionBound, /) -> None:
        if not isinstance(session, tt.Session):
            return

        session._java_api.jvm.io.atoti.loading.gcp.GcpPlugin.init()

    @property
    def jar_path(self) -> Optional[Path]:
        return Path(__file__).parent / "data" / "atoti-gcp.jar"
