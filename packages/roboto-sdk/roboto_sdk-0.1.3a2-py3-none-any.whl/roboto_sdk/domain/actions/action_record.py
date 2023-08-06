import datetime
from typing import Any, Optional

import pydantic


class ActionRecord(pydantic.BaseModel):
    """
    Actions are unique by their org_id and name.

    Note: update Action.DISALLOWED_FOR_UPDATE if necessary when adding/updating/removing fields.
    """

    created: datetime.datetime  # Persisted as ISO 8601 string in UTC
    created_by: str
    modified: datetime.datetime  # Persisted as ISO 8601 string in UTC
    modified_by: str
    name: str  # Sort key
    org_id: str  # Partition key

    description: Optional[str] = None
    # Linked to `uri`; an Action may have a URI set but the container expected at that URI may not be available
    is_available: bool = False
    metadata: Optional[dict[str, Any]] = None
    tags: Optional[list[str]] = None
    uri: Optional[str] = None
