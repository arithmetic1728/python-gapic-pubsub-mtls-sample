# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
#

from unittest import mock

import grpc
import math
import pytest

from google import auth
from google.api_core import client_options
from google.api_core import grpc_helpers
from google.auth import credentials
from google.oauth2 import service_account
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.pubsub_v1.services.subscriber import SubscriberClient
from google.pubsub_v1.services.subscriber import pagers
from google.pubsub_v1.services.subscriber import transports
from google.pubsub_v1.types import pubsub


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert SubscriberClient._get_default_mtls_endpoint(None) == None
    assert SubscriberClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert SubscriberClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert SubscriberClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert SubscriberClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert SubscriberClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test_subscriber_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = SubscriberClient.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = SubscriberClient.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == 'pubsub.googleapis.com:443'


def test_subscriber_client_client_options():
    # Check that if channel is provided we won't create a new one.
    with mock.patch('google.pubsub_v1.services.subscriber.SubscriberClient.get_transport_class') as gtc:
        transport = transports.SubscriberGrpcTransport(
            credentials=credentials.AnonymousCredentials()
        )
        client = SubscriberClient(transport=transport)
        gtc.assert_not_called()

    # Check mTLS is not triggered with empty client options.
    options = client_options.ClientOptions()
    with mock.patch('google.pubsub_v1.services.subscriber.SubscriberClient.get_transport_class') as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = SubscriberClient(client_options=options)
        transport.assert_called_once_with(
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check mTLS is not triggered if api_endpoint is provided but
    # client_cert_source is None.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch('google.pubsub_v1.services.subscriber.transports.SubscriberGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = SubscriberClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )

    # Check mTLS is triggered if client_cert_source is provided.
    options = client_options.ClientOptions(
        client_cert_source=client_cert_source_callback
    )
    with mock.patch('google.pubsub_v1.services.subscriber.transports.SubscriberGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = SubscriberClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check mTLS is triggered if api_endpoint and client_cert_source are provided.
    options = client_options.ClientOptions(
        api_endpoint="squid.clam.whelk",
        client_cert_source=client_cert_source_callback
    )
    with mock.patch('google.pubsub_v1.services.subscriber.transports.SubscriberGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = SubscriberClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host="squid.clam.whelk",
        )

def test_subscriber_client_client_options_from_dict():
    with mock.patch('google.pubsub_v1.services.subscriber.transports.SubscriberGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = SubscriberClient(
            client_options={'api_endpoint': 'squid.clam.whelk'}
        )
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )


def test_create_subscription(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.Subscription()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_subscription),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription(
            name='name_value',
            topic='topic_value',
            ack_deadline_seconds=2066,
            retain_acked_messages=True,
            enable_message_ordering=True,
            filter='filter_value',
        )

        response = client.create_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Subscription)
    assert response.name == 'name_value'
    assert response.topic == 'topic_value'
    assert response.ack_deadline_seconds == 2066

    assert response.retain_acked_messages is True

    assert response.enable_message_ordering is True
    assert response.filter == 'filter_value'


def test_create_subscription_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_subscription),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_subscription(
            name='name_value',
            topic='topic_value',
            push_config=pubsub.PushConfig(push_endpoint='push_endpoint_value'),
            ack_deadline_seconds=2066,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'
        assert args[0].topic == 'topic_value'
        assert args[0].push_config == pubsub.PushConfig(push_endpoint='push_endpoint_value')
        assert args[0].ack_deadline_seconds == 2066


def test_create_subscription_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_subscription(
            pubsub.Subscription(),
            name='name_value',
            topic='topic_value',
            push_config=pubsub.PushConfig(push_endpoint='push_endpoint_value'),
            ack_deadline_seconds=2066,
        )


def test_get_subscription(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.GetSubscriptionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_subscription),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription(
            name='name_value',
            topic='topic_value',
            ack_deadline_seconds=2066,
            retain_acked_messages=True,
            enable_message_ordering=True,
            filter='filter_value',
        )

        response = client.get_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Subscription)
    assert response.name == 'name_value'
    assert response.topic == 'topic_value'
    assert response.ack_deadline_seconds == 2066

    assert response.retain_acked_messages is True

    assert response.enable_message_ordering is True
    assert response.filter == 'filter_value'


def test_get_subscription_field_headers():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.GetSubscriptionRequest(
        subscription='subscription/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_subscription),
            '__call__') as call:
        call.return_value = pubsub.Subscription()
        client.get_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'subscription=subscription/value',
    ) in kw['metadata']


def test_get_subscription_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_subscription),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_subscription(
            subscription='subscription_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].subscription == 'subscription_value'


def test_get_subscription_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_subscription(
            pubsub.GetSubscriptionRequest(),
            subscription='subscription_value',
        )


def test_update_subscription(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.UpdateSubscriptionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_subscription),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription(
            name='name_value',
            topic='topic_value',
            ack_deadline_seconds=2066,
            retain_acked_messages=True,
            enable_message_ordering=True,
            filter='filter_value',
        )

        response = client.update_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Subscription)
    assert response.name == 'name_value'
    assert response.topic == 'topic_value'
    assert response.ack_deadline_seconds == 2066

    assert response.retain_acked_messages is True

    assert response.enable_message_ordering is True
    assert response.filter == 'filter_value'


def test_list_subscriptions(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.ListSubscriptionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_subscriptions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListSubscriptionsResponse(
            next_page_token='next_page_token_value',
        )

        response = client.list_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSubscriptionsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_subscriptions_field_headers():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListSubscriptionsRequest(
        project='project/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_subscriptions),
            '__call__') as call:
        call.return_value = pubsub.ListSubscriptionsResponse()
        client.list_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'project=project/value',
    ) in kw['metadata']


def test_list_subscriptions_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_subscriptions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListSubscriptionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_subscriptions(
            project='project_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project == 'project_value'


def test_list_subscriptions_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_subscriptions(
            pubsub.ListSubscriptionsRequest(),
            project='project_value',
        )


def test_list_subscriptions_pager():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_subscriptions),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSubscriptionsResponse(
                subscriptions=[
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                ],
                next_page_token='abc',
            ),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[],
                next_page_token='def',
            ),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[
                    pubsub.Subscription(),
                ],
                next_page_token='ghi',
            ),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                ],
            ),
            RuntimeError,
        )
        results = [i for i in client.list_subscriptions(
            request={},
        )]
        assert len(results) == 6
        assert all(isinstance(i, pubsub.Subscription)
                   for i in results)

def test_list_subscriptions_pages():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_subscriptions),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSubscriptionsResponse(
                subscriptions=[
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                ],
                next_page_token='abc',
            ),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[],
                next_page_token='def',
            ),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[
                    pubsub.Subscription(),
                ],
                next_page_token='ghi',
            ),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_subscriptions(request={}).pages)
        for page, token in zip(pages, ['abc','def','ghi', '']):
            assert page.raw_page.next_page_token == token


def test_delete_subscription(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.DeleteSubscriptionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.delete_subscription),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_subscription_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.delete_subscription),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.delete_subscription(
            subscription='subscription_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].subscription == 'subscription_value'


def test_delete_subscription_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_subscription(
            pubsub.DeleteSubscriptionRequest(),
            subscription='subscription_value',
        )


def test_modify_ack_deadline(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.ModifyAckDeadlineRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.modify_ack_deadline),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.modify_ack_deadline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_modify_ack_deadline_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.modify_ack_deadline),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.modify_ack_deadline(
            subscription='subscription_value',
            ack_ids=['ack_ids_value'],
            ack_deadline_seconds=2066,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].subscription == 'subscription_value'
        assert args[0].ack_ids == ['ack_ids_value']
        assert args[0].ack_deadline_seconds == 2066


def test_modify_ack_deadline_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.modify_ack_deadline(
            pubsub.ModifyAckDeadlineRequest(),
            subscription='subscription_value',
            ack_ids=['ack_ids_value'],
            ack_deadline_seconds=2066,
        )


def test_acknowledge(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.AcknowledgeRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.acknowledge),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.acknowledge(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_acknowledge_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.acknowledge),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.acknowledge(
            subscription='subscription_value',
            ack_ids=['ack_ids_value'],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].subscription == 'subscription_value'
        assert args[0].ack_ids == ['ack_ids_value']


def test_acknowledge_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.acknowledge(
            pubsub.AcknowledgeRequest(),
            subscription='subscription_value',
            ack_ids=['ack_ids_value'],
        )


def test_pull(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.PullRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.pull),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.PullResponse(
        )

        response = client.pull(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.PullResponse)


def test_pull_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.pull),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.PullResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.pull(
            subscription='subscription_value',
            return_immediately=True,
            max_messages=1277,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].subscription == 'subscription_value'
        assert args[0].return_immediately == True
        assert args[0].max_messages == 1277


def test_pull_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.pull(
            pubsub.PullRequest(),
            subscription='subscription_value',
            return_immediately=True,
            max_messages=1277,
        )


def test_streaming_pull(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.StreamingPullRequest()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.streaming_pull),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([pubsub.StreamingPullResponse()])

        response = client.streaming_pull(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, pubsub.StreamingPullResponse)


def test_modify_push_config(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.ModifyPushConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.modify_push_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.modify_push_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_modify_push_config_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.modify_push_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.modify_push_config(
            subscription='subscription_value',
            push_config=pubsub.PushConfig(push_endpoint='push_endpoint_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].subscription == 'subscription_value'
        assert args[0].push_config == pubsub.PushConfig(push_endpoint='push_endpoint_value')


def test_modify_push_config_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.modify_push_config(
            pubsub.ModifyPushConfigRequest(),
            subscription='subscription_value',
            push_config=pubsub.PushConfig(push_endpoint='push_endpoint_value'),
        )


def test_get_snapshot(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.GetSnapshotRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_snapshot),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot(
            name='name_value',
            topic='topic_value',
        )

        response = client.get_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Snapshot)
    assert response.name == 'name_value'
    assert response.topic == 'topic_value'


def test_get_snapshot_field_headers():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.GetSnapshotRequest(
        snapshot='snapshot/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_snapshot),
            '__call__') as call:
        call.return_value = pubsub.Snapshot()
        client.get_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'snapshot=snapshot/value',
    ) in kw['metadata']


def test_get_snapshot_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_snapshot),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_snapshot(
            snapshot='snapshot_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].snapshot == 'snapshot_value'


def test_get_snapshot_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_snapshot(
            pubsub.GetSnapshotRequest(),
            snapshot='snapshot_value',
        )


def test_list_snapshots(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.ListSnapshotsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_snapshots),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListSnapshotsResponse(
            next_page_token='next_page_token_value',
        )

        response = client.list_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSnapshotsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_snapshots_field_headers():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListSnapshotsRequest(
        project='project/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_snapshots),
            '__call__') as call:
        call.return_value = pubsub.ListSnapshotsResponse()
        client.list_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'project=project/value',
    ) in kw['metadata']


def test_list_snapshots_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_snapshots),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListSnapshotsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_snapshots(
            project='project_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project == 'project_value'


def test_list_snapshots_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_snapshots(
            pubsub.ListSnapshotsRequest(),
            project='project_value',
        )


def test_list_snapshots_pager():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_snapshots),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSnapshotsResponse(
                snapshots=[
                    pubsub.Snapshot(),
                    pubsub.Snapshot(),
                    pubsub.Snapshot(),
                ],
                next_page_token='abc',
            ),
            pubsub.ListSnapshotsResponse(
                snapshots=[],
                next_page_token='def',
            ),
            pubsub.ListSnapshotsResponse(
                snapshots=[
                    pubsub.Snapshot(),
                ],
                next_page_token='ghi',
            ),
            pubsub.ListSnapshotsResponse(
                snapshots=[
                    pubsub.Snapshot(),
                    pubsub.Snapshot(),
                ],
            ),
            RuntimeError,
        )
        results = [i for i in client.list_snapshots(
            request={},
        )]
        assert len(results) == 6
        assert all(isinstance(i, pubsub.Snapshot)
                   for i in results)

def test_list_snapshots_pages():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_snapshots),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSnapshotsResponse(
                snapshots=[
                    pubsub.Snapshot(),
                    pubsub.Snapshot(),
                    pubsub.Snapshot(),
                ],
                next_page_token='abc',
            ),
            pubsub.ListSnapshotsResponse(
                snapshots=[],
                next_page_token='def',
            ),
            pubsub.ListSnapshotsResponse(
                snapshots=[
                    pubsub.Snapshot(),
                ],
                next_page_token='ghi',
            ),
            pubsub.ListSnapshotsResponse(
                snapshots=[
                    pubsub.Snapshot(),
                    pubsub.Snapshot(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_snapshots(request={}).pages)
        for page, token in zip(pages, ['abc','def','ghi', '']):
            assert page.raw_page.next_page_token == token


def test_create_snapshot(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.CreateSnapshotRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_snapshot),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot(
            name='name_value',
            topic='topic_value',
        )

        response = client.create_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Snapshot)
    assert response.name == 'name_value'
    assert response.topic == 'topic_value'


def test_create_snapshot_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_snapshot),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_snapshot(
            name='name_value',
            subscription='subscription_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'
        assert args[0].subscription == 'subscription_value'


def test_create_snapshot_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_snapshot(
            pubsub.CreateSnapshotRequest(),
            name='name_value',
            subscription='subscription_value',
        )


def test_update_snapshot(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.UpdateSnapshotRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_snapshot),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot(
            name='name_value',
            topic='topic_value',
        )

        response = client.update_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Snapshot)
    assert response.name == 'name_value'
    assert response.topic == 'topic_value'


def test_delete_snapshot(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.DeleteSnapshotRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.delete_snapshot),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_snapshot_flattened():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.delete_snapshot),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.delete_snapshot(
            snapshot='snapshot_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].snapshot == 'snapshot_value'


def test_delete_snapshot_flattened_error():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_snapshot(
            pubsub.DeleteSnapshotRequest(),
            snapshot='snapshot_value',
        )


def test_seek(transport: str = 'grpc'):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.SeekRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.seek),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.SeekResponse(
        )

        response = client.seek(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.SeekResponse)


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.SubscriberGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SubscriberClient(
            credentials=credentials.AnonymousCredentials(),
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SubscriberGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = SubscriberClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client._transport,
        transports.SubscriberGrpcTransport,
    )


def test_subscriber_base_transport():
    # Instantiate the base transport.
    transport = transports.SubscriberTransport(
        credentials=credentials.AnonymousCredentials(),
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'create_subscription',
        'get_subscription',
        'update_subscription',
        'list_subscriptions',
        'delete_subscription',
        'modify_ack_deadline',
        'acknowledge',
        'pull',
        'streaming_pull',
        'modify_push_config',
        'get_snapshot',
        'list_snapshots',
        'create_snapshot',
        'update_snapshot',
        'delete_snapshot',
        'seek',
        )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_subscriber_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, 'default') as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        SubscriberClient()
        adc.assert_called_once_with(scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/pubsub',
        ))


def test_subscriber_host_no_port():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='pubsub.googleapis.com'),
        transport='grpc',
    )
    assert client._transport._host == 'pubsub.googleapis.com:443'


def test_subscriber_host_with_port():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='pubsub.googleapis.com:8000'),
        transport='grpc',
    )
    assert client._transport._host == 'pubsub.googleapis.com:8000'


def test_subscriber_grpc_transport_channel():
    channel = grpc.insecure_channel('http://localhost/')

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.SubscriberGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_subscriber_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.SubscriberGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        ssl_credentials=mock_ssl_cred,
        scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/pubsub',
        ),
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_subscriber_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.SubscriberGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            ssl_credentials=mock_ssl_cred,
            scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/pubsub',
            ),
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_snapshot_path():
    project = "squid"
    snapshot = "clam"

    expected = "projects/{project}/snapshots/{snapshot}".format(project=project, snapshot=snapshot, )
    actual = SubscriberClient.snapshot_path(project, snapshot)
    assert expected == actual


def test_parse_snapshot_path():
    expected = {
    "project": "whelk",
    "snapshot": "octopus",

    }
    path = SubscriberClient.snapshot_path(**expected)

    # Check that the path construction is reversible.
    actual = SubscriberClient.parse_snapshot_path(path)
    assert expected == actual

def test_subscription_path():
    project = "squid"
    subscription = "clam"

    expected = "projects/{project}/subscriptions/{subscription}".format(project=project, subscription=subscription, )
    actual = SubscriberClient.subscription_path(project, subscription)
    assert expected == actual


def test_parse_subscription_path():
    expected = {
    "project": "whelk",
    "subscription": "octopus",

    }
    path = SubscriberClient.subscription_path(**expected)

    # Check that the path construction is reversible.
    actual = SubscriberClient.parse_subscription_path(path)
    assert expected == actual
