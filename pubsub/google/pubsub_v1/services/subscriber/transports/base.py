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

import abc
import typing

from google import auth
from google.auth import credentials  # type: ignore

from google.protobuf import empty_pb2 as empty  # type: ignore
from google.pubsub_v1.types import pubsub


class SubscriberTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for Subscriber."""

    AUTH_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/pubsub',
    )

    def __init__(
            self, *,
            host: str = 'pubsub.googleapis.com',
            credentials: credentials.Credentials = None,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ':' not in host:
            host += ':443'
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials is None:
            credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

    @property
    def create_subscription(self) -> typing.Callable[
            [pubsub.Subscription],
            pubsub.Subscription]:
        raise NotImplementedError

    @property
    def get_subscription(self) -> typing.Callable[
            [pubsub.GetSubscriptionRequest],
            pubsub.Subscription]:
        raise NotImplementedError

    @property
    def update_subscription(self) -> typing.Callable[
            [pubsub.UpdateSubscriptionRequest],
            pubsub.Subscription]:
        raise NotImplementedError

    @property
    def list_subscriptions(self) -> typing.Callable[
            [pubsub.ListSubscriptionsRequest],
            pubsub.ListSubscriptionsResponse]:
        raise NotImplementedError

    @property
    def delete_subscription(self) -> typing.Callable[
            [pubsub.DeleteSubscriptionRequest],
            empty.Empty]:
        raise NotImplementedError

    @property
    def modify_ack_deadline(self) -> typing.Callable[
            [pubsub.ModifyAckDeadlineRequest],
            empty.Empty]:
        raise NotImplementedError

    @property
    def acknowledge(self) -> typing.Callable[
            [pubsub.AcknowledgeRequest],
            empty.Empty]:
        raise NotImplementedError

    @property
    def pull(self) -> typing.Callable[
            [pubsub.PullRequest],
            pubsub.PullResponse]:
        raise NotImplementedError

    @property
    def streaming_pull(self) -> typing.Callable[
            [pubsub.StreamingPullRequest],
            pubsub.StreamingPullResponse]:
        raise NotImplementedError

    @property
    def modify_push_config(self) -> typing.Callable[
            [pubsub.ModifyPushConfigRequest],
            empty.Empty]:
        raise NotImplementedError

    @property
    def get_snapshot(self) -> typing.Callable[
            [pubsub.GetSnapshotRequest],
            pubsub.Snapshot]:
        raise NotImplementedError

    @property
    def list_snapshots(self) -> typing.Callable[
            [pubsub.ListSnapshotsRequest],
            pubsub.ListSnapshotsResponse]:
        raise NotImplementedError

    @property
    def create_snapshot(self) -> typing.Callable[
            [pubsub.CreateSnapshotRequest],
            pubsub.Snapshot]:
        raise NotImplementedError

    @property
    def update_snapshot(self) -> typing.Callable[
            [pubsub.UpdateSnapshotRequest],
            pubsub.Snapshot]:
        raise NotImplementedError

    @property
    def delete_snapshot(self) -> typing.Callable[
            [pubsub.DeleteSnapshotRequest],
            empty.Empty]:
        raise NotImplementedError

    @property
    def seek(self) -> typing.Callable[
            [pubsub.SeekRequest],
            pubsub.SeekResponse]:
        raise NotImplementedError


__all__ = (
    'SubscriberTransport',
)
