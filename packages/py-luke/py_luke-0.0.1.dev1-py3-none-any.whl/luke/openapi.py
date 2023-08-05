from typing import List, Dict, Any, Tuple, Optional
import yaml


class OpenAPISpec:
    def __init__(self):
        self.endpoints: List[Endpoint] = []
        self.spec = dict()

    @property
    def info(self) -> dict:
        return self.spec.get("info", {})

    def load_from_file(self, file):
        spec_data = yaml.load(file, yaml.Loader)
        self.spec = spec_data

        for path, endpoints in spec_data["paths"].items():
            for method, endpoint_spec in endpoints.items():
                try:
                    endpoint = Endpoint(path, method, self)
                    endpoint.load_spec(endpoint_spec)
                    self.endpoints.append(endpoint)
                except (ValueError, KeyError):
                    pass

    def resolve_spec(self, spec: dict) -> dict:
        resolved = spec
        ref = spec.get("$ref")
        if ref:
            resolved = self.resolve_ref(ref)
        
        if resolved["type"] == "object":
            if "properties" in resolved:
                for key in resolved["properties"]:
                    resolved["properties"][key] = self.resolve_spec(resolved["properties"][key])
            else:
                resolved["additionalProperties"] = self.resolve_spec(resolved["additionalProperties"])

        elif resolved["type"] == "array":
            resolved["items"] = self.resolve_spec(resolved["items"])

        return resolved

    def resolve_ref(self, ref: str):
        if not ref.startswith("#/"):
            raise ValueError("Reference is invalid")

        node = self.spec
        for node_name in ref[2:].split("/"):
            if node_name not in node:
                raise ValueError("Reference not found")

            node = node[node_name]

        return node


class Endpoint:
    def __init__(
        self,
        path: str,
        method: str,
        openapi: "OpenAPISpec",
    ):
        self.path = path
        self.method = method
        self.content_specs: Dict[Tuple[str, str], Any] = dict()
        self.headers_spec = {
            "type": "object",
            "properties": dict(),
        }
        self.spec: dict = None  # type: ignore
        self.openapi = openapi

    def load_spec(self, spec: dict):
        self.spec = spec

        content_specs = self.content_specs
        for code, contents in spec["responses"].items():
            if "content" not in contents:
                content_specs[(code, "application/json")] = {
                    "type": "string"
                }
                continue

            for content_type, content in contents["content"].items():
                try:
                    content_specs[(code, content_type)] = self.openapi.resolve_spec(content["schema"])
                except KeyError:
                    pass

        headers_spec = self.headers_spec
        if "headers" in spec:
            for header_name, header_spec in spec["headers"].items():
                try:
                    headers_spec["properties"][header_name] = self.openapi.resolve_spec(header_spec["schema"]) # type: ignore
                except KeyError:
                    continue

    def get_content_spec(self, code: str, content_type: str) -> Optional[dict]:
        return self.content_specs.get((code, content_type))

    def get_headers_spec(self) -> dict:
        return self.headers_spec


