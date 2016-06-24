import traceback
from django.core.urlresolvers import resolve
from django.http import HttpResponsePermanentRedirect, HttpResponse, Http404
from django.conf import settings
from re import sub
import urllib
import urllib2
import json


class ExceptionNotifier(object):
    def process_exception(self, request, exception):
        if not settings.DEBUG:
            if isinstance(exception, Http404):
                return
            exc = u'Error at {}:\n\n'.format(request.path)
            error_lines = traceback.format_exc().split('\n')
            # error_lines = error_lines[:3] + error_lines[3:5] * 100 + error_lines[5:]

            frames_skipped = 0
            while len('\n'.join(error_lines)) > 4000 or len(error_lines) > 22:
                error_lines = error_lines[:3] + error_lines[5:]
                frames_skipped += 1

            if frames_skipped > 0:
                error_lines = error_lines[:3] + ['  ' + '=' * 11, '  ({} frames skipped)'.format(frames_skipped), '  ' + '=' * 11] + error_lines[3:]

            exc += '```' + '\n'.join(error_lines) + '```'

            exc += '\nContext info:\n'

            ctx = ''
            ctx += 'User: {} (id={})\n'.format(str(request.user), str(getattr(request.user, 'id', None)))

            exc += '```' + ctx + '```'

            # Notifier.notify(exc, parse_mode='Markdown', tags='web error')
            request = urllib2.urlopen(
                settings.SLACK_NOTIFIER_URL,
                data=urllib.urlencode(dict(
                    payload=json.dumps(dict(
                        text=exc
                    ))
                ))
            )
            request.read()
