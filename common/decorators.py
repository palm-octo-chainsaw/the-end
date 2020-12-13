from django.http import HttpResponseBadRequest


def ajax_required(f):

    def wrap(req, *args, **kwargs):

        if not req.is_ajax():

            return HttpResponseBadRequest()

        return f(req, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap
