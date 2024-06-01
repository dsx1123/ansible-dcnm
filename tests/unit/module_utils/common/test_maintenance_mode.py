# Copyright (c) 2024 Cisco and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# See the following regarding *_fixture imports
# https://pylint.pycqa.org/en/latest/user_guide/messages/warning/redefined-outer-name.html
# Due to the above, we also need to disable unused-import
# Also, fixtures need to use *args to match the signature of the function they are mocking
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function

__metaclass__ = type

__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__author__ = "Allen Robel"

import copy
import inspect

import pytest
from ansible_collections.cisco.dcnm.plugins.module_utils.common.api.v1.lan_fabric.rest.control.fabrics.fabrics import (
    EpMaintenanceModeDisable, EpMaintenanceModeEnable)
from ansible_collections.cisco.dcnm.plugins.module_utils.common.conversion import \
    ConversionUtils
from ansible_collections.cisco.dcnm.plugins.module_utils.common.exceptions import \
    ControllerResponseError
from ansible_collections.cisco.dcnm.plugins.module_utils.common.maintenance_mode import \
    MaintenanceMode
from ansible_collections.cisco.dcnm.plugins.module_utils.common.response_handler import \
    ResponseHandler
from ansible_collections.cisco.dcnm.plugins.module_utils.common.rest_send_v2 import \
    RestSend
from ansible_collections.cisco.dcnm.plugins.module_utils.common.results import \
    Results
from ansible_collections.cisco.dcnm.tests.unit.module_utils.common.common_utils import (
    MockSender, ResponseGenerator, does_not_raise, maintenance_mode_fixture,
    params, responses_config_deploy, responses_maintenance_mode)

FABRIC_NAME = "VXLAN_Fabric"
CONFIG = [
    {
        "deploy": False,
        "fabric_name": f"{FABRIC_NAME}",
        "ip_address": "192.168.1.2",
        "mode": "maintenance",
        "serial_number": "FDO22180ASJ",
    }
]


def test_maintenance_mode_00000(maintenance_mode) -> None:
    """
    Classes and Methods
    - MaintenanceMode
        - __init__()

    Test
    - Class attributes are initialized to expected values
    - Exception is not raised
    """
    with does_not_raise():
        instance = maintenance_mode
    assert instance._properties["config"] is None
    assert instance._properties["rest_send"] is None
    assert instance._properties["results"] is None
    assert instance.action == "maintenance_mode"
    assert instance.class_name == "MaintenanceMode"
    assert instance.config is None
    assert instance.check_mode is False
    assert instance.deploy_dict == {}
    assert instance.serial_number_to_ip_address == {}
    assert instance.valid_modes == ["maintenance", "normal"]
    assert instance.state == "merged"
    assert instance.rest_send is None
    assert instance.results is None
    assert isinstance(instance.conversion, ConversionUtils)
    assert isinstance(instance.ep_maintenance_mode_disable, EpMaintenanceModeDisable)
    assert isinstance(instance.ep_maintenance_mode_enable, EpMaintenanceModeEnable)


def test_maintenance_mode_00010() -> None:
    """
    Classes and Methods
    - MaintenanceMode
        - __init__()

    Test
    - ``ValueError`` is raised when params is missing check_mode key.
    """
    params = {"state": "merged"}
    match = r"MaintenanceMode\.__init__:\s+"
    match += r"params is missing mandatory parameter: check_mode\."
    with pytest.raises(ValueError, match=match):
        instance = MaintenanceMode(params)  # pylint: disable=unused-variable


def test_maintenance_mode_00020() -> None:
    """
    Classes and Methods
    - MaintenanceMode
        - __init__()

    Test
    - ``ValueError`` is raised when params is missing state key.
    """
    params = {"check_mode": False}
    match = r"MaintenanceMode\.__init__:\s+"
    match += r"params is missing mandatory parameter: state\."
    with pytest.raises(ValueError, match=match):
        instance = MaintenanceMode(params)  # pylint: disable=unused-variable


def test_maintenance_mode_00030(maintenance_mode) -> None:
    """
    Classes and Methods
    - MaintenanceMode()
        - __init__()
        - verify_commit_parameters()
        - commit()

    Summary
    -   Verify MaintenanceMode().commit() raises ``ValueError`` when
        ``config`` is not set.

    Code Flow - Setup
    -   MaintenanceMode() is instantiated
    -   Other required attributes are set

    Code Flow - Test
    -   ``MaintenanceMode().commit()`` is called without having first set
        ``MaintenanceMode().config``

    Expected Result
    -   ``ValueError`` is raised
    -   Exception message matches expected
    """
    with does_not_raise():
        instance = maintenance_mode
        instance.rest_send = RestSend({})
        instance.results = Results()

    match = r"MaintenanceMode\.verify_commit_parameters: "
    match += r"MaintenanceMode\.config must be set before calling\s+"
    match += r"commit\."
    with pytest.raises(ValueError, match=match):
        instance.commit()


def test_maintenance_mode_00040(maintenance_mode) -> None:
    """
    Classes and Methods
    - MaintenanceMode()
        - __init__()
        - verify_commit_parameters()
        - commit()

    Summary
    -   Verify MaintenanceMode().commit() raises ``ValueError``
        when ``rest_send`` is not set.

    Code Flow - Setup
    -   MaintenanceMode() is instantiated
    -   Other required attributes are set

    Code Flow - Test
    -   MaintenanceMode().commit() is called without having
        first set MaintenanceMode().rest_send

    Expected Result
    -   ``ValueError`` is raised
    -   Exception message matches expected
    """
    with does_not_raise():
        instance = maintenance_mode
        instance.results = Results()
        instance.config = CONFIG

    match = r"MaintenanceMode\.verify_commit_parameters: "
    match += r"MaintenanceMode\.rest_send must be set before calling\s+"
    match += r"commit\."
    with pytest.raises(ValueError, match=match):
        instance.commit()


def test_maintenance_mode_00050(maintenance_mode) -> None:
    """
    Classes and Methods
    - MaintenanceMode()
        - __init__()
        - verify_commit_parameters()
        - commit()

    Summary
    -   Verify MaintenanceMode().commit() raises ``ValueError``
        when ``MaintenanceMode().results`` is not set.

    Code Flow - Setup
    -   MaintenanceMode() is instantiated
    -   Other required attributes are set

    Code Flow - Test
    -   MaintenanceMode().commit() is called without having
        first set MaintenanceMode().results

    Expected Result
    -   ``ValueError`` is raised
    -   Exception message matches expected
    """
    with does_not_raise():
        instance = maintenance_mode
        instance.rest_send = RestSend({})
        instance.config = CONFIG

    match = r"MaintenanceMode\.verify_commit_parameters: "
    match += r"MaintenanceMode\.results must be set before calling\s+"
    match += r"commit\."
    with pytest.raises(ValueError, match=match):
        instance.commit()


@pytest.mark.parametrize(
    "mock_exception, expected_exception, mock_message",
    [
        (ControllerResponseError, ValueError, "Bad controller response"),
        (TypeError, ValueError, "Bad type"),
        (ValueError, ValueError, "Bad value"),
    ],
)
def test_maintenance_mode_00200(
    monkeypatch, maintenance_mode, mock_exception, expected_exception, mock_message
) -> None:
    """
    Classes and Methods
    - MaintenanceMode()
        - __init__()
        - commit()

    Summary
    -   Verify MaintenanceMode().commit() raises ``ValueError`` when
        ``MaintenanceMode().change_system_mode`` raises any of:
            -   ``ControllerResponseError``
            -   ``TypeError``
            -   ``ValueError``


    Code Flow - Setup
    -   MaintenanceMode() is instantiated
    -   Required attributes are set
    -   change_system_mode() is mocked to raise each of the above exceptions

    Code Flow - Test
    -   MaintenanceMode().commit() is called for each exception

    Expected Result
    -   ``ValueError`` is raised
    -   Exception message matches expected
    """

    def mock_change_system_mode(*args, **kwargs):
        raise mock_exception(mock_message)

    with does_not_raise():
        instance = maintenance_mode
        instance.config = CONFIG
        instance.rest_send = RestSend({})
        instance.results = Results()

    monkeypatch.setattr(instance, "change_system_mode", mock_change_system_mode)
    with pytest.raises(expected_exception, match=mock_message):
        instance.commit()


@pytest.mark.parametrize(
    "mock_exception, expected_exception, mock_message",
    [
        (ControllerResponseError, ValueError, "Bad controller response"),
        (ValueError, ValueError, "Bad value"),
    ],
)
def test_maintenance_mode_00210(
    monkeypatch, maintenance_mode, mock_exception, expected_exception, mock_message
) -> None:
    """
    Classes and Methods
    - MaintenanceMode()
        - __init__()
        - commit()

    Summary
    -   Verify MaintenanceMode().commit() raises ``ValueError`` when
        ``MaintenanceMode().deploy_switches`` raises any of:
            -   ``ControllerResponseError``
            -   ``ValueError``


    Code Flow - Setup
    -   MaintenanceMode() is instantiated
    -   Required attributes are set
    -   change_system_mode() is mocked to do nothing
    -   deploy_switches() is mocked to raise each of the above exceptions

    Code Flow - Test
    -   MaintenanceMode().commit() is called for each exception

    Expected Result
    -   ``ValueError`` is raised
    -   Exception message matches expected
    """

    def mock_change_system_mode(*args, **kwargs):
        pass

    def mock_deploy_switches(*args, **kwargs):
        raise mock_exception(mock_message)

    with does_not_raise():
        instance = maintenance_mode
        instance.config = CONFIG
        instance.rest_send = RestSend({})
        instance.results = Results()

    monkeypatch.setattr(instance, "change_system_mode", mock_change_system_mode)
    monkeypatch.setattr(instance, "deploy_switches", mock_deploy_switches)
    with pytest.raises(expected_exception, match=mock_message):
        instance.commit()


@pytest.mark.parametrize(
    "mode",
    [
        ("maintenance"),
        ("normal"),
    ],
)
def test_maintenance_mode_00220(maintenance_mode, mode) -> None:
    """
    Classes and Methods
    - MaintenanceMode()
        - __init__()
        - commit()
        - change_system_mode()
        - deploy_switches()

    Summary
    - Verify commit() success case:
        -   RETURN_CODE is 200.
        -   Controller response contains expected structure and values.

    Code Flow - Setup
    -   MaintenanceMode() is instantiated
    -   Sender() is mocked to return expected responses
    -   Required attributes are set
    -   MaintenanceMode().commit() is called
    -   responses_MaintenanceMode contains a dict with:
        - RETURN_CODE == 200
        - DATA == {"status": "Success"}

    Code Flow - Test
    -   MaintenanceMode().commit() is called

    Expected Result
    -   Exception is not raised
    -   instance.response_data returns expected data
    -   MaintenanceMode()._properties are updated
    """
    method_name = inspect.stack()[0][3]
    key = f"{method_name}a"

    def responses():
        yield responses_maintenance_mode(key)
        yield responses_config_deploy(key)

    mock_sender = MockSender()
    mock_sender.gen = ResponseGenerator(responses())

    config = copy.deepcopy(CONFIG[0])
    config["mode"] = mode

    with does_not_raise():
        rest_send = RestSend({"state": "merged", "check_mode": False})
        rest_send.sender = mock_sender
        rest_send.response_handler = ResponseHandler()
        instance = maintenance_mode
        instance.rest_send = rest_send
        instance.rest_send.unit_test = True
        instance.rest_send.timeout = 1
        instance.results = Results()
        instance.config = [config]

    with does_not_raise():
        instance.commit()

    assert isinstance(instance.results.diff, list)
    assert isinstance(instance.results.metadata, list)
    assert isinstance(instance.results.response, list)
    assert isinstance(instance.results.result, list)
    assert instance.results.diff[0].get("fabric_name", None) == FABRIC_NAME
    assert instance.results.diff[0].get("ip_address", None) == "192.168.1.2"
    assert instance.results.diff[0].get("maintenance_mode", None) == mode
    assert instance.results.diff[0].get("sequence_number", None) == 1
    assert instance.results.diff[0].get("serial_number", None) == "FDO22180ASJ"

    assert instance.results.diff[1].get("config_deploy", None) is True
    assert instance.results.diff[1].get("sequence_number", None) == 2

    assert instance.results.metadata[0].get("action", None) == "maintenance_mode"
    assert instance.results.metadata[0].get("sequence_number", None) == 1
    assert instance.results.metadata[0].get("state", None) == "merged"

    assert instance.results.metadata[1].get("action", None) == "config_deploy"
    assert instance.results.metadata[1].get("sequence_number", None) == 2
    assert instance.results.metadata[1].get("state", None) == "merged"

    assert instance.results.response[0].get("DATA", {}).get("status") == "Success"
    assert instance.results.response[0].get("MESSAGE", None) == "OK"
    assert instance.results.response[0].get("RETURN_CODE", None) == 200
    assert instance.results.response[0].get("METHOD", None) == "POST"

    value = "Configuration deployment completed."
    assert instance.results.response[1].get("DATA", {}).get("status") == value
    assert instance.results.response[1].get("MESSAGE", None) == "OK"
    assert instance.results.response[1].get("RETURN_CODE", None) == 200
    assert instance.results.response[1].get("METHOD", None) == "POST"

    assert instance.results.result[0].get("changed", None) is True
    assert instance.results.result[0].get("success", None) is True

    assert instance.results.result[1].get("changed", None) is True
    assert instance.results.result[1].get("success", None) is True


def test_maintenance_mode_00300(maintenance_mode) -> None:
    """
    Classes and Methods
    - MaintenanceMode()
        - __init__()
        - verify_config_parameters()
        - config.setter

    Summary
    -   Verify MaintenanceMode().verify_config_parameters() raises
            -   ``TypeError`` if:
                    - value is not a list
    -   Verify MaintenanceMode().config.setter re-raises:
            -   ``TypeError`` as ``ValueError``

    Code Flow - Setup
    -   MaintenanceMode() is instantiated
    -   config is set to a non-list value

    Code Flow - Test
    -   MaintenanceMode().config.setter is accessed with non-list

    Expected Result
    -   verify_config_parameters() raises ``TypeError``.
    -   config.setter re-raises as ``ValueError``.
    -   Exception message matches expected.
    """
    with does_not_raise():
        instance = maintenance_mode
    match = r"MaintenanceMode\.verify_config_parameters:\s+"
    match += r"MaintenanceMode\.config must be a list\.\s+"
    match += r"Got type: str\."
    with pytest.raises(ValueError, match=match):
        instance.config = "NOT_A_LIST"


@pytest.mark.parametrize(
    "remove_param",
    [("deploy"), ("fabric_name"), ("ip_address"), ("mode"), ("serial_number")],
)
def test_maintenance_mode_00310(maintenance_mode, remove_param) -> None:
    """
    Classes and Methods
    - MaintenanceMode()
        - __init__()
        - verify_config_parameters()
        - config.setter

    Summary
    -   Verify MaintenanceMode().verify_config_parameters() raises
            -   ``ValueError`` if:
                    - deploy is missing from config
                    - fabric_name is missing from config
                    - ip_address is missing from config
                    - mode is missing from config
                    - serial_number is missing from config


    Code Flow - Setup
    -   MaintenanceMode() is instantiated

    Code Flow - Test
    -   MaintenanceMode().config is set to a dict with all of the above
        keys present, except that each key, in turn, is removed.

    Expected Result
    -   ``ValueError`` is raised
    -   Exception message matches expected
    """

    with does_not_raise():
        instance = maintenance_mode

    config = copy.deepcopy(CONFIG[0])
    del config[remove_param]
    match = rf"MaintenanceMode\.verify_{remove_param}:\s+"
    match += rf"config is missing mandatory key: {remove_param}\."
    with pytest.raises(ValueError, match=match):
        instance.config = [config]


@pytest.mark.parametrize(
    "param, raises",
    [
        (False, None),
        (True, None),
        (10, ValueError),
        ("FOO", ValueError),
        (["FOO"], ValueError),
        ({"FOO": "BAR"}, ValueError),
    ],
)
def test_maintenance_mode_00400(maintenance_mode, param, raises) -> None:
    """
    Classes and Methods
    - MaintenanceMode()
        - __init__()
        - verify_config_parameters()
        - config.setter

    Summary
    -   Verify MaintenanceMode().verify_config_parameters() re-raises
            -   ``ValueError`` if:
                    - ``deploy`` raises ``TypeError``

    Code Flow - Setup
    -   MaintenanceMode() is instantiated

    Code Flow - Test
    -   MaintenanceMode().config is set to a dict.
    -   The dict is updated with deploy set to valid and invalid
        values of ``deploy``

    Expected Result
    -   ``ValueError`` is raised when deploy is not a boolean
    -   Exception message matches expected
    -   Exception is not raised when deploy is a boolean
    """

    with does_not_raise():
        instance = maintenance_mode

    config = copy.deepcopy(CONFIG[0])
    config["deploy"] = param
    match = r"MaintenanceMode\.verify_deploy:\s+"
    match += r"Expected boolean for deploy\.\s+"
    match += r"Got type\s+"
    if raises:
        with pytest.raises(raises, match=match):
            instance.config = [config]
    else:
        instance.config = [config]
        assert instance.config[0]["deploy"] == param


@pytest.mark.parametrize(
    "param, raises",
    [
        ("MyFabric", None),
        ("MyFabric_123", None),
        ("10MyFabric", ValueError),
        ("_MyFabric", ValueError),
        ("MyFabric&BadFabric", ValueError),
    ],
)
def test_maintenance_mode_00500(maintenance_mode, param, raises) -> None:
    """
    Classes and Methods
    - MaintenanceMode()
        - __init__()
        - verify_config_parameters()
        - config.setter

    Summary
    -   Verify MaintenanceMode().verify_config_parameters() re-raises
            -   ``ValueError`` if:
                    - ``fabric_name`` raises ``ValueError`` due to being an
                        invalid value.

    Code Flow - Setup
    -   MaintenanceMode() is instantiated

    Code Flow - Test
    -   MaintenanceMode().config is set to a dict.
    -   The dict is updated with fabric_name set to valid and invalid
        values of ``fabric_name``

    Expected Result
    -   ``ValueError`` is raised when fabric_name is not a valid value
    -   Exception message matches expected
    -   Exception is not raised when fabric_name is a valid value
    """

    with does_not_raise():
        instance = maintenance_mode

    config = copy.deepcopy(CONFIG[0])
    config["fabric_name"] = param
    match = r"ConversionUtils\.validate_fabric_name:\s+"
    match += rf"Invalid fabric name: {param}\.\s+"
    match += r"Fabric name must start with a letter A-Z or a-z and contain\s+"
    match += r"only the characters in:"
    if raises:
        with pytest.raises(raises, match=match):
            instance.config = [config]
    else:
        instance.config = [config]
        assert instance.config[0]["fabric_name"] == param


@pytest.mark.parametrize(
    "param, raises",
    [
        ("maintenance", None),
        ("normal", None),
        (10, ValueError),
        (["192.168.1.2"], ValueError),
        ({"ip_address": "192.168.1.2"}, ValueError),
    ],
)
def test_maintenance_mode_00600(maintenance_mode, param, raises) -> None:
    """
    Classes and Methods
    - MaintenanceMode()
        - __init__()
        - verify_config_parameters()
        - config.setter

    Summary
    -   Verify MaintenanceMode().verify_config_parameters() re-raises
            -   ``ValueError`` if:
                    - ``mode`` raises ``ValueError`` due to being an
                        invalid value.

    Code Flow - Setup
    -   MaintenanceMode() is instantiated

    Code Flow - Test
    -   MaintenanceMode().config is set to a dict.
    -   The dict is updated with mode set to valid and invalid
        values of ``mode``

    Expected Result
    -   ``ValueError`` is raised when mode is not a valid value
    -   Exception message matches expected
    -   Exception is not raised when mode is a valid value
    """

    with does_not_raise():
        instance = maintenance_mode

    config = copy.deepcopy(CONFIG[0])
    config["mode"] = param
    match = r"MaintenanceMode\.verify_mode:\s+"
    match += r"mode must be one of\s+"
    if raises:
        with pytest.raises(raises, match=match):
            instance.config = [config]
    else:
        instance.config = [config]
        assert instance.config[0]["mode"] == param
