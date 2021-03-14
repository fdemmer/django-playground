import structlog

from django.utils import translation
from django.views.generic import TemplateView


class StructlogMixin:
    logger_name = None

    def __init__(self, *args, **kwargs):
        if not getattr(self, 'log', None):
            name = self.logger_name \
                or f'{self.__class__.__module__}.{self.__class__.__name__}'
            self.log = structlog.get_logger(name).new()
        # noinspection PyArgumentList
        super().__init__(*args, **kwargs)


class StructlogViewMixin(StructlogMixin):
    """
    View mixin to bind a structlog logger to self.log before dispatching.
    """
    structlog_bind_user = False
    structlog_language = True
    structlog_log_dispatch = True

    def dispatch(self, request, *args, **kwargs):
        log_kwargs = {
            'class': self.__class__.__name__,
            'method': request.method,
            'path': request.path,
            'view_name': getattr(request.resolver_match, 'view_name', None),
        }
        if self.structlog_bind_user:
            log_kwargs['username'] = request.user.get_username()
        if self.structlog_language:
            log_kwargs['language'] = translation.get_language()

        self.log = self.log.bind()
        if self.structlog_log_dispatch:
            self.log.info('dispatch', **log_kwargs)

        # noinspection PyUnresolvedReferences
        return super().dispatch(request, *args, **kwargs)


class AboutView(StructlogViewMixin, TemplateView):
    template_name = 'about.html'
