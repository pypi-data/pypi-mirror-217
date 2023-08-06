#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
# -------------------------------------------------------------------------------


"""
This module contains error handling code for *Hawat* application.
"""

__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"

from werkzeug.http import HTTP_STATUS_CODES
from flask import request, make_response, render_template, jsonify
from flask_babel import gettext
from flask_login import current_user

import hawat.const


def wants_json_response():
    """Helper method for detecting preferred response in JSON format."""
    return request.accept_mimetypes['application/json'] >= \
           request.accept_mimetypes['text/html']


def error_handler_switch(status_code, exc):
    """Return correct error response (HTML or JSON) based on client preferences."""
    if wants_json_response():
        return api_error_response(status_code, exception=exc)
    return error_response(status_code, exception=exc)


def _get_error_message(status_code):
    """Get error message for custom errors which are not defined in werkzeug."""
    if status_code == 499:
        return gettext('Client Closed Request')
    return HTTP_STATUS_CODES.get(status_code, gettext('Unknown error'))


def _make_payload(status_code, message=None, exception=None):
    """Prepare the error response payload regardless of the response type."""
    payload = {
        'status': status_code,
        'error': _get_error_message(status_code)
    }
    if message:
        payload['message'] = message
    if exception:
        # Flask built-in exceptions classes come with default description strings.
        # Use these as default for empty message.
        if hasattr(exception.__class__, 'description'):
            payload['message'] = exception.__class__.description
        # Append the whole exception object for developers to make debugging easier.
        if current_user.is_authenticated and current_user.has_role(hawat.const.ROLE_DEVELOPER):
            payload['exception'] = exception
    return payload


def error_response(status_code, message=None, exception=None):
    """Generate error response in HTML format."""
    status_code = int(status_code)
    payload = _make_payload(status_code, message, exception)
    return make_response(
        render_template(
            'http_error.html',
            **payload
        ),
        status_code
    )


def api_error_response(status_code, message=None, exception=None):
    """Generate error response in JSON format."""
    status_code = int(status_code)
    payload = _make_payload(status_code, message, exception)
    response = jsonify(payload)
    response.status_code = status_code
    return response
