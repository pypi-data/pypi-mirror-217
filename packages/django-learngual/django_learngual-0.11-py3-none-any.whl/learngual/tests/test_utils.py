from faker import Faker

from ..utils import (
    PermissonUtils,
    flatten_dict,
    get_nested_value,
    unflatten_dict,
    update_nested_value,
)

faker = Faker()


def test_update_nested_value():
    permission_data: dict = dict(
        metadata=dict(
            request_count=dict(
                value=faker.pyint(min_value=100, max_value=1000),
            ),
            manage_courses=dict(value=faker.pybool()),
            ids=[0, 1, 2, 3, 4, 5, 6],
            age=10,
        ),
    )
    res = update_nested_value(permission_data, "metadata.age", 20)
    assert res.get("metadata", {}).get("age") == 20
    assert permission_data.get("metadata", {}).get("age") == 20


def test_flatten_dict():
    permission_data: dict = dict(
        metadata=dict(
            request_count=dict(
                value=faker.pyint(min_value=100, max_value=1000),
            ),
            manage_courses=dict(value=faker.pybool()),
            ids=[0, 1, 2, 3, 4, 5, 6],
        ),
    )
    permission_data_flat = {
        "metadata.request_count.value": permission_data.get("metadata", {})
        .get("request_count", {})
        .get("value"),
        "metadata.manage_courses.value": permission_data.get("metadata", {})
        .get("manage_courses", {})
        .get("value"),
        "metadata.ids": permission_data.get("metadata", {}).get("ids"),
    }
    assert flatten_dict(permission_data) == permission_data_flat
    assert unflatten_dict(permission_data_flat) == permission_data


def test_get_nested_value():
    permission_data: dict = dict(
        metadata=dict(
            request_count=dict(
                value=faker.pyint(min_value=100, max_value=1000),
            ),
            manage_courses=dict(value=faker.pybool()),
            ids=[0, 1, 2, 3, 4, 5, 6],
        ),
    )
    assert get_nested_value(permission_data, "metadata.request_count.value")
    assert not get_nested_value(permission_data, "metadata.request_count.val")
    assert get_nested_value(permission_data, "metadata.request_count")
    assert (
        get_nested_value(permission_data, "metadata.ids[1]")
        == permission_data.get("metadata", {}).get("ids")[1]
    )
    assert (
        get_nested_value(permission_data, "metadata.ids[0:4]")
        == permission_data.get("metadata", {}).get("ids")[0:4]
    )


def test_PermissonUtils():
    permission_data: dict = dict(
        metadata=dict(
            request_count=dict(
                value=faker.pyint(min_value=100, max_value=1000),
            ),
            manage_courses=dict(value=faker.pybool()),
            value=20,
        ),
    )
    permission: PermissonUtils = PermissonUtils(permission_data)
    assert permission.bool("metadata.manage_courses.value") == permission_data.get(
        "metadata", {}
    ).get("manage_courses", {}).get("value")

    assert type(permission.bool("metadata.manage_courses.value")) == bool
    assert permission.bool("metadata.manage_courses.alue") is None

    assert permission.int("metadata.request_count.value") == permission_data.get(
        "metadata", {}
    ).get("request_count", {}).get("value")

    assert type(permission.int("metadata.request_count.value")) == int
    assert permission.int("metadata.request_count.alue") == int()

    assert type(permission.float("metadata.request_count.value")) == float

    # check increment works
    value = faker.pyint(min_value=1, max_value=100)
    res = permission.add_number("metadata.value", value)
    assert res.get("metadata", {}).get("value") == 20 + value

    # check that decrement works
    res = permission.add_number("metadata.value", -30)
    assert res.get("metadata", {}).get("value") == 20 + value - 30

    # check that error is raised if key does not exist
    try:
        permission.add_number("metadata.fake", -30)
        assert False, "did not raise key error"
    except KeyError:
        assert True

    # check that error is raised for wrong type
    try:
        permission.add_number("metadata.value", "334459aas")
        assert False, "did not raise type error"
    except TypeError:
        assert True

    # check that force create works
    assert permission.add_number("metadata.fake", -30, force_create=True)

    # check that force create works
    assert permission.set_value("metadata.fake2", -30, force_create=True)
    permission.set_value("metadata.value", -30)
    assert permission.to_dict().get("metadata", {}).get("value") == -30

    try:
        permission.set_value("metadata.fake4", -30)
        assert False
    except KeyError:
        assert True

    permission_data: dict = dict(
        metadata=dict(
            request_count=dict(
                value=faker.pyint(min_value=100, max_value=1000),
            ),
            manage_courses=dict(value=faker.pybool()),
            ids=[0, 1, 2, 3, 4, 5, 6],
        ),
    )
    permission_data_flat = {
        "metadata.request_count.value": permission_data.get("metadata", {})
        .get("request_count", {})
        .get("value"),
        "metadata.manage_courses.value": permission_data.get("metadata", {})
        .get("manage_courses", {})
        .get("value"),
        "metadata.ids": permission_data.get("metadata", {}).get("ids"),
    }
    assert PermissonUtils(permission_data).to_flat_dict() == permission_data_flat
    assert PermissonUtils(permission_data).to_dict() == permission_data
