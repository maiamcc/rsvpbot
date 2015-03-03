#!/usr/bin/env python

import os
import zulip

HELP_MSG = """Hi, I'm RSVP Bot! I don't do anything yet. Sorry."""

# initializing a Zulip client
# if running from my machine, in terminal, `source environ` to set environmental var
client = zulip.Client(email=os.environ['RSVPBOT_USERNAME'],
                      api_key=os.environ['RSVPBOT_API_KEY'])

all_events = []

def respond(msg):
    if msg["type"] == "private":
        private_msg_respond(msg)
    elif msg["sender_email"] != "punbot-bot@students.hackerschool.com" and \
        "@**rsvp bot**" in msg["content"]:
        # and msg["stream"] in [event.stream for event in all_events]:
            stream_msg_respond(msg)

def private_msg_respond(msg):
    print"you sent me a private message"

def stream_msg_respond(msg):
    print "you sent a message to a stream"

def print_message(msg):
    for k, v in msg.iteritems():
        print k, "-->", v

# This is a blocking call that will run forever
client.call_on_each_message(respond)

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