from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import yaml
from fastapi.templating import Jinja2Templates as FastAPIJinja2Templates
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from starlette.datastructures import URL
from starlette.routing import Router
from starlette.templating import pass_context

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

if TYPE_CHECKING:
    pass

def filter_yaml(value: Any, sort_keys=True, indent=2) -> str:
    return yaml.dump(value, sort_keys=sort_keys, indent=indent, allow_unicode=True)

class Jinja2Templates(FastAPIJinja2Templates):

    def _create_env(self, *args, **kwargs) -> "jinja2.Environment":
        from mweb import config
        templates_config = config.get("mweb", {}).get("templates", {})
        cache_size = templates_config.get("cache_size", 1000)
        kwargs["cache_size"] = cache_size

        env = super()._create_env(*args, **kwargs)

        @pass_context
        def url(context: dict, name: str, **path_params: Any) -> URL:
            request = context["request"]
            router: Router = request.scope["router"]
            try:
                url_path = router.url_path_for(name, **path_params)
            except AssertionError as e:
                raise ValueError(f"Could not generate url for '{name}' with params {path_params}: {e}") from e
            return url_path

        env_config = templates_config.get("env", {})
        env.globals.update(env_config.get("globals", {}))

        env.globals["url"] = url

        env.filters["json"] = env.filters["tojson"]
        env.filters["yaml"] = filter_yaml

        return env

    def TemplateResponse(self, name, *args, **kwargs):
        with tracer.start_as_current_span(f"template.render", kind=SpanKind.INTERNAL) as span:  # type: trace.Span
            span.set_attribute("template.name", name)
            return super().TemplateResponse(name, *args, **kwargs)
