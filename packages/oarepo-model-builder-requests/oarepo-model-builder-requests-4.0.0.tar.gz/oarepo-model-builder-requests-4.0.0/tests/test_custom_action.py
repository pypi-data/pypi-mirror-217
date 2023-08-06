from invenio_requests.records.api import RequestEventFormat
from test_custom_classes.request_test_actions import ActuallyApproveRecordAction
from thesis.proxies import current_service
from thesis.records.requests.types import CustomApproveActionRequestType


def test_action_changes_topic_status(
    app,
    identity_simple,
    identity_simple_2,
    submit_request,
    request_events_service,
    requests_service,
    example_topic,
    users,
    request_record_input_data,
):
    receiver_user = users[1]
    sender_identity = identity_simple
    receiver_identity = identity_simple_2
    request_types = app.extensions["invenio-requests"].request_type_registry
    for request_type in request_types:
        if not request_type == CustomApproveActionRequestType:
            continue
        assert request_type.available_actions["accept"] == ActuallyApproveRecordAction
        request = submit_request(
            sender_identity,
            data=request_record_input_data,
            topic=example_topic,
            request_type=request_type,
            receiver=receiver_user,
        )

        request_id = request.id

        # approve request by receiver
        payload = {
            "payload": {
                "content": "Ok doc1 is good enough and therefore approved.",
                "format": RequestEventFormat.HTML.value,
            }
        }
        # the reciever can
        requests_service.execute_action(
            receiver_identity, request_id, "accept", payload
        )
        assert (
            current_service.read(sender_identity, example_topic["id"])["metadata"][
                "status"
            ]
            == "approved"
        )  # this part checks whether the topic status was approved
