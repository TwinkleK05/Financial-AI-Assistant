import logging

from typing import List

from config import ROLE_PERMISSIONS

from .database import Chunk

logger = logging.getLogger(__name__)

# ==================================================
# ACCESS CHECK
# ==================================================
def has_access(
    user_role: str,
    resource_access: str
) -> bool:
    """
    Check whether the user's role
    is allowed to access the resource.
    """

    logger.info(
        f"Checking access for role '{user_role}'."
    )

    normalized_role = user_role.strip().lower()

    permissions = [
        permission.lower()
        for permission in ROLE_PERMISSIONS.get(
            user_role.strip().upper()
            if user_role.strip().upper() in ROLE_PERMISSIONS
            else user_role.strip().title(),
            []
        )
    ]

    logger.info(
        f"Permissions: {permissions}"
    )

    return resource_access.strip().lower() in permissions

# ==================================================
# FILTER CHUNKS
# ==================================================

def filter_chunks(
    chunks: List[Chunk],
    user_role: str
) -> List[Chunk]:
    """
    Filter retrieved chunks according
    to the user's permissions.
    """

    logger.info(
        "Filtering retrieved chunks..."
    )

    authorized_chunks = []

    for chunk in chunks:

        if has_access(
            user_role,
            chunk.access
        ):
            authorized_chunks.append(chunk)

    logger.info(
        f"Authorized chunks: {len(authorized_chunks)}"
    )

    return authorized_chunks

# ==================================================
# AUTHORIZE RETRIEVAL
# ==================================================

def authorize_retrieval(
    chunks: List[Chunk],
    user_role: str
) -> List[Chunk]:
    """
    Apply RBAC filtering
    before generation.
    """

    logger.info(
        "Authorizing retrieved chunks..."
    )

    authorized_chunks = filter_chunks(
        chunks,
        user_role
    )

    if not authorized_chunks:

        logger.warning(
            "User has no permission to access retrieved chunks."
        )

    return authorized_chunks


