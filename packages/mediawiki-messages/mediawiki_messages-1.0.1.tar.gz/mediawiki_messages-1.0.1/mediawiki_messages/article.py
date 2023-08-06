# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import typing

from .base import SCHEMA_URL, MediawikiMessage


class ArticleEditV1(MediawikiMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by Mediawiki when a new thing is created.
    """

    topic: typing.ClassVar[str] = "wiki.article.edit"

    body_schema: typing.ClassVar[dict] = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new thing is created",
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "summary": {"type": "string"},
            "minor_edit": {"type": "boolean"},
            "user": {"type": "string"},
            "url": {"type": "string", "format": "uri"},
            "diff_url": {"type": "string", "format": "uri"},
            "page_url": {"type": "string", "format": "uri"},
            "revision": {"type": "object"},
        },
        "required": ["title", "summary", "minor_edit", "user", "diff_url", "page_url"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return (
            "Wiki page {title} was edited by {user}\nSummary: {summary}\n"
            "Page: {page_url}\nDiff: {diff_url}\n"
        ).format(**self.body)

    @property
    def summary(self):
        """Return a summary of the message."""
        return "Wiki page {title} was edited by {user}".format(**self.body)

    @property
    def url(self):
        return self.body["diff_url"]
