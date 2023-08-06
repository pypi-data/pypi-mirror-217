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

from zenith.components.pool import Pool
from zenith.ext.singleton import Singleton

from zenith.ext.exceptions import PoolNotFound, PoolAlreadyExists, PermissionException


class PoolRegistry(Singleton):
    __service_pool = dict()

    @staticmethod
    def create_new_pool(
            pool: Pool,
            override: bool = False
    ) -> None:

        """
        Create new service pool

        Attributes:
        ------------
        :param pool:
        :param override:
        :return:
        ------------
        """

        if pool.get_pool_name() in PoolRegistry.__service_pool and override is False:
            raise PoolAlreadyExists("Service pool already exists")

        PoolRegistry.__service_pool[pool.get_pool_name()] = pool

    @staticmethod
    def delete_pool_by_name(
            name: str
    ) -> None:

        """
        Delete a service pool

        Attributes:
        ------------
        :param name:
        :return:
        ------------
        """

        if name not in PoolRegistry.__service_pool:
            raise PoolNotFound("Service pool not found")

        del PoolRegistry.__service_pool[name]

    @staticmethod
    def delete_pool_by_priority(priority: int) -> None:

        """
        Delete a service pool by priority

        Attributes:
        ------------
        :param priority:
        :return:
        ------------
        """

        if priority == 0:
            raise PermissionException("Cannot delete default priority pool")

        for pool in PoolRegistry.__service_pool.values():
            if pool.get_pool_priority() == priority:
                del PoolRegistry.__service_pool[pool.get_pool_name()]
                break

    @staticmethod
    def get_pool_by_name(name: str) -> Pool:

        """
        Get a service pool

        Attributes:
        ------------
        :param name:
        :return:
        ------------
        """

        if name not in PoolRegistry.__service_pool:
            raise PoolNotFound("Service pool not found")

        return PoolRegistry.__service_pool[name]

    @staticmethod
    def get_all_pools() -> list:

        """
        Get all service pools

        Attributes:
        ------------
        :return:
        ------------
        """

        return [pool for pool in PoolRegistry.__service_pool.values()]

    @staticmethod
    def get_all_default_priority_pools() -> list:

        """
        Get all service pools with default priority

        Attributes:
        ------------
        :return:
        ------------
        """

        return [pool for pool in PoolRegistry.__service_pool.values() if pool.get_pool_priority() == 0]

    @staticmethod
    def nums_of_pools() -> int:

        """
        Get the number of service pools

        Attributes:
        ------------
        :return:
        ------------
        """

        return len(PoolRegistry.__service_pool)
