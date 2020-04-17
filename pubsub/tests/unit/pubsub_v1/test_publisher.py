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
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.pubsub_v1.services.publisher import PublisherClient
from google.pubsub_v1.services.publisher import pagers
from google.pubsub_v1.services.publisher import transports
from google.pubsub_v1.types import pubsub


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert PublisherClient._get_default_mtls_endpoint(None) == None
    assert PublisherClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert PublisherClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert PublisherClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert PublisherClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert PublisherClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test_publisher_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = PublisherClient.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = PublisherClient.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == 'pubsub.googleapis.com:443'


def test_publisher_client_client_options():
    # Check that if channel is provided we won't create a new one.
    with mock.patch('google.pubsub_v1.services.publisher.PublisherClient.get_transport_class') as gtc:
        transport = transports.PublisherGrpcTransport(
            credentials=credentials.AnonymousCredentials()
        )
        client = PublisherClient(transport=transport)
        gtc.assert_not_called()

    # Check mTLS is not triggered with empty client options.
    options = client_options.ClientOptions()
    with mock.patch('google.pubsub_v1.services.publisher.PublisherClient.get_transport_class') as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = PublisherClient(client_options=options)
        transport.assert_called_once_with(
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check mTLS is not triggered if api_endpoint is provided but
    # client_cert_source is None.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch('google.pubsub_v1.services.publisher.transports.PublisherGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = PublisherClient(client_options=options)
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
    with mock.patch('google.pubsub_v1.services.publisher.transports.PublisherGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = PublisherClient(client_options=options)
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
    with mock.patch('google.pubsub_v1.services.publisher.transports.PublisherGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = PublisherClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host="squid.clam.whelk",
        )

def test_publisher_client_client_options_from_dict():
    with mock.patch('google.pubsub_v1.services.publisher.transports.PublisherGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = PublisherClient(
            client_options={'api_endpoint': 'squid.clam.whelk'}
        )
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )


def test_create_topic(transport: str = 'grpc'):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.Topic()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_topic),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic(
            name='name_value',
            kms_key_name='kms_key_name_value',
        )

        response = client.create_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Topic)
    assert response.name == 'name_value'
    assert response.kms_key_name == 'kms_key_name_value'


def test_create_topic_flattened():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_topic),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_topic(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'


def test_create_topic_flattened_error():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_topic(
            pubsub.Topic(),
            name='name_value',
        )


def test_update_topic(transport: str = 'grpc'):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.UpdateTopicRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_topic),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic(
            name='name_value',
            kms_key_name='kms_key_name_value',
        )

        response = client.update_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Topic)
    assert response.name == 'name_value'
    assert response.kms_key_name == 'kms_key_name_value'


def test_publish(transport: str = 'grpc'):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.PublishRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.publish),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.PublishResponse(
            message_ids=['message_ids_value'],
        )

        response = client.publish(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.PublishResponse)
    assert response.message_ids == ['message_ids_value']


def test_publish_flattened():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.publish),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.PublishResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.publish(
            topic='topic_value',
            messages=[pubsub.PubsubMessage(data=b'data_blob')],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].topic == 'topic_value'
        assert args[0].messages == [pubsub.PubsubMessage(data=b'data_blob')]


def test_publish_flattened_error():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.publish(
            pubsub.PublishRequest(),
            topic='topic_value',
            messages=[pubsub.PubsubMessage(data=b'data_blob')],
        )


def test_get_topic(transport: str = 'grpc'):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.GetTopicRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_topic),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic(
            name='name_value',
            kms_key_name='kms_key_name_value',
        )

        response = client.get_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Topic)
    assert response.name == 'name_value'
    assert response.kms_key_name == 'kms_key_name_value'


def test_get_topic_field_headers():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.GetTopicRequest(
        topic='topic/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_topic),
            '__call__') as call:
        call.return_value = pubsub.Topic()
        client.get_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'topic=topic/value',
    ) in kw['metadata']


def test_get_topic_flattened():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_topic),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_topic(
            topic='topic_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].topic == 'topic_value'


def test_get_topic_flattened_error():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_topic(
            pubsub.GetTopicRequest(),
            topic='topic_value',
        )


def test_list_topics(transport: str = 'grpc'):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.ListTopicsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_topics),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicsResponse(
            next_page_token='next_page_token_value',
        )

        response = client.list_topics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTopicsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_topics_field_headers():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListTopicsRequest(
        project='project/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_topics),
            '__call__') as call:
        call.return_value = pubsub.ListTopicsResponse()
        client.list_topics(request)

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


def test_list_topics_flattened():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_topics),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_topics(
            project='project_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project == 'project_value'


def test_list_topics_flattened_error():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_topics(
            pubsub.ListTopicsRequest(),
            project='project_value',
        )


def test_list_topics_pager():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_topics),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicsResponse(
                topics=[
                    pubsub.Topic(),
                    pubsub.Topic(),
                    pubsub.Topic(),
                ],
                next_page_token='abc',
            ),
            pubsub.ListTopicsResponse(
                topics=[],
                next_page_token='def',
            ),
            pubsub.ListTopicsResponse(
                topics=[
                    pubsub.Topic(),
                ],
                next_page_token='ghi',
            ),
            pubsub.ListTopicsResponse(
                topics=[
                    pubsub.Topic(),
                    pubsub.Topic(),
                ],
            ),
            RuntimeError,
        )
        results = [i for i in client.list_topics(
            request={},
        )]
        assert len(results) == 6
        assert all(isinstance(i, pubsub.Topic)
                   for i in results)

def test_list_topics_pages():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_topics),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicsResponse(
                topics=[
                    pubsub.Topic(),
                    pubsub.Topic(),
                    pubsub.Topic(),
                ],
                next_page_token='abc',
            ),
            pubsub.ListTopicsResponse(
                topics=[],
                next_page_token='def',
            ),
            pubsub.ListTopicsResponse(
                topics=[
                    pubsub.Topic(),
                ],
                next_page_token='ghi',
            ),
            pubsub.ListTopicsResponse(
                topics=[
                    pubsub.Topic(),
                    pubsub.Topic(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_topics(request={}).pages)
        for page, token in zip(pages, ['abc','def','ghi', '']):
            assert page.raw_page.next_page_token == token


def test_list_topic_subscriptions(transport: str = 'grpc'):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.ListTopicSubscriptionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_topic_subscriptions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicSubscriptionsResponse(
            subscriptions=['subscriptions_value'],
            next_page_token='next_page_token_value',
        )

        response = client.list_topic_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.ListTopicSubscriptionsResponse)
    assert response.subscriptions == ['subscriptions_value']
    assert response.next_page_token == 'next_page_token_value'


def test_list_topic_subscriptions_field_headers():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListTopicSubscriptionsRequest(
        topic='topic/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_topic_subscriptions),
            '__call__') as call:
        call.return_value = pubsub.ListTopicSubscriptionsResponse()
        client.list_topic_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'topic=topic/value',
    ) in kw['metadata']


def test_list_topic_subscriptions_flattened():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_topic_subscriptions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicSubscriptionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_topic_subscriptions(
            topic='topic_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].topic == 'topic_value'


def test_list_topic_subscriptions_flattened_error():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_topic_subscriptions(
            pubsub.ListTopicSubscriptionsRequest(),
            topic='topic_value',
        )


def test_list_topic_snapshots(transport: str = 'grpc'):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.ListTopicSnapshotsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_topic_snapshots),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicSnapshotsResponse(
            snapshots=['snapshots_value'],
            next_page_token='next_page_token_value',
        )

        response = client.list_topic_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.ListTopicSnapshotsResponse)
    assert response.snapshots == ['snapshots_value']
    assert response.next_page_token == 'next_page_token_value'


def test_list_topic_snapshots_field_headers():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListTopicSnapshotsRequest(
        topic='topic/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_topic_snapshots),
            '__call__') as call:
        call.return_value = pubsub.ListTopicSnapshotsResponse()
        client.list_topic_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'topic=topic/value',
    ) in kw['metadata']


def test_list_topic_snapshots_flattened():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_topic_snapshots),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicSnapshotsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_topic_snapshots(
            topic='topic_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].topic == 'topic_value'


def test_list_topic_snapshots_flattened_error():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_topic_snapshots(
            pubsub.ListTopicSnapshotsRequest(),
            topic='topic_value',
        )


def test_delete_topic(transport: str = 'grpc'):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.DeleteTopicRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.delete_topic),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_topic_flattened():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.delete_topic),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.delete_topic(
            topic='topic_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].topic == 'topic_value'


def test_delete_topic_flattened_error():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_topic(
            pubsub.DeleteTopicRequest(),
            topic='topic_value',
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.PublisherGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PublisherClient(
            credentials=credentials.AnonymousCredentials(),
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PublisherGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = PublisherClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client._transport,
        transports.PublisherGrpcTransport,
    )


def test_publisher_base_transport():
    # Instantiate the base transport.
    transport = transports.PublisherTransport(
        credentials=credentials.AnonymousCredentials(),
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'create_topic',
        'update_topic',
        'publish',
        'get_topic',
        'list_topics',
        'list_topic_subscriptions',
        'list_topic_snapshots',
        'delete_topic',
        )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_publisher_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, 'default') as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        PublisherClient()
        adc.assert_called_once_with(scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/pubsub',
        ))


def test_publisher_host_no_port():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='pubsub.googleapis.com'),
        transport='grpc',
    )
    assert client._transport._host == 'pubsub.googleapis.com:443'


def test_publisher_host_with_port():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='pubsub.googleapis.com:8000'),
        transport='grpc',
    )
    assert client._transport._host == 'pubsub.googleapis.com:8000'


def test_publisher_grpc_transport_channel():
    channel = grpc.insecure_channel('http://localhost/')

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.PublisherGrpcTransport(
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
def test_publisher_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.PublisherGrpcTransport(
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
def test_publisher_grpc_transport_channel_mtls_with_adc(
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
        transport = transports.PublisherGrpcTransport(
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


def test_topic_path():
    project = "squid"
    topic = "clam"

    expected = "projects/{project}/topics/{topic}".format(project=project, topic=topic, )
    actual = PublisherClient.topic_path(project, topic)
    assert expected == actual


def test_parse_topic_path():
    expected = {
    "project": "whelk",
    "topic": "octopus",

    }
    path = PublisherClient.topic_path(**expected)

    # Check that the path construction is reversible.
    actual = PublisherClient.parse_topic_path(path)
    assert expected == actual
