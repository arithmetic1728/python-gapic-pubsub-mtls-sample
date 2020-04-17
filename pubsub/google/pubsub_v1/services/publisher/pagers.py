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


class ListTopicsPager:
    """A pager for iterating through ``list_topics`` requests.

    This class thinly wraps an initial
    :class:`~.pubsub.ListTopicsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``topics`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTopics`` requests and continue to iterate
    through the ``topics`` field on the
    corresponding responses.

    All the usual :class:`~.pubsub.ListTopicsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[[pubsub.ListTopicsRequest],
                pubsub.ListTopicsResponse],
            request: pubsub.ListTopicsRequest,
            response: pubsub.ListTopicsResponse):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.pubsub.ListTopicsRequest`):
                The initial request object.
            response (:class:`~.pubsub.ListTopicsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = pubsub.ListTopicsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[pubsub.ListTopicsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[pubsub.Topic]:
        for page in self.pages:
            yield from page.topics

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)
