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

from typing import Callable, Dict, Tuple

from google.api_core import grpc_helpers   # type: ignore
from google.auth import credentials        # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore


import grpc  # type: ignore

from google.protobuf import empty_pb2 as empty  # type: ignore
from google.pubsub_v1.types import pubsub

from .base import PublisherTransport


class PublisherGrpcTransport(PublisherTransport):
    """gRPC backend transport for Publisher.

    The service that an application uses to manipulate topics,
    and to send messages to a topic.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """
    def __init__(self, *,
            host: str = 'pubsub.googleapis.com',
            credentials: credentials.Credentials = None,
            channel: grpc.Channel = None,
            api_mtls_endpoint: str = None,
            client_cert_source: Callable[[], Tuple[bytes, bytes]] = None) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.

        Raises:
          google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = api_mtls_endpoint if ":" in api_mtls_endpoint else api_mtls_endpoint + ":443"

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = grpc_helpers.create_channel(
                host,
                credentials=credentials,
                ssl_credentials=ssl_credentials,
                scopes=self.AUTH_SCOPES,
            )

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

    @classmethod
    def create_channel(cls,
                       host: str = 'pubsub.googleapis.com',
                       credentials: credentials.Credentials = None,
                       **kwargs) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            scopes=cls.AUTH_SCOPES,
            **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, '_grpc_channel'):
            self._grpc_channel = self.create_channel(
                self._host,
                credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def create_topic(self) -> Callable[
            [pubsub.Topic],
            pubsub.Topic]:
        r"""Return a callable for the create topic method over gRPC.

        Creates the given topic with the given name. See the resource
        name rules.

        Returns:
            Callable[[~.Topic],
                    ~.Topic]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_topic' not in self._stubs:
            self._stubs['create_topic'] = self.grpc_channel.unary_unary(
                '/google.pubsub.v1.Publisher/CreateTopic',
                request_serializer=pubsub.Topic.serialize,
                response_deserializer=pubsub.Topic.deserialize,
            )
        return self._stubs['create_topic']

    @property
    def update_topic(self) -> Callable[
            [pubsub.UpdateTopicRequest],
            pubsub.Topic]:
        r"""Return a callable for the update topic method over gRPC.

        Updates an existing topic. Note that certain
        properties of a topic are not modifiable.

        Returns:
            Callable[[~.UpdateTopicRequest],
                    ~.Topic]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_topic' not in self._stubs:
            self._stubs['update_topic'] = self.grpc_channel.unary_unary(
                '/google.pubsub.v1.Publisher/UpdateTopic',
                request_serializer=pubsub.UpdateTopicRequest.serialize,
                response_deserializer=pubsub.Topic.deserialize,
            )
        return self._stubs['update_topic']

    @property
    def publish(self) -> Callable[
            [pubsub.PublishRequest],
            pubsub.PublishResponse]:
        r"""Return a callable for the publish method over gRPC.

        Adds one or more messages to the topic. Returns ``NOT_FOUND`` if
        the topic does not exist.

        Returns:
            Callable[[~.PublishRequest],
                    ~.PublishResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'publish' not in self._stubs:
            self._stubs['publish'] = self.grpc_channel.unary_unary(
                '/google.pubsub.v1.Publisher/Publish',
                request_serializer=pubsub.PublishRequest.serialize,
                response_deserializer=pubsub.PublishResponse.deserialize,
            )
        return self._stubs['publish']

    @property
    def get_topic(self) -> Callable[
            [pubsub.GetTopicRequest],
            pubsub.Topic]:
        r"""Return a callable for the get topic method over gRPC.

        Gets the configuration of a topic.

        Returns:
            Callable[[~.GetTopicRequest],
                    ~.Topic]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_topic' not in self._stubs:
            self._stubs['get_topic'] = self.grpc_channel.unary_unary(
                '/google.pubsub.v1.Publisher/GetTopic',
                request_serializer=pubsub.GetTopicRequest.serialize,
                response_deserializer=pubsub.Topic.deserialize,
            )
        return self._stubs['get_topic']

    @property
    def list_topics(self) -> Callable[
            [pubsub.ListTopicsRequest],
            pubsub.ListTopicsResponse]:
        r"""Return a callable for the list topics method over gRPC.

        Lists matching topics.

        Returns:
            Callable[[~.ListTopicsRequest],
                    ~.ListTopicsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_topics' not in self._stubs:
            self._stubs['list_topics'] = self.grpc_channel.unary_unary(
                '/google.pubsub.v1.Publisher/ListTopics',
                request_serializer=pubsub.ListTopicsRequest.serialize,
                response_deserializer=pubsub.ListTopicsResponse.deserialize,
            )
        return self._stubs['list_topics']

    @property
    def list_topic_subscriptions(self) -> Callable[
            [pubsub.ListTopicSubscriptionsRequest],
            pubsub.ListTopicSubscriptionsResponse]:
        r"""Return a callable for the list topic subscriptions method over gRPC.

        Lists the names of the subscriptions on this topic.

        Returns:
            Callable[[~.ListTopicSubscriptionsRequest],
                    ~.ListTopicSubscriptionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_topic_subscriptions' not in self._stubs:
            self._stubs['list_topic_subscriptions'] = self.grpc_channel.unary_unary(
                '/google.pubsub.v1.Publisher/ListTopicSubscriptions',
                request_serializer=pubsub.ListTopicSubscriptionsRequest.serialize,
                response_deserializer=pubsub.ListTopicSubscriptionsResponse.deserialize,
            )
        return self._stubs['list_topic_subscriptions']

    @property
    def list_topic_snapshots(self) -> Callable[
            [pubsub.ListTopicSnapshotsRequest],
            pubsub.ListTopicSnapshotsResponse]:
        r"""Return a callable for the list topic snapshots method over gRPC.

        Lists the names of the snapshots on this topic.
        Snapshots are used in <a
        href="https://cloud.google.com/pubsub/docs/replay-
        overview">Seek</a> operations, which allow
        you to manage message acknowledgments in bulk. That is,
        you can set the acknowledgment state of messages in an
        existing subscription to the state captured by a
        snapshot.

        Returns:
            Callable[[~.ListTopicSnapshotsRequest],
                    ~.ListTopicSnapshotsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_topic_snapshots' not in self._stubs:
            self._stubs['list_topic_snapshots'] = self.grpc_channel.unary_unary(
                '/google.pubsub.v1.Publisher/ListTopicSnapshots',
                request_serializer=pubsub.ListTopicSnapshotsRequest.serialize,
                response_deserializer=pubsub.ListTopicSnapshotsResponse.deserialize,
            )
        return self._stubs['list_topic_snapshots']

    @property
    def delete_topic(self) -> Callable[
            [pubsub.DeleteTopicRequest],
            empty.Empty]:
        r"""Return a callable for the delete topic method over gRPC.

        Deletes the topic with the given name. Returns ``NOT_FOUND`` if
        the topic does not exist. After a topic is deleted, a new topic
        may be created with the same name; this is an entirely new topic
        with none of the old configuration or subscriptions. Existing
        subscriptions to this topic are not deleted, but their ``topic``
        field is set to ``_deleted-topic_``.

        Returns:
            Callable[[~.DeleteTopicRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_topic' not in self._stubs:
            self._stubs['delete_topic'] = self.grpc_channel.unary_unary(
                '/google.pubsub.v1.Publisher/DeleteTopic',
                request_serializer=pubsub.DeleteTopicRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs['delete_topic']


__all__ = (
    'PublisherGrpcTransport',
)
