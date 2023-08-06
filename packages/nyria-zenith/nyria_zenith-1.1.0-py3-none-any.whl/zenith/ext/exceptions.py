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

class PoolNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class PoolAlreadyExists(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class PodNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class PodAlreadyExists(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class PermissionException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class PriorityAlreadyExists(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
