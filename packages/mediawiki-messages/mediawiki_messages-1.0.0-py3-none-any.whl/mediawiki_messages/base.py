# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from fedora_messaging import message

SCHEMA_URL = "http://fedoraproject.org/message-schema/"


class MediawikiMessage(message.Message):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by Mediawiki.
    """

    @property
    def app_name(self):
        return "Mediawiki"

    @property
    def app_icon(self):
        return "https://apps.fedoraproject.org/img/icons/mediawiki.png"

    @property
    def agent_name(self):
        """The username of the user who initiated the action that generated this message."""
        return self.body.get("user")

    @property
    def usernames(self):
        """List of users affected by the action that generated this message."""
        names = [self.agent_name]
        if self.body["title"].startswith("User:"):
            names.append(self.body["title"].split(":", 1)[1].lower())
        return names

    @property
    def groups(self):
        """List of groups affected by the action that generated this message."""
        # TODO: are there wiki pages for groups?
        return []
