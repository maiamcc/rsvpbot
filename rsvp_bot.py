#!/usr/bin/env python


import os
import zulip

class SendMsgError(Exception): pass

HELP_MSG = """Hi, I'm RSVP Bot! I don't do anything yet. Sorry."""

# initializing a Zulip client
# if running from my machine, in terminal, `source environ` to set environmental var
client = zulip.Client(email=os.environ['RSVPBOT_USERNAME'],
                      api_key=os.environ['RSVPBOT_API_KEY'])

all_events = []

class Event(object):
    def __init__(self, hosts=[], subject=None, shortname=None, attending=[],
            description=None, posted=False):
        self.hosts = hosts
        self.subject = subject
        self.shortname = shortname
        self.attending = attending
        self.description = description
        self.posted = posted

def process_incoming_message(msg):
    if msg["sender_email"] != "rsvp-bot@students.hackerschool.com":
        if msg["type"] == "private":
            respond_private_msg(msg)
        elif "@**rsvp bot**" in msg["content"]:
            # and msg["stream"] in [event.stream for event in all_events]:
            respond_stream_msg(msg)

def respond_private_msg(msg):
    # if lower(msg["content"]) == "help":
    content = msg["content"]
    send_response_msg(msg, "you sent me: %s" % content)
    send_new_msg("private", "and here's a new message!", recipient="maia.mcc@gmail.com")

def respond_stream_msg(msg):
    content = msg["content"]
    send_response_msg(msg, "you sent me: %s" % content)
    send_new_msg("stream", "and here's a new message!", stream="bot-test", subject="stuffz")

def send_response_msg(incoming_msg, outgoing_text):
    if incoming_msg["type"] == "private":
        client.send_message({
            "type": "private",
            "to": incoming_msg["sender_email"],
            "content": outgoing_text
        })
    elif incoming_msg["type"] == "stream":
        client.send_message({
            "type": "stream",
            "subject": incoming_msg["subject"],
            "to": incoming_msg['display_recipient'],
            "content": outgoing_text
        })

def send_new_msg(msgtype, outgoing_text, recipient=None, stream=None, subject=None):
    """Sends a Zulip message (NOT in response to a previous message). Specify type as 'private'
        or 'stream'. If private, 'recipient' will be a single user email, 'stream' and 'subject'
        will be None. If public, set 'stream' and 'subject', 'recipient' will be None."""
    if msgtype == "private":
        client.send_message({
            "type": "private",
            "to": recipient,
            "content": outgoing_text
        })
    elif msgtype == "stream":
        client.send_message({
            "type": "stream",
            "to": stream,
            "subject": subject,
            "content": outgoing_text
        })
    else:
        raise SendMsgError("Unrecognized message type")

def print_message(msg):
    for k, v in msg.iteritems():
        print k, "-->", v

# This is a blocking call that will run forever
client.call_on_each_message(process_incoming_message)

"""
An event has:
    a host(s) - list of usernames
    an associated topic (zulip subject)
    a shortname - used to rsvp to this event (do i want to restrict to
        no spaces?)
    attending list
    description
    posted - bool saying whether this event has been posted to
        zulip (on a public stream)

general host actions:
    list (show all events that I'm a host of)
    new (make a new event)

Host actions for a particular event
    add host
    post (post the event to stream) (a generic message)
    remind (to stream) (custom message?)
    PM all guests
    PM all y/m
    list all attending
    close event
    personalized invite (sent to users(s) via PM -- "reply to this message with the text 'xyz __' to rsvp")
    edit subject/description/shortname

When you rsvp:
    y/n/m
    guests
    bringing
    notes

(in thread: @rsvp_bot xy)
(in pm: {shortname} xy)

@rsvp_bot help (in pm or thread)
"""

"""recipient_id --> 35576
sender_email --> maia.mcc@gmail.com
timestamp --> 1425417148
display_recipient --> bot-test
sender_id --> 6175
sender_full_name --> Maia McCormick (S'14)
sender_domain --> students.hackerschool.com
content --> :laughing:
gravatar_hash --> 068432e2e1839c64c05323d419c78762
avatar_url --> https://humbug-user-avatars.s3.amazonaws.com/47ec406248244f0cf1171700f2be783279ac6e13?x=x
client --> website
content_type --> text/x-markdown
subject_links --> []
sender_short_name --> maia.mcc
type --> stream
id --> 35994610
subject --> stuffz"""