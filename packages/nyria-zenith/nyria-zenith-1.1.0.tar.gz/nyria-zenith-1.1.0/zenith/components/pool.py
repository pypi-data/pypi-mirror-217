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

from typing import Union

from zenith.components.pod import Pod
from zenith.stats.permission import Permission

from zenith.ext.exceptions import PodNotFound, PodAlreadyExists, PriorityAlreadyExists, PermissionException


class Pool:
    def __init__(self, name: str, permission: Permission, priority: int = 0):
        self.__name = name.lower()
        self.__priority = priority
        self.__permission = permission

        self.__pods = dict()

    def register_pod(
            self,
            pod: Pod,
            override: bool = False
    ) -> None:

        """
        Register a new service to the pool
        :param pod:
        :param override:
        :return:
        """

        if pod.get_name() in self.__pods and override is False:
            raise PodAlreadyExists("Service already exists")

        for registered_pod in self.__pods.values():
            if pod.get_priority() == registered_pod.get_priority() and pod.get_priority() != 0:
                raise PriorityAlreadyExists("Priority already exists")

        if override and self.__permission == Permission.READ_ONLY:
            raise PermissionException("This pool is read only")

        self.__pods[pod.get_name()] = pod

    def register_pods(self, pods: list[Pod], override: bool = False) -> None:

        """
        Register multiple services to one the pool

        Attributes
        ----------
        :param override:
        :param pods:
        :return:
        ----------
        """

        for pod in pods:
            self.register_pod(pod, override)

    def unregister_pod(
            self,
            pod: Pod
    ) -> None:

        """
        Unregister a service from the pool
        :param pod:
        :return:
        """

        if pod.get_permission() == Permission.READ_ONLY:
            raise PermissionException("This pool is read only")

        del self.__pods[pod.get_name()]

    def get_pod_by_name(
            self,
            name: str
    ) -> Pod:

        """
        Get service from the pool
        :param name:
        :return:
        """

        if name not in self.__pods:
            raise PodNotFound("Service not found")

        return self.__pods[name]

    def get_pod_by_priority(
            self,
            priority: int
    ) -> Union[Pod, list[Pod]]:

        """
        Get service from the pool by priority
        :param priority:
        :return:
        """

        if priority == 0:
            return [pod for pod in self.__pods.values() if pod.get_priority() == 0]

        for pod in self.__pods.values():
            if pod.get_priority() == priority:
                return pod

        raise PodNotFound("Pod not found")

    def get_all_default_priority_pods(self) -> list[Pod]:

        """
        Get all services from the pool
        :return:
        """

        return [pod for pod in self.__pods.values() if pod.get_priority() == 0]

    def get_pool_permission(self) -> Permission:

        """
        Get pool permission
        :return:
        """

        return self.__permission

    def get_pool_priority(self) -> int:

        """
        Get pool priority
        :return:
        """

        return self.__priority

    def get_pool_name(self) -> str:

        """
        Get pool name
        :return:
        """

        return self.__name

    def get_all_pods(self) -> list[Pod]:

        """
        Get all pods
        :return:
        """

        return list(self.__pods.values())

    def nums_of_pods(self) -> int:

        """
        Get number of pods
        :return:
        """

        return len(self.__pods)
