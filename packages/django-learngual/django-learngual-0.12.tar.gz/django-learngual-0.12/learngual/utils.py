import logging
from typing import Any, Literal

import requests
from django.core.cache import cache

# from django.utils import timezone


def get_service_request_headers(**kwargs) -> dict:
    """function add headers needed for request made from a service

    Returns:
        dict: _description_
    """

    return {**kwargs}


def get_service_request_params(**kwargs) -> str:
    """function return query params needed to make request as a service

    Returns:
        dict: _description_
    """

    return ""


def get_nested_value(data: dict[str, Any], path: str):
    """
    Retrieve a nested dictionary value using a dot path, including support for accessing lists and slicing.

    Args:
        data (Dict[str, Any]): The nested dictionary to traverse.
        path (str): The dot-separated path to the desired value.

    Returns:
        The value at the specified path if found, otherwise None.

    Example:
        data = {
            'foo': {
                'bar': [
                    {'baz': 42},
                    {'qux': [1, 2, 3, 4, 5]}
                ]
            }
        }

        result = get_nested_value(data, 'foo.bar[0].baz')
        # Output: 42

        result = get_nested_value(data, 'foo.bar[1].qux[2]')
        # Output: 3

        result = get_nested_value(data, 'foo.bar[1].qux[1:4]')
        # Output: [2, 3, 4]

        result = get_nested_value(data, 'foo.bar[1].qux[:3]')
        # Output: [1, 2, 3]

        result = get_nested_value(data, 'foo.bar[1].qux[2:]')
        # Output: [3, 4, 5]

        result = get_nested_value(data, 'foo.bar[1].qux[5]')
        # Output: None (Index out of range)

        result = get_nested_value(data, 'foo.bar[1].qux[4:2]')
        # Output: None (Invalid slice range)
    """
    keys = path.split(".")
    value = data

    try:
        for key in keys:
            if key.endswith("]"):
                key, index_or_slice = key[:-1].split("[")
                if ":" in index_or_slice:
                    start, stop = map(int, index_or_slice.split(":"))
                    value = value[key][start:stop]
                else:
                    index = int(index_or_slice)
                    value = value[key][index]
            else:
                value = value[key]
    except (KeyError, TypeError, IndexError, ValueError) as e:
        value = None
        logging.warning(
            f"An error occurred while retrieving nested value from path '{path}': {e}"
        )

    return value


def update_nested_value(data: dict[str, Any], path: str, value: Any) -> dict[str, Any]:
    """
    Update a nested dictionary value using a dot path and return the modified dictionary.

    Args:
        data (Dict[str, Any]): The nested dictionary to update.
        path (str): The dot-separated path to the value to update.
        value (Any): The new value to assign.

    Returns:
        Dict[str, Any]: The modified dictionary.

    Example:
        data = {
            'foo': {
                'bar': {
                    'baz': 42
                }
            }
        }

        updated_data = update_nested_value(data, 'foo.bar.baz', 99)
        # Now, updated_data['foo']['bar']['baz'] is 99

        updated_data = update_nested_value(data, 'foo.bar.qux', [1, 2, 3])
        # Now, updated_data['foo']['bar']['qux'] is [1, 2, 3]
    """
    keys = path.split(".")
    current_dict = data

    for key in keys[:-1]:
        if key not in current_dict or not isinstance(current_dict[key], dict):
            current_dict[key] = {}
        current_dict = current_dict[key]

    current_dict[keys[-1]] = value
    return data


def flatten_dict(
    data: dict[str, Any], parent_key: str = "", sep: str = "."
) -> dict[str, Any]:
    """
    Flatten a nested dictionary into a new dictionary with dot path keys.

    Args:
        data (Dict[str, Any]): The nested dictionary to flatten.
        parent_key (str): The parent key to use for the current level of the dictionary (used recursively).
        sep (str): The separator to use between the parent key and the current key.

    Returns:
        Dict[str, Any]: The flattened dictionary with dot path keys.

    Example:
        data = {
            'foo': {
                'bar': {
                    'baz': 42
                },
                'qux': [1, 2, 3]
            },
            'hello': 'world'
        }

        flattened_data = flatten_dict(data)
        # flattened_data is:
        # {
        #     'foo.bar.baz': 42,
        #     'foo.qux': [1, 2, 3],
        #     'hello': 'world'
        # }
    """
    flattened = {}
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened.update(flatten_dict(value, new_key, sep=sep))
        else:
            flattened[new_key] = value
    return flattened


def unflatten_dict(data: dict[str, Any], sep: str = ".") -> dict[str, Any]:
    """
    Convert a dictionary with dot path keys to a nested dictionary.

    Args:
        data (Dict[str, Any]): The dictionary with dot path keys to convert.
        sep (str): The separator used in the dot path keys.

    Returns:
        Dict[str, Any]: The nested dictionary.

    Example:
        data = {
            'foo.bar.baz': 42,
            'foo.qux': [1, 2, 3],
            'hello': 'world'
        }

        nested_data = unflatten_dict(data)
        # nested_data is:
        # {
        #     'foo': {
        #         'bar': {
        #             'baz': 42
        #         },
        #         'qux': [1, 2, 3]
        #     },
        #     'hello': 'world'
        # }
    """
    nested = {}
    for key, value in data.items():
        parts = key.split(sep)
        current_dict = nested
        for part in parts[:-1]:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
        current_dict[parts[-1]] = value
    return nested


class PermissonUtils:
    def __init__(self, permission: dict) -> None:
        """
        Example: {
            "id":1223344
            "metadata":{

            }
        }

        Args:
            permission (dict): _description_
        """
        assert type(permission) == dict, "permssion must be a dictionary"
        self.__permission = permission

    def to_dict(self) -> dict:
        """return a dictionary of modified permission

        Returns:
            dict: _description_
        """
        return self.__permission

    def to_flat_dict(
        self, parent_key: str = "", sep: str = ".", *args, **kwargs
    ) -> dict:
        """return a flat dictionary of modified permission

        Example:
        data = {
            'foo': {
                'bar': {
                    'baz': 42
                },
                'qux': [1, 2, 3]
            },
            'hello': 'world'
        }

        flattened_data = flatten_dict(data)
        # flattened_data is:
        # {
        #     'foo.bar.baz': 42,
        #     'foo.qux': [1, 2, 3],
        #     'hello': 'world'
        # }

        Returns:
            dict: _description_
        """
        return flatten_dict(
            self.to_dict(), parent_key=parent_key, sep=sep, *args, **kwargs
        )

    def bool(self, path: str):
        """retrieve a boolean value from a nested dictionary

        Args:
            path (str): Example: metadata.manage_course.value

        Returns:
            bool|None: _description_
        """
        res = get_nested_value(self.__permission, path)
        if res is not None:
            return str(res).strip().lower() in ["true", "1"] or res

    def int(self, path: str) -> int:
        """retrieve a boolean value from a nested dictionary

        Args:
            path (str): Example: metadata.request_count.value

        Returns:
            int: _description_
        """
        res = get_nested_value(self.__permission, path)
        try:
            return int(res or 0)
        except (ValueError, TypeError):
            return int()

    def float(self, path: str) -> float:
        """retrieve a boolean value from a nested dictionary

        Args:
            path (str): Example: metadata.audio_seconds.value

        Returns:
            float: _description_
        """
        res = get_nested_value(self.__permission, path)
        try:
            return float(res or 0)
        except (ValueError, TypeError):
            return float()

    def set_value(self, path: str, value: Any, force_create: bool = False) -> dict:
        """function is used to overwrite key in the permission

        Args:
            path (str): _description_
            value Any: Example: 10, -30, {"age":12}
            force_create (bool, optional): _description_. Defaults to False.

        Raises:
            KeyError: if key does not exist and force_create is equal to false

        Returns:
            dict: _description_
        """

        res = get_nested_value(self.__permission, path)

        if res is None and not force_create:
            raise KeyError(f"{path} does not exists")
        return update_nested_value(self.__permission, path, value)

    def add_number(self, path: str, number, force_create: bool = False) -> dict:  # noqa
        """function is used to increment or decrement

        Args:
            path (str): _description_
            number (float | int): Example: 10, -30
            force_create (bool, optional): _description_. Defaults to False.

        Raises:
            TypeError: if wrong type is passed as number
            KeyError: if key does not exist and force_create is equal to false

        Returns:
            dict: _description_
        """
        if type(number) == str and str(number).isdigit():
            number = float(number)

        res = get_nested_value(self.__permission, path)

        if res is None and not force_create:
            raise KeyError(f"{path} does not exists")

        if type(number) in [int, float]:
            data = (res + number) if type(res) in [int, float] else 0 + number
            return update_nested_value(self.__permission, path, data)
        else:
            raise TypeError(f"{number} must be of type int ot float")


class PermissionManager:
    def update_permission_with_event(
        self, event_name, routing_key, permission_data, permission_id
    ):
        ...

    def update_permission_with_api(
        self,
        base_url: str,
        permission_id,
        service: Literal["iam", "payment", "notify", "learn", "media"] = "iam",
        permmission_data=dict(),
    ):
        url_path = f"/{service}/v1/permission/{permission_id}/"
        res = requests.patch(base_url.rstrip("/") + url_path, json=permmission_data)
        if not res.ok:
            raise requests.exceptions.RequestException(res.content)
        return res.json()

    def retrieve_permission(
        self,
        *,
        base_url: str,
        permission_id,
        service: Literal["iam", "payment", "notify", "learn", "media"] = "iam",
        dot_path: str = None,
    ):
        """_summary_

        Args:
            permission_id (str): example: '123456', 'sdGh66gGGHgfadsty', 'product:1234567'
            service (_type_): "iam" | "pay" | "notify" | "learn" | "media"
            base_url (str):
            dot_path (str):Default:None, e.g metadata.request_count.value
        """
        url_path = f"/{service}/v1/permission/{permission_id}/"
        data = cache.get(url_path)

        if not data:
            res = requests.get(base_url.rstrip("/") + url_path)
            if not res.ok:
                raise requests.exceptions.RequestException(res.content)
            data = res.json()
            # TODO fine a way to remove the cache when a new permission is added
            # cache.set(url_path, data, timeout=timezone.timedelta(hours=1).total_seconds())

        if dot_path:
            return get_nested_value(data, dot_path)
        return data
