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

from typing import Any, Callable, Iterable

from google.pubsub_v1.types import pubsub


class ListSubscriptionsPager:
    """A pager for iterating through ``list_subscriptions`` requests.

    This class thinly wraps an initial
    :class:`~.pubsub.ListSubscriptionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``subscriptions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSubscriptions`` requests and continue to iterate
    through the ``subscriptions`` field on the
    corresponding responses.

    All the usual :class:`~.pubsub.ListSubscriptionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[[pubsub.ListSubscriptionsRequest],
                pubsub.ListSubscriptionsResponse],
            request: pubsub.ListSubscriptionsRequest,
            response: pubsub.ListSubscriptionsResponse):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.pubsub.ListSubscriptionsRequest`):
                The initial request object.
            response (:class:`~.pubsub.ListSubscriptionsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = pubsub.ListSubscriptionsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[pubsub.ListSubscriptionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[pubsub.Subscription]:
        for page in self.pages:
            yield from page.subscriptions

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListSnapshotsPager:
    """A pager for iterating through ``list_snapshots`` requests.

    This class thinly wraps an initial
    :class:`~.pubsub.ListSnapshotsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``snapshots`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSnapshots`` requests and continue to iterate
    through the ``snapshots`` field on the
    corresponding responses.

    All the usual :class:`~.pubsub.ListSnapshotsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[[pubsub.ListSnapshotsRequest],
                pubsub.ListSnapshotsResponse],
            request: pubsub.ListSnapshotsRequest,
            response: pubsub.ListSnapshotsResponse):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.pubsub.ListSnapshotsRequest`):
                The initial request object.
            response (:class:`~.pubsub.ListSnapshotsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = pubsub.ListSnapshotsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[pubsub.ListSnapshotsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[pubsub.Snapshot]:
        for page in self.pages:
            yield from page.snapshots

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)
