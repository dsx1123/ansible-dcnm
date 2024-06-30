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

import inspect

import pytest
from ansible_collections.cisco.dcnm.plugins.module_utils.common.response_handler import \
    ResponseHandler
from ansible_collections.cisco.dcnm.plugins.module_utils.common.rest_send_v2 import \
    RestSend
from ansible_collections.cisco.dcnm.plugins.module_utils.common.results import \
    Results
from ansible_collections.cisco.dcnm.plugins.module_utils.common.sender_file import \
    Sender
from ansible_collections.cisco.dcnm.tests.unit.module_utils.common.common_utils import \
    ResponseGenerator
from ansible_collections.cisco.dcnm.tests.unit.modules.dcnm.dcnm_image_policy.utils import (
    MockAnsibleModule, MockImagePolicies, does_not_raise,
    image_policy_create_bulk_fixture, params,
    payloads_image_policy_create_bulk, responses_ep_policies,
    responses_ep_policy_create, rest_send_result_current)


def test_image_policy_create_bulk_00000(image_policy_create_bulk) -> None:
    """
    Classes and Methods
    - ImagePolicyCreateCommon
        - __init__()
    - ImagePolicyCreateBulk
        - __init__()

    Summary
    Verify that __init__() sets class attributes to the expected values.

    Test
    - Class attributes are initialized to expected values
    - Exceptions are not raised.
    """
    with does_not_raise():
        instance = image_policy_create_bulk
    assert instance.class_name == "ImagePolicyCreateBulk"
    assert instance.action == "create"
    assert instance.params.get("state") == "merged"
    assert instance.params.get("check_mode") is False
    assert instance.endpoint.class_name == "EpPolicyCreate"
    assert instance.endpoint.verb == "POST"
    assert instance._mandatory_payload_keys == {
        "nxosVersion",
        "policyName",
        "policyType",
    }
    assert instance.payloads is None
    assert instance._payloads_to_commit == []


def test_image_policy_create_bulk_00010(image_policy_create_bulk) -> None:
    """
    ### Classes and Methods
    - ImagePolicyCreateCommon
        - __init__()
        - payloads setter
    - ImagePolicyCreateBulk
        - __init__()

    ### Summary
    Verify that the payloads setter sets the payloads attribute
    to the expected value.

    ### Test
    - payloads is set to expected value
    - Exceptions are not raised.
    """
    method_name = inspect.stack()[0][3]
    key = f"{method_name}a"

    with does_not_raise():
        instance = image_policy_create_bulk
        instance.payloads = payloads_image_policy_create_bulk(key)
    assert instance.payloads == payloads_image_policy_create_bulk(key)


def test_image_policy_create_bulk_00021(image_policy_create_bulk) -> None:
    """
    ### Classes and Methods
        -   ImagePolicyCreateCommon
                -   __init__()
                -   payloads.setter
        -   ImagePolicyCreateBulk
                -   __init__()

    ### Summary
    Verify that the payloads setter raises TypeError when payloads is not
    a list of dict.

    ### Test
    - TypeError is raised because payloads is not a list of dict
    - instance.payloads is not modified, hence it retains its initial value of None
    """
    method_name = inspect.stack()[0][3]
    key = f"{method_name}a"

    match = "ImagePolicyCreateBulk.payloads: "
    match += "payloads must be a list of dict. got dict for value"

    with does_not_raise():
        instance = image_policy_create_bulk
        instance.results = Results()
    with pytest.raises(TypeError, match=match):
        instance.payloads = payloads_image_policy_create_bulk(key)
    assert instance.payloads is None


@pytest.mark.parametrize(
    "key, match",
    [
        ("test_image_policy_create_bulk_00022a", "nxosVersion"),
        ("test_image_policy_create_bulk_00022b", "policyName"),
        ("test_image_policy_create_bulk_00022c", "policyType"),
    ],
)
def test_image_policy_create_bulk_00022(image_policy_create_bulk, key, match) -> None:
    """
    ### Classes and Methods
    - ImagePolicyCreateCommon
        - __init__()
        - payloads setter
    - ImagePolicyCreateBulk
        - __init__()

    ### Summary
    Verify that the payloads setter raises ``ValueError`` when a payload in
    the payloads list is missing a mandatory key.

    ### Test
    -   ``ValueError`` is raised because a payload in the payloads list is
        missing a mandatory key.
    -   instance.payloads is not modified, hence it retains its initial value
        of None.
    """
    with does_not_raise():
        instance = image_policy_create_bulk
        instance.results = Results()
    with pytest.raises(ValueError, match=match):
        instance.payloads = payloads_image_policy_create_bulk(key)
    assert instance.payloads is None


def test_image_policy_create_bulk_00030(monkeypatch, image_policy_create_bulk) -> None:
    """
    ### Classes and Methods
    - ImagePolicyCreateCommon
        - __init__()
        - payloads setter
        - build_payloads_to_commit()
    - ImagePolicyCreateBulk
        - __init__()

    ### Summary
    Verify behavior when the user sends an image create payload for an
    image policy that already exists on the controller.

    ### Setup
    -   ImagePolicies().all_policies, called from instance.build_payloads_to_commit(),
        is mocked to indicate that two image policies (KR5M, NR3F) exist on the
        controller.
    -   ImagePolicyCreateCommon().payloads is set to contain one payload (KR5M)
        that is present in all_policies.

    ### Test
    -   payloads_to_commit will an empty list because all payloads in
        instance.payloads exist on the controller.
    """
    method_name = inspect.stack()[0][3]
    key = f"{method_name}a"

    instance = image_policy_create_bulk
    instance.results = Results()
    instance.payloads = payloads_image_policy_create_bulk(key)
    monkeypatch.setattr(instance, "_image_policies", MockImagePolicies(key))
    instance.build_payloads_to_commit()
    assert instance._payloads_to_commit == []
    assert len(instance.results.failed) == 0
    assert len(instance.results.changed) == 0


def test_image_policy_create_bulk_00031(monkeypatch, image_policy_create_bulk) -> None:
    """
    ### Classes and Methods
    - ImagePolicyCreateCommon
        - __init__()
        - payloads setter
        - build_payloads_to_commit()
    - ImagePolicyCreateBulk
        - __init__()

    ### Summary
    Verify that instance.build_payloads_to_commit() adds a payload to the
    payloads_to_commit list when a request is made to create an image policy
    that does not exist on the controller.

    ### Setup
    -   ImagePolicies().all_policies, called from instance.build_payloads_to_commit(),
        is mocked to indicate that two image policies (KR5M, NR3F) exist on the
        controller.
    -   ImagePolicyCreateCommon().payloads is set to contain one payload containing
        an image policy (FOO) that is not present in all_policies.

    ### Test
    -   _payloads_to_commit will equal instance.payloads since none of the
        image policies in instance.payloads exist on the controller.
    """
    method_name = inspect.stack()[0][3]
    key = f"{method_name}a"

    with does_not_raise():
        instance = image_policy_create_bulk
        instance.results = Results()
        instance.payloads = payloads_image_policy_create_bulk(key)
        monkeypatch.setattr(instance, "_image_policies", MockImagePolicies(key))
        instance.build_payloads_to_commit()
    assert len(instance._payloads_to_commit) == 1
    assert instance._payloads_to_commit == payloads_image_policy_create_bulk(key)


def test_image_policy_create_bulk_00032(monkeypatch, image_policy_create_bulk) -> None:
    """
    ### Classes and Methods
    - ImagePolicyCreateCommon
        - payloads setter
        - build_payloads_to_commit()
    - ImagePolicyCreateBulk
        - __init__()

    ### Summary
    Verify that instance.build_payloads_to_commit() adds a payload to the
    payloads_to_commit list when the image policy in the payload does not
    on the controller.

    ### Setup
    -   ImagePolicies().all_policies, called from
        instance.build_payloads_to_commit(), is mocked to indicate that two
        image policies (KR5M, NR3F) exist on the controller.
    -   ImagePolicyCreateCommon().payloads is set to contain one payload
        containing an image policy (FOO) that is not present in all_policies
        and one payload containing an image policy (KR5M) that does exist on
        the controller.

    ### Test
    -   _payloads_to_commit will contain one payload
    -   The policyName for this payload will be "FOO", which is the image
        policy that does not exist on the controller
    """
    method_name = inspect.stack()[0][3]
    key = f"{method_name}a"

    instance = image_policy_create_bulk
    instance.payloads = payloads_image_policy_create_bulk(key)
    monkeypatch.setattr(instance, "_image_policies", MockImagePolicies(key))
    instance.build_payloads_to_commit()
    assert len(instance._payloads_to_commit) == 1
    assert instance._payloads_to_commit[0]["policyName"] == "FOO"


def test_image_policy_create_bulk_00033(image_policy_create_bulk) -> None:
    """
    ### Classes and Methods
    - ImagePolicyCreateBulk
        - commit()

    ### Summary
    Verify that ImagePolicyCreateBulk.commit() raises ``ValueError`` when
    payloads is None.

    ### Setup
    -   ImagePolicyCreateCommon().payloads is not set.

    ### Test
    -   ValueError is called because payloads is None.
    """
    with does_not_raise():
        results = Results()
        instance = image_policy_create_bulk
        instance.results = results

    match = r"ImagePolicyCreateBulk\.commit:\s+"
    match += r"payloads must be set prior to calling commit\."
    with pytest.raises(ValueError, match=match):
        instance.commit()


def test_image_policy_create_bulk_00034(monkeypatch, image_policy_create_bulk) -> None:
    """
    ### Classes and Methods
    - ImagePolicyCreateCommon
        - payloads setter
    - ImagePolicyCreateBulk
        - commit()

    ### Summary
    Verify that ImagePolicyCreateBulk.commit() returns without doing anything
    if payloads is an empty list.

    ### Setup
    -   ImagePolicyCreateCommon().payloads is set to an empty list

    ### Test
    -   ImagePolicyCreateBulk().results.changed is empty.
    """
    method_name = inspect.stack()[0][3]
    key = f"{method_name}a"

    with does_not_raise():
        instance = image_policy_create_bulk
        instance.payloads = []

    monkeypatch.setattr(instance, "_image_policies", MockImagePolicies(key))

    with does_not_raise():
        instance.rest_send = RestSend(params)
        instance.results = Results()
        instance.commit()
    assert len(instance.results.changed) == 0


def test_image_policy_create_bulk_00035(image_policy_create_bulk) -> None:
    """
    ### Classes and Methods
    - ImagePolicyCreateCommon
        - build_payloads_to_commit()
        - send_payloads()
    - ImagePolicyCreateBulk
        - payloads setter
        - commit()

    ### Summary
    Verify ImagePolicyCreateBulk.commit() happy path.  Controller responds
    to an image create request with a 200 response.

    ### Setup responses
    -   EpPolicies endpoint response contains DATA indicating no image policies
        exist on the controller.
    -   ImagePolicyCreateCommon().payloads is set to contain one payload that
        contains an image policy (FOO) which does not exist on the controller.
    -   EpPolicyCreate endpoint response contains a 200 response.

    ### Test
    -   commit calls build_payloads_to_commit which returns one payload.
    -   commit calls send_payloads, which calls rest_send, which populates
        diff_current with the payload due to result_current indicating
        success.
    -   results.result_current is set to the expected value
    -   results.diff_current is set to the expected value
    -   results.response_current is set to the expected value
    -   results.action is set to "create"
    """
    method_name = inspect.stack()[0][3]
    key = f"{method_name}a"

    def responses():
        yield responses_ep_policies(key)
        yield responses_ep_policy_create(key)

    gen_responses = ResponseGenerator(responses())

    def payloads():
        yield payloads_image_policy_create_bulk(key)

    gen_payloads = ResponseGenerator(payloads())

    sender = Sender()
    sender.ansible_module = MockAnsibleModule()
    sender.gen = gen_responses
    rest_send = RestSend(params)
    rest_send.response_handler = ResponseHandler()
    rest_send.sender = sender

    with does_not_raise():
        instance = image_policy_create_bulk
        instance.results = Results()
        instance.rest_send = rest_send
        instance.params = params

    with does_not_raise():
        instance.payloads = gen_payloads.next
        instance.commit()

    response_current = responses_ep_policy_create(key)
    response_current["sequence_number"] = 1

    result_current = rest_send_result_current(key)
    result_current["sequence_number"] = 1

    payload = payloads_image_policy_create_bulk(key)[0]
    payload["sequence_number"] = 1

    assert instance.results.action == "create"
    assert instance.rest_send.result_current == rest_send_result_current(key)
    assert instance.results.result_current == result_current
    assert instance.results.response_current == response_current
    assert instance.results.diff_current == payload
    assert False in instance.results.failed
    assert True not in instance.results.failed
    assert False not in instance.results.changed
    assert True in instance.results.changed
    assert len(instance.results.metadata) == 1
    assert instance.results.metadata[0]["action"] == "create"
    assert instance.results.metadata[0]["state"] == "merged"
    assert instance.results.metadata[0]["sequence_number"] == 1


def test_image_policy_create_bulk_00036(image_policy_create_bulk) -> None:
    """
    ### Classes and Methods
    - ImagePolicyCreateCommon
        - payloads setter
        - build_payloads_to_commit()
        - send_payloads()
    - ImagePolicyCreateBulk
        - commit()

    ### Summary
    Verify ImagePolicyCreateBulk.commit() sad path. Controller returns a 500
    response to an image policy create request.

    ### Setup
    -   EpPolicies endpoint response contains DATA indicating no image policies
        exist on the controller.
    -   ImagePolicyCreateBulk().payloads is set to contain one payload that
        contains an image policy (FOO) which does not exist on the controller.
    -   EpPolicyCreate endpoint response contains a 500 response.

    ### Test
    -   A sequence_number key is added to instance.results.response_current
    -   instance.results.diff_current is set to a dict with only
        the key "sequence_number", since no changes were made
    -   instance.results.failed set() contains True and does not contain False
    -   instance.results.changed set() contains False and does not contain True
    -   instance.results.metadata contains one dict
    -   The value of instance.results.metadata "action" is "create"
    -   The value of instance.results.metadata "state" is "merged"
    -   The value of instance.results.metadata "sequence_number" is 1
    """
    method_name = inspect.stack()[0][3]
    key = f"{method_name}a"

    def responses():
        yield responses_ep_policies(key)
        yield responses_ep_policy_create(key)

    gen_responses = ResponseGenerator(responses())

    def payloads():
        yield payloads_image_policy_create_bulk(key)

    gen_payloads = ResponseGenerator(payloads())

    sender = Sender()
    sender.ansible_module = MockAnsibleModule()
    sender.gen = gen_responses
    rest_send = RestSend(params)
    rest_send.response_handler = ResponseHandler()
    rest_send.sender = sender
    rest_send.unit_test = True

    with does_not_raise():
        instance = image_policy_create_bulk
        instance.results = Results()
        instance.rest_send = rest_send
        instance.params = params
        instance.payloads = gen_payloads.next
        instance.commit()

    response_current = responses_ep_policy_create(key)
    response_current["sequence_number"] = 1
    assert instance.results.response_current == response_current
    assert instance.results.diff_current == {"sequence_number": 1}
    assert True in instance.results.failed
    assert False not in instance.results.failed
    assert True not in instance.results.changed
    assert False in instance.results.changed
    assert len(instance.results.metadata) == 1
    assert len(instance.results.diff) == 1
    assert instance.results.diff[0] == {"sequence_number": 1}
    assert instance.results.metadata[0]["action"] == "create"
    assert instance.results.metadata[0]["state"] == "merged"
    assert instance.results.metadata[0]["sequence_number"] == 1


def test_image_policy_create_bulk_00037(image_policy_create_bulk) -> None:
    """
    ### Classes and Methods
    - ImagePolicyCreateCommon
        - _process_responses()
    - ImagePolicyCreateBulk
        - __init__()

    ### Summary
    Simulate a succussful response from the controller, followed by a bad response
    from the controller during policy create.

    ### Setup
    -   instance.payloads is set to contain two payloads

    ### Test
    - Both successful and bad responses are recorded with separate sequence_numbers.
    - instance.results.failed will be a set() containing both True and False
    - instance.results.changed will be a set() containing both True and False
    - instance.results.response contains two responses
    - instance.results.result contains two results
    - instance.results.diff contains two diffs
    """

    key_policies = "test_image_policy_create_bulk_00037a"
    key_ok = "test_image_policy_create_bulk_00037b"
    key_nok = "test_image_policy_create_bulk_00037c"
    key_payloads = "test_image_policy_create_bulk_00037d"

    def responses():
        yield responses_ep_policies(key_policies)
        yield responses_ep_policy_create(key_ok)
        yield responses_ep_policy_create(key_nok)

    gen_responses = ResponseGenerator(responses())

    def payloads():
        yield payloads_image_policy_create_bulk(key_payloads)

    gen_payloads = ResponseGenerator(payloads())

    sender = Sender()
    sender.ansible_module = MockAnsibleModule()
    sender.gen = gen_responses
    rest_send = RestSend(params)
    rest_send.response_handler = ResponseHandler()
    rest_send.sender = sender
    rest_send.unit_test = True

    with does_not_raise():
        instance = image_policy_create_bulk
        instance.results = Results()
        instance.rest_send = rest_send
        instance.payloads = gen_payloads.next
        instance.commit()

    assert len(instance.results.diff) == 2
    assert len(instance.results.result) == 2
    assert len(instance.results.response) == 2
    assert len(instance.results.metadata) == 2
    assert instance.results.response[0]["RETURN_CODE"] == 200
    assert instance.results.response[1]["RETURN_CODE"] == 500
    assert False in instance.results.changed
    assert True in instance.results.changed
    assert False in instance.results.failed
    assert True in instance.results.failed
