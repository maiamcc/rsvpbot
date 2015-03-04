#!/usr/bin/env python

import os
import re
import zulip

class SendMsgError(Exception): pass

HELP_MSG = """Hi, I'm RSVP Bot! I don't do anything yet. Sorry."""

# initializing a Zulip client
# if running from my machine, in terminal, `source environ` to set environmental var
client = zulip.Client(email=os.environ['RSVPBOT_USERNAME'],
                      api_key=os.environ['RSVPBOT_API_KEY'])

global all_events
all_events = []

class Event(object):
    def __init__(self, shortname, hosts=[], stream="Social", subject=None,
            description=None, attending=[], posted=False):
        self.shortname = shortname
        self.hosts = hosts
        self.stream = stream
        self.subject = subject
        self.description = description
        self.attending = attending
        self.posted = posted
        # TODO: recurring?
        # should all this stuff even be passed in by the constructor?

def process_incoming_message(msg):
    if msg["sender_email"] != "rsvp-bot@students.hackerschool.com":
        if msg["type"] == "private":
            respond_private_msg(msg)
        elif "@**rsvp bot**" in msg["content"]:
            # and msg["stream"] in [event.stream for event in all_events]:
            respond_stream_msg(msg)

def respond_private_msg(msg):
    content = msg["content"].lower()
    user = msg["sender_email"]
    number = re.search("^\d*", content).group()
    their_events = [event for event in all_events if user in event.hosts]
    # TODO: ^make this a function?
    if content == "help":
        send_response_msg(msg, HELP_MSG)
    elif number:
        # event-specific commands
        i = int(number)
        response_text = "You're trying to access event %d: %s" % (i, their_events[i].shortname)
        send_response_msg(msg, response_text)
    else:
        # general commands
        if content == "list":
            if their_events:
                response_text = ["Okay, here are all of your events:"]
                for i, event in enumerate(their_events):
                    response_text.append("%d. %s" % (i, event.shortname))
                send_response_msg(msg, "\n".join(response_text))
            else:
                response_text = "Sorry, you have no events at this time. Make one with `new [shortname]`!"
                send_response_msg(msg, response_text)
        if content.startswith("new"):
            shortname = re.search('(?<=new ).*', content).group()
            new_event = Event(shortname, hosts=[user])
            all_events.append(new_event)
            their_events = [event for event in all_events if user in event.hosts]
            event_index = their_events.index(new_event)
            response_text = "You've created your event, `%s`, at index %d." % (shortname, event_index)
            send_response_msg(msg, response_text)

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
Anatomy of an event:
    - host(s) = those with admin privileges for the event (list of user emails)
    - shortname = identifier for an event. Guests can use this for RSVPs via PM, and
        it will appear on the hosts's admin panel.
    - stream (defaults to Social) and subject = thread in which discussion
        will take place--RSVP Bot will watch this topic for RSVPs
    - description = any relevant information about the event (what, when,
        where, etc.); RSVP Bot will post this in the thread when soliciting RSVPs.
    - attending list = just what it says on the tin
    - posted = boolean saying whether or not RSVP Bot has (publicly) posted this event
        to its stream

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
    review details of an event
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