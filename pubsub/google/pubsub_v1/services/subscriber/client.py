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
from typing import Callable, Dict, Iterable, Iterator, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions # type: ignore
from google.api_core import exceptions                 # type: ignore
from google.api_core import gapic_v1                   # type: ignore
from google.api_core import retry as retries           # type: ignore
from google.auth import credentials                    # type: ignore
from google.oauth2 import service_account              # type: ignore

from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.pubsub_v1.services.subscriber import pagers
from google.pubsub_v1.types import pubsub

from .transports.base import SubscriberTransport
from .transports.grpc import SubscriberGrpcTransport


class SubscriberClientMeta(type):
    """Metaclass for the Subscriber client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """
    _transport_registry = OrderedDict()  # type: Dict[str, Type[SubscriberTransport]]
    _transport_registry['grpc'] = SubscriberGrpcTransport

    def get_transport_class(cls,
            label: str = None,
            ) -> Type[SubscriberTransport]:
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


class SubscriberClient(metaclass=SubscriberClientMeta):
    """The service that an application uses to manipulate subscriptions and
    to consume messages from a subscription via the ``Pull`` method or
    by establishing a bi-directional stream using the ``StreamingPull``
    method.
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
    def snapshot_path(project: str,snapshot: str,) -> str:
        """Return a fully-qualified snapshot string."""
        return "projects/{project}/snapshots/{snapshot}".format(project=project, snapshot=snapshot, )

    @staticmethod
    def parse_snapshot_path(path: str) -> Dict[str,str]:
        """Parse a snapshot path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/snapshots/(?P<snapshot>.+?)$", path)
        return m.groupdict() if m else {}
    @staticmethod
    def subscription_path(project: str,subscription: str,) -> str:
        """Return a fully-qualified subscription string."""
        return "projects/{project}/subscriptions/{subscription}".format(project=project, subscription=subscription, )

    @staticmethod
    def parse_subscription_path(path: str) -> Dict[str,str]:
        """Parse a subscription path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/subscriptions/(?P<subscription>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(self, *,
            credentials: credentials.Credentials = None,
            transport: Union[str, SubscriberTransport] = None,
            client_options: ClientOptions = None,
            ) -> None:
        """Instantiate the subscriber client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SubscriberTransport]): The
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
        if isinstance(transport, SubscriberTransport):
            # transport is a SubscriberTransport instance.
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

            self._transport = SubscriberGrpcTransport(
                credentials=credentials,
                host=api_endpoint,
                api_mtls_endpoint=api_mtls_endpoint,
                client_cert_source=client_options.client_cert_source,
            )

    def create_subscription(self,
            request: pubsub.Subscription = None,
            *,
            name: str = None,
            topic: str = None,
            push_config: pubsub.PushConfig = None,
            ack_deadline_seconds: int = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.Subscription:
        r"""Creates a subscription to a given topic. See the resource name
        rules. If the subscription already exists, returns
        ``ALREADY_EXISTS``. If the corresponding topic doesn't exist,
        returns ``NOT_FOUND``.

        If the name is not provided in the request, the server will
        assign a random name for this subscription on the same project
        as the topic, conforming to the `resource name
        format <https://cloud.google.com/pubsub/docs/admin#resource_names>`__.
        The generated name is populated in the returned Subscription
        object. Note that for REST API requests, you must specify a name
        in the request.

        Args:
            request (:class:`~.pubsub.Subscription`):
                The request object. A subscription resource.
            name (:class:`str`):
                Required. The name of the subscription. It must have the
                format
                ``"projects/{project}/subscriptions/{subscription}"``.
                ``{subscription}`` must start with a letter, and contain
                only letters (``[A-Za-z]``), numbers (``[0-9]``), dashes
                (``-``), underscores (``_``), periods (``.``), tildes
                (``~``), plus (``+``) or percent signs (``%``). It must
                be between 3 and 255 characters in length, and it must
                not start with ``"goog"``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            topic (:class:`str`):
                Required. The name of the topic from which this
                subscription is receiving messages. Format is
                ``projects/{project}/topics/{topic}``. The value of this
                field will be ``_deleted-topic_`` if the topic has been
                deleted.
                This corresponds to the ``topic`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            push_config (:class:`~.pubsub.PushConfig`):
                If push delivery is used with this subscription, this
                field is used to configure it. An empty ``pushConfig``
                signifies that the subscriber will pull and ack messages
                using API methods.
                This corresponds to the ``push_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            ack_deadline_seconds (:class:`int`):
                The approximate amount of time (on a best-effort basis)
                Pub/Sub waits for the subscriber to acknowledge receipt
                before resending the message. In the interval after the
                message is delivered and before it is acknowledged, it
                is considered to be outstanding. During that time
                period, the message will not be redelivered (on a
                best-effort basis).

                For pull subscriptions, this value is used as the
                initial value for the ack deadline. To override this
                value for a given message, call ``ModifyAckDeadline``
                with the corresponding ``ack_id`` if using non-streaming
                pull or send the ``ack_id`` in a
                ``StreamingModifyAckDeadlineRequest`` if using streaming
                pull. The minimum custom deadline you can specify is 10
                seconds. The maximum custom deadline you can specify is
                600 seconds (10 minutes). If this parameter is 0, a
                default value of 10 seconds is used.

                For push delivery, this value is also used to set the
                request timeout for the call to the push endpoint.

                If the subscriber never acknowledges the message, the
                Pub/Sub system will eventually redeliver the message.
                This corresponds to the ``ack_deadline_seconds`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.Subscription:
                A subscription resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name, topic, push_config, ack_deadline_seconds]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.Subscription(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name
        if topic is not None:
            request.topic = topic
        if push_config is not None:
            request.push_config = push_config
        if ack_deadline_seconds is not None:
            request.ack_deadline_seconds = ack_deadline_seconds

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_subscription,
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

    def get_subscription(self,
            request: pubsub.GetSubscriptionRequest = None,
            *,
            subscription: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.Subscription:
        r"""Gets the configuration details of a subscription.

        Args:
            request (:class:`~.pubsub.GetSubscriptionRequest`):
                The request object. Request for the GetSubscription
                method.
            subscription (:class:`str`):
                Required. The name of the subscription to get. Format is
                ``projects/{project}/subscriptions/{sub}``.
                This corresponds to the ``subscription`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.Subscription:
                A subscription resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([subscription]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.GetSubscriptionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if subscription is not None:
            request.subscription = subscription

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_subscription,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('subscription', request.subscription),
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

    def update_subscription(self,
            request: pubsub.UpdateSubscriptionRequest = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.Subscription:
        r"""Updates an existing subscription. Note that certain
        properties of a subscription, such as its topic, are not
        modifiable.

        Args:
            request (:class:`~.pubsub.UpdateSubscriptionRequest`):
                The request object. Request for the UpdateSubscription
                method.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.Subscription:
                A subscription resource.
        """
        # Create or coerce a protobuf request object.

        request = pubsub.UpdateSubscriptionRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_subscription,
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

    def list_subscriptions(self,
            request: pubsub.ListSubscriptionsRequest = None,
            *,
            project: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListSubscriptionsPager:
        r"""Lists matching subscriptions.

        Args:
            request (:class:`~.pubsub.ListSubscriptionsRequest`):
                The request object. Request for the `ListSubscriptions`
                method.
            project (:class:`str`):
                Required. The name of the project in which to list
                subscriptions. Format is ``projects/{project-id}``.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListSubscriptionsPager:
                Response for the ``ListSubscriptions`` method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.ListSubscriptionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project is not None:
            request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_subscriptions,
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
        response = pagers.ListSubscriptionsPager(
            method=rpc,
            request=request,
            response=response,
        )

        # Done; return the response.
        return response

    def delete_subscription(self,
            request: pubsub.DeleteSubscriptionRequest = None,
            *,
            subscription: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Deletes an existing subscription. All messages retained in the
        subscription are immediately dropped. Calls to ``Pull`` after
        deletion will return ``NOT_FOUND``. After a subscription is
        deleted, a new one may be created with the same name, but the
        new one has no association with the old subscription or its
        topic unless the same topic is specified.

        Args:
            request (:class:`~.pubsub.DeleteSubscriptionRequest`):
                The request object. Request for the DeleteSubscription
                method.
            subscription (:class:`str`):
                Required. The subscription to delete. Format is
                ``projects/{project}/subscriptions/{sub}``.
                This corresponds to the ``subscription`` field
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
        if request is not None and any([subscription]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.DeleteSubscriptionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if subscription is not None:
            request.subscription = subscription

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_subscription,
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

    def modify_ack_deadline(self,
            request: pubsub.ModifyAckDeadlineRequest = None,
            *,
            subscription: str = None,
            ack_ids: Sequence[str] = None,
            ack_deadline_seconds: int = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Modifies the ack deadline for a specific message. This method is
        useful to indicate that more time is needed to process a message
        by the subscriber, or to make the message available for
        redelivery if the processing was interrupted. Note that this
        does not modify the subscription-level ``ackDeadlineSeconds``
        used for subsequent messages.

        Args:
            request (:class:`~.pubsub.ModifyAckDeadlineRequest`):
                The request object. Request for the ModifyAckDeadline
                method.
            subscription (:class:`str`):
                Required. The name of the subscription. Format is
                ``projects/{project}/subscriptions/{sub}``.
                This corresponds to the ``subscription`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            ack_ids (:class:`Sequence[str]`):
                Required. List of acknowledgment IDs.
                This corresponds to the ``ack_ids`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            ack_deadline_seconds (:class:`int`):
                Required. The new ack deadline with respect to the time
                this request was sent to the Pub/Sub system. For
                example, if the value is 10, the new ack deadline will
                expire 10 seconds after the ``ModifyAckDeadline`` call
                was made. Specifying zero might immediately make the
                message available for delivery to another subscriber
                client. This typically results in an increase in the
                rate of message redeliveries (that is, duplicates). The
                minimum deadline you can specify is 0 seconds. The
                maximum deadline you can specify is 600 seconds (10
                minutes).
                This corresponds to the ``ack_deadline_seconds`` field
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
        if request is not None and any([subscription, ack_ids, ack_deadline_seconds]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.ModifyAckDeadlineRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if subscription is not None:
            request.subscription = subscription
        if ack_ids is not None:
            request.ack_ids = ack_ids
        if ack_deadline_seconds is not None:
            request.ack_deadline_seconds = ack_deadline_seconds

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.modify_ack_deadline,
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

    def acknowledge(self,
            request: pubsub.AcknowledgeRequest = None,
            *,
            subscription: str = None,
            ack_ids: Sequence[str] = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Acknowledges the messages associated with the ``ack_ids`` in the
        ``AcknowledgeRequest``. The Pub/Sub system can remove the
        relevant messages from the subscription.

        Acknowledging a message whose ack deadline has expired may
        succeed, but such a message may be redelivered later.
        Acknowledging a message more than once will not result in an
        error.

        Args:
            request (:class:`~.pubsub.AcknowledgeRequest`):
                The request object. Request for the Acknowledge method.
            subscription (:class:`str`):
                Required. The subscription whose message is being
                acknowledged. Format is
                ``projects/{project}/subscriptions/{sub}``.
                This corresponds to the ``subscription`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            ack_ids (:class:`Sequence[str]`):
                Required. The acknowledgment ID for the messages being
                acknowledged that was returned by the Pub/Sub system in
                the ``Pull`` response. Must not be empty.
                This corresponds to the ``ack_ids`` field
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
        if request is not None and any([subscription, ack_ids]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.AcknowledgeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if subscription is not None:
            request.subscription = subscription
        if ack_ids is not None:
            request.ack_ids = ack_ids

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.acknowledge,
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

    def pull(self,
            request: pubsub.PullRequest = None,
            *,
            subscription: str = None,
            return_immediately: bool = None,
            max_messages: int = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.PullResponse:
        r"""Pulls messages from the server. The server may return
        ``UNAVAILABLE`` if there are too many concurrent pull requests
        pending for the given subscription.

        Args:
            request (:class:`~.pubsub.PullRequest`):
                The request object. Request for the `Pull` method.
            subscription (:class:`str`):
                Required. The subscription from which messages should be
                pulled. Format is
                ``projects/{project}/subscriptions/{sub}``.
                This corresponds to the ``subscription`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            return_immediately (:class:`bool`):
                Optional. If this field set to true, the system will
                respond immediately even if it there are no messages
                available to return in the ``Pull`` response. Otherwise,
                the system may wait (for a bounded amount of time) until
                at least one message is available, rather than returning
                no messages. Warning: setting this field to ``true`` is
                discouraged because it adversely impacts the performance
                of ``Pull`` operations. We recommend that users do not
                set this field.
                This corresponds to the ``return_immediately`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            max_messages (:class:`int`):
                Required. The maximum number of
                messages to return for this request.
                Must be a positive integer. The Pub/Sub
                system may return fewer than the number
                specified.
                This corresponds to the ``max_messages`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.PullResponse:
                Response for the ``Pull`` method.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([subscription, return_immediately, max_messages]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.PullRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if subscription is not None:
            request.subscription = subscription
        if return_immediately is not None:
            request.return_immediately = return_immediately
        if max_messages is not None:
            request.max_messages = max_messages

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.pull,
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

    def streaming_pull(self,
            requests: Iterator[pubsub.StreamingPullRequest] = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> Iterable[pubsub.StreamingPullResponse]:
        r"""Establishes a stream with the server, which sends messages down
        to the client. The client streams acknowledgements and ack
        deadline modifications back to the server. The server will close
        the stream and return the status on any error. The server may
        close the stream with status ``UNAVAILABLE`` to reassign
        server-side resources, in which case, the client should
        re-establish the stream. Flow control can be achieved by
        configuring the underlying RPC channel.

        Args:
            requests (Iterator[`~.pubsub.StreamingPullRequest`]):
                The request object iterator. Request for the `StreamingPull`
                streaming RPC method. This request is used to establish
                the initial stream as well as to stream acknowledgements
                and ack deadline modifications from the client to the
                server.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[~.pubsub.StreamingPullResponse]:
                Response for the ``StreamingPull`` method. This response
                is used to stream messages from the server to the
                client.

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.streaming_pull,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            requests,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def modify_push_config(self,
            request: pubsub.ModifyPushConfigRequest = None,
            *,
            subscription: str = None,
            push_config: pubsub.PushConfig = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Modifies the ``PushConfig`` for a specified subscription.

        This may be used to change a push subscription to a pull one
        (signified by an empty ``PushConfig``) or vice versa, or change
        the endpoint URL and other attributes of a push subscription.
        Messages will accumulate for delivery continuously through the
        call regardless of changes to the ``PushConfig``.

        Args:
            request (:class:`~.pubsub.ModifyPushConfigRequest`):
                The request object. Request for the ModifyPushConfig
                method.
            subscription (:class:`str`):
                Required. The name of the subscription. Format is
                ``projects/{project}/subscriptions/{sub}``.
                This corresponds to the ``subscription`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            push_config (:class:`~.pubsub.PushConfig`):
                Required. The push configuration for future deliveries.

                An empty ``pushConfig`` indicates that the Pub/Sub
                system should stop pushing messages from the given
                subscription and allow messages to be pulled and
                acknowledged - effectively pausing the subscription if
                ``Pull`` or ``StreamingPull`` is not called.
                This corresponds to the ``push_config`` field
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
        if request is not None and any([subscription, push_config]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.ModifyPushConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if subscription is not None:
            request.subscription = subscription
        if push_config is not None:
            request.push_config = push_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.modify_push_config,
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

    def get_snapshot(self,
            request: pubsub.GetSnapshotRequest = None,
            *,
            snapshot: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.Snapshot:
        r"""Gets the configuration details of a snapshot.
        Snapshots are used in <a
        href="https://cloud.google.com/pubsub/docs/replay-
        overview">Seek</a> operations, which allow you to manage
        message acknowledgments in bulk. That is, you can set
        the acknowledgment state of messages in an existing
        subscription to the state captured by a snapshot.

        Args:
            request (:class:`~.pubsub.GetSnapshotRequest`):
                The request object. Request for the GetSnapshot method.
            snapshot (:class:`str`):
                Required. The name of the snapshot to get. Format is
                ``projects/{project}/snapshots/{snap}``.
                This corresponds to the ``snapshot`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.Snapshot:
                A snapshot resource. Snapshots are
                used in <a
                href="https://cloud.google.com/pubsub/docs/replay-
                overview">Seek</a> operations, which
                allow
                you to manage message acknowledgments in
                bulk. That is, you can set the
                acknowledgment state of messages in an
                existing subscription to the state
                captured by a snapshot.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([snapshot]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.GetSnapshotRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if snapshot is not None:
            request.snapshot = snapshot

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_snapshot,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('snapshot', request.snapshot),
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

    def list_snapshots(self,
            request: pubsub.ListSnapshotsRequest = None,
            *,
            project: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListSnapshotsPager:
        r"""Lists the existing snapshots. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-
        overview">Seek</a> operations, which allow
        you to manage message acknowledgments in bulk. That is,
        you can set the acknowledgment state of messages in an
        existing subscription to the state captured by a
        snapshot.

        Args:
            request (:class:`~.pubsub.ListSnapshotsRequest`):
                The request object. Request for the `ListSnapshots`
                method.
            project (:class:`str`):
                Required. The name of the project in which to list
                snapshots. Format is ``projects/{project-id}``.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListSnapshotsPager:
                Response for the ``ListSnapshots`` method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.ListSnapshotsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project is not None:
            request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_snapshots,
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
        response = pagers.ListSnapshotsPager(
            method=rpc,
            request=request,
            response=response,
        )

        # Done; return the response.
        return response

    def create_snapshot(self,
            request: pubsub.CreateSnapshotRequest = None,
            *,
            name: str = None,
            subscription: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.Snapshot:
        r"""Creates a snapshot from the requested subscription. Snapshots
        are used in Seek operations, which allow you to manage message
        acknowledgments in bulk. That is, you can set the acknowledgment
        state of messages in an existing subscription to the state
        captured by a snapshot. If the snapshot already exists, returns
        ``ALREADY_EXISTS``. If the requested subscription doesn't exist,
        returns ``NOT_FOUND``. If the backlog in the subscription is too
        old -- and the resulting snapshot would expire in less than 1
        hour -- then ``FAILED_PRECONDITION`` is returned. See also the
        ``Snapshot.expire_time`` field. If the name is not provided in
        the request, the server will assign a random name for this
        snapshot on the same project as the subscription, conforming to
        the `resource name
        format <https://cloud.google.com/pubsub/docs/admin#resource_names>`__.
        The generated name is populated in the returned Snapshot object.
        Note that for REST API requests, you must specify a name in the
        request.

        Args:
            request (:class:`~.pubsub.CreateSnapshotRequest`):
                The request object. Request for the `CreateSnapshot`
                method.
            name (:class:`str`):
                Required. User-provided name for this snapshot. If the
                name is not provided in the request, the server will
                assign a random name for this snapshot on the same
                project as the subscription. Note that for REST API
                requests, you must specify a name. See the resource name
                rules. Format is
                ``projects/{project}/snapshots/{snap}``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            subscription (:class:`str`):
                Required. The subscription whose backlog the snapshot
                retains. Specifically, the created snapshot is
                guaranteed to retain: (a) The existing backlog on the
                subscription. More precisely, this is defined as the
                messages in the subscription's backlog that are
                unacknowledged upon the successful completion of the
                ``CreateSnapshot`` request; as well as: (b) Any messages
                published to the subscription's topic following the
                successful completion of the CreateSnapshot request.
                Format is ``projects/{project}/subscriptions/{sub}``.
                This corresponds to the ``subscription`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.Snapshot:
                A snapshot resource. Snapshots are
                used in <a
                href="https://cloud.google.com/pubsub/docs/replay-
                overview">Seek</a> operations, which
                allow
                you to manage message acknowledgments in
                bulk. That is, you can set the
                acknowledgment state of messages in an
                existing subscription to the state
                captured by a snapshot.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name, subscription]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.CreateSnapshotRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name
        if subscription is not None:
            request.subscription = subscription

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_snapshot,
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

    def update_snapshot(self,
            request: pubsub.UpdateSnapshotRequest = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.Snapshot:
        r"""Updates an existing snapshot. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-
        overview">Seek</a> operations, which allow
        you to manage message acknowledgments in bulk. That is,
        you can set the acknowledgment state of messages in an
        existing subscription to the state captured by a
        snapshot.

        Args:
            request (:class:`~.pubsub.UpdateSnapshotRequest`):
                The request object. Request for the UpdateSnapshot
                method.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.Snapshot:
                A snapshot resource. Snapshots are
                used in <a
                href="https://cloud.google.com/pubsub/docs/replay-
                overview">Seek</a> operations, which
                allow
                you to manage message acknowledgments in
                bulk. That is, you can set the
                acknowledgment state of messages in an
                existing subscription to the state
                captured by a snapshot.

        """
        # Create or coerce a protobuf request object.

        request = pubsub.UpdateSnapshotRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_snapshot,
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

    def delete_snapshot(self,
            request: pubsub.DeleteSnapshotRequest = None,
            *,
            snapshot: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Removes an existing snapshot. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-
        overview">Seek</a> operations, which allow
        you to manage message acknowledgments in bulk. That is,
        you can set the acknowledgment state of messages in an
        existing subscription to the state captured by a
        snapshot.<br><br>
        When the snapshot is deleted, all messages retained in
        the snapshot are immediately dropped. After a snapshot
        is deleted, a new one may be created with the same name,
        but the new one has no association with the old snapshot
        or its subscription, unless the same subscription is
        specified.

        Args:
            request (:class:`~.pubsub.DeleteSnapshotRequest`):
                The request object. Request for the `DeleteSnapshot`
                method.
            snapshot (:class:`str`):
                Required. The name of the snapshot to delete. Format is
                ``projects/{project}/snapshots/{snap}``.
                This corresponds to the ``snapshot`` field
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
        if request is not None and any([snapshot]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = pubsub.DeleteSnapshotRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if snapshot is not None:
            request.snapshot = snapshot

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_snapshot,
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

    def seek(self,
            request: pubsub.SeekRequest = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pubsub.SeekResponse:
        r"""Seeks an existing subscription to a point in time or
        to a given snapshot, whichever is provided in the
        request. Snapshots are used in <a
        href="https://cloud.google.com/pubsub/docs/replay-
        overview">Seek</a> operations, which allow
        you to manage message acknowledgments in bulk. That is,
        you can set the acknowledgment state of messages in an
        existing subscription to the state captured by a
        snapshot. Note that both the subscription and the
        snapshot must be on the same topic.

        Args:
            request (:class:`~.pubsub.SeekRequest`):
                The request object. Request for the `Seek` method.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pubsub.SeekResponse:
                Response for the ``Seek`` method (this response is
                empty).

        """
        # Create or coerce a protobuf request object.

        request = pubsub.SeekRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.seek,
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





try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            'google-pubsub',
        ).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = (
    'SubscriberClient',
)
