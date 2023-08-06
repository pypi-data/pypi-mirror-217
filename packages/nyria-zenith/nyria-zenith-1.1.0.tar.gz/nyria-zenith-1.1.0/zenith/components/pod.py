#  All Rights Reserved
#  Copyright (c) 2023 Nyria
#
#  This code, including all accompanying software, documentation, and related materials, is the exclusive property
#  of Nyria. All rights are reserved.
#
#  Any use, reproduction, distribution, or modification of the code without the express written
#  permission of Nyria is strictly prohibited.
#
#  No warranty is provided for the code, and Nyria shall not be liable for any claims, damages,
#  or other liability arising from the use or inability to use the code.

from typing import Any

from zenith.stats.permission import Permission
from zenith.ext.exceptions import PermissionException


class Pod:
    def __init__(self, name: str, service_instance, permission: Permission, priority: int = 0):
        self.__name = name.lower()
        self.__service_instance = service_instance
        self.__priority = priority
        self.__permission = permission

    def get_name(self) -> str:

        """
        Get name
        :return:
        """

        return self.__name

    def get_service(self) -> Any:

        """
        Get service
        :return:
        """

        return self.__service_instance

    def get_priority(self) -> int:

        """
        Get priority
        :return:
        """

        return self.__priority

    def get_permission(self) -> Permission:

        """
        Get permission
        :return:
        """

        return self.__permission

    def set_new_service(
            self,
            service_instance: Any
    ) -> None:

        """
        Set new service
        :param service_instance:
        :return:
        """

        if self.__permission == Permission.READ_ONLY:
            raise PermissionException("Cannot set new service to read-only pod")

        self.__service_instance = service_instance

    def change_priority(
            self,
            priority: int
    ) -> None:

        """
        Change priority
        :param priority:
        :return:
        """

        if self.__permission == Permission.READ_ONLY:
            raise PermissionException("Cannot change priority of read-only pod")

        self.__priority = priority
