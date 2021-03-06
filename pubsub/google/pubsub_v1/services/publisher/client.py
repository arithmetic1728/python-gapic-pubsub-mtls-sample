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

from collections import OrderedDict
import re
from typing import Callable, Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions # type: ignore
from google.api_core import exceptions                 # type: ignore
from google.api_core import gapic_v1                   # type: ignore
from google.api_core import retry as retries           # type: ignore
from google.auth import credentials                    # type: ignore
from google.oauth2 import service_account              # type: ignore

from google.pubsub_v1.services.publisher import pagers
from google.pubsub_v1.types import pubsub

from .transports.base import PublisherTransport
from .transports.grpc import PublisherGrpcTransport


class PublisherClientMeta(type):
    """Metaclass for the Publisher client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """
    _transport_registry = OrderedDict()  # type: Dict[str, Type[PublisherTransport]]
    _transport_registry['grpc'] = PublisherGrpcTransport

    def get_transport_class(cls,
            label: str = None,
            ) -> Type[PublisherTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class PublisherClient(metaclass=PublisherClientMeta):
    """The service that an application uses to manipulate topics,
    and to send messages to a topic.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = 'pubsub.googleapis.com'
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @staticmethod
    def topic_path(project: str,topic: str,) -> str:
        """Return a fully-qualified topic string."""
        return "projects/{project}/topics/{topic}".format(project=project, topic=topic, )

    @staticmethod
    def parse_topic_path(path: str) -> Dict[str,str]:
        """Parse a topic path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/topics/(?P<topic>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(self, *,
            credentials: credentials.Credentials = None,
            transport: Union[str, PublisherTransport] = None,
            client_options: ClientOptions = None,
            ) -> None:
        """Instantiate the publisher client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.PublisherTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client.
                (2) If ``transport`` argument is None, ``client_options`` can be
                used to create a mutual TLS transport. If ``client_cert_source``
                is provided, mutual TLS transport will be created with the given
                ``api_endpoint`` or the default mTLS endpoint, and the client
                SSL credentials obtained from ``client_cert_source``.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, PublisherTransport):
            # transport is a PublisherTransport instance.
            if credentials:
                raise ValueError('When providing a transport instance, '
                                 'provide its credentials directly.')
            self._transport = transport
        elif client_options is None or (
            client_options.api_endpoint == None
            and client_options.client_cert_source is None
        ):
            # Don't trigger mTLS if we get an empty ClientOptions.
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials, host=self.DEFAULT_ENDPOINT
            )
        else:
            # We have a non-empty ClientOptions. If client_cert_source is
            # provided, trigger mTLS with user provided endpoint or the default
            # mTLS endpoint.
            if client_options.client_cert_source:
                api_mtls_endpoint = (
                    client_options.api_endpoint
                    if client_options.api_endpoint
                    else self.DEFAULT_MTLS_ENDPOINT
                )
            else:
                api_mtls_endpoint = None

            api_endpoint = (
                client_options.api_endpoint
                if client_options.api_endpoint
                else self.DEFAULT_ENDPOINT
            )

            self._transport = PublisherGrpcTransport(
                credentials=credentials,
                host=api_endpoint,
                api_mtls_endpoint=api_mtls_endpoint,
                client_cert_source=client_options.client_cert_source,
            )

    def create_topic(self,
            request: pubsub.Topic = None,
            *,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.Topic:
        r"""Creates the given topic with the given name. See the resource
        name rules.

        Args:
            request (:class:`~.pubsub.Topic`):
                The request object. A topic resource.
            name (:class:`str`):
                Required. The name of the topic. It must have the format
                ``"projects/{project}/topics/{topic}"``. ``{topic}``
                must start with a letter, and contain only letters
                (``[A-Za-z]``), numbers (``[0-9]``), dashes (``-``),
                underscores (``_``), periods (``.``), tildes (``~``),
                plus (``+``) or percent signs (``%``). It must be
                between 3 and 255 characters in length, and it must not
                start with ``"goog"``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.Topic:
                A topic resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.Topic(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_topic,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_topic(self,
            request: pubsub.UpdateTopicRequest = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.Topic:
        r"""Updates an existing topic. Note that certain
        properties of a topic are not modifiable.

        Args:
            request (:class:`~.pubsub.UpdateTopicRequest`):
                The request object. Request for the UpdateTopic method.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.Topic:
                A topic resource.
        """
        # Create or coerce a protobuf request object.

        request = pubsub.UpdateTopicRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_topic,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def publish(self,
            request: pubsub.PublishRequest = None,
            *,
            topic: str = None,
            messages: Sequence[pubsub.PubsubMessage] = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.PublishResponse:
        r"""Adds one or more messages to the topic. Returns ``NOT_FOUND`` if
        the topic does not exist.

        Args:
            request (:class:`~.pubsub.PublishRequest`):
                The request object. Request for the Publish method.
            topic (:class:`str`):
                Required. The messages in the request will be published
                on this topic. Format is
                ``projects/{project}/topics/{topic}``.
                This corresponds to the ``topic`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            messages (:class:`Sequence[~.pubsub.PubsubMessage]`):
                Required. The messages to publish.
                This corresponds to the ``messages`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.PublishResponse:
                Response for the ``Publish`` method.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([topic, messages]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.PublishRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if topic is not None:
            request.topic = topic
        if messages is not None:
            request.messages = messages

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.publish,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_topic(self,
            request: pubsub.GetTopicRequest = None,
            *,
            topic: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.Topic:
        r"""Gets the configuration of a topic.

        Args:
            request (:class:`~.pubsub.GetTopicRequest`):
                The request object. Request for the GetTopic method.
            topic (:class:`str`):
                Required. The name of the topic to get. Format is
                ``projects/{project}/topics/{topic}``.
                This corresponds to the ``topic`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.Topic:
                A topic resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([topic]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.GetTopicRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if topic is not None:
            request.topic = topic

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_topic,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('topic', request.topic),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_topics(self,
            request: pubsub.ListTopicsRequest = None,
            *,
            project: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListTopicsPager:
        r"""Lists matching topics.

        Args:
            request (:class:`~.pubsub.ListTopicsRequest`):
                The request object. Request for the `ListTopics` method.
            project (:class:`str`):
                Required. The name of the project in which to list
                topics. Format is ``projects/{project-id}``.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListTopicsPager:
                Response for the ``ListTopics`` method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.ListTopicsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project is not None:
            request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_topics,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('project', request.project),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTopicsPager(
            method=rpc,
            request=request,
            response=response,
        )

        # Done; return the response.
        return response

    def list_topic_subscriptions(self,
            request: pubsub.ListTopicSubscriptionsRequest = None,
            *,
            topic: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.ListTopicSubscriptionsResponse:
        r"""Lists the names of the subscriptions on this topic.

        Args:
            request (:class:`~.pubsub.ListTopicSubscriptionsRequest`):
                The request object. Request for the
                `ListTopicSubscriptions` method.
            topic (:class:`str`):
                Required. The name of the topic that subscriptions are
                attached to. Format is
                ``projects/{project}/topics/{topic}``.
                This corresponds to the ``topic`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.ListTopicSubscriptionsResponse:
                Response for the ``ListTopicSubscriptions`` method.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([topic]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.ListTopicSubscriptionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if topic is not None:
            request.topic = topic

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_topic_subscriptions,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('topic', request.topic),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_topic_snapshots(self,
            request: pubsub.ListTopicSnapshotsRequest = None,
            *,
            topic: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.ListTopicSnapshotsResponse:
        r"""Lists the names of the snapshots on this topic.
        Snapshots are used in <a
        href="https://cloud.google.com/pubsub/docs/replay-
        overview">Seek</a> operations, which allow
        you to manage message acknowledgments in bulk. That is,
        you can set the acknowledgment state of messages in an
        existing subscription to the state captured by a
        snapshot.

        Args:
            request (:class:`~.pubsub.ListTopicSnapshotsRequest`):
                The request object. Request for the `ListTopicSnapshots`
                method.
            topic (:class:`str`):
                Required. The name of the topic that snapshots are
                attached to. Format is
                ``projects/{project}/topics/{topic}``.
                This corresponds to the ``topic`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.ListTopicSnapshotsResponse:
                Response for the ``ListTopicSnapshots`` method.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([topic]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.ListTopicSnapshotsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if topic is not None:
            request.topic = topic

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_topic_snapshots,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('topic', request.topic),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_topic(self,
            request: pubsub.DeleteTopicRequest = None,
            *,
            topic: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Deletes the topic with the given name. Returns ``NOT_FOUND`` if
        the topic does not exist. After a topic is deleted, a new topic
        may be created with the same name; this is an entirely new topic
        with none of the old configuration or subscriptions. Existing
        subscriptions to this topic are not deleted, but their ``topic``
        field is set to ``_deleted-topic_``.

        Args:
            request (:class:`~.pubsub.DeleteTopicRequest`):
                The request object. Request for the `DeleteTopic`
                method.
            topic (:class:`str`):
                Required. Name of the topic to delete. Format is
                ``projects/{project}/topics/{topic}``.
                This corresponds to the ``topic`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([topic]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.DeleteTopicRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if topic is not None:
            request.topic = topic

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_topic,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )





try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            'google-pubsub',
        ).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = (
    'PublisherClient',
)
