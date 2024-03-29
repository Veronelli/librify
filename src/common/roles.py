from enum import Enum


class AdminRoles(str, Enum):
    ADMIN_READ = "ADMIN_READ"
    ADMIN_WRITE = "ADMIN_WRITE"

    ADMIN_DELETE = "ADMIN_DELETE"
    ADMIN_UPDATE = "ADMIN_UPDATE"


class UserType(str, Enum):
    BASE_USER = "BASE_USER"
    PREMIUM_USER = "PREMIUM_USER"

    WRITER_USER = "WRITER_USER"
    ADMIN_USER = "ADMIN_USER"
    HELPER_USER = "HELPER_USER"
