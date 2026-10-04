"""Minimal read-only MCP server over stdio; no SDK, network or SQL execution.

Messages are newline-delimited JSON-RPC 2.0 (MCP stdio transport).
The catalog is synthetic and tool inputs never become paths or commands.
"""
import json
import sys
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / 'catalog/dependencies.json'
PROTOCOLS = ('2025-11-25', '2025-06-18', '2024-11-05')
TOOLS = [
    {'name': 'list_objects', 'description': 'List synthetic database objects.',
     'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    {'name': 'describe_object', 'description': 'Read schema, dependencies and provenance for one known object.',
     'inputSchema': {'type': 'object', 'properties': {'name': {'type': 'string'}},
                     'required': ['name'], 'additionalProperties': False}},
]
for tool in TOOLS:
    tool['annotations'] = {'readOnlyHint': True, 'destructiveHint': False,
                           'idempotentHint': True, 'openWorldHint': False}


def result(value):
    return {'content': [{'type': 'text', 'text': json.dumps(value, ensure_ascii=False)}]}


def handle(message):
    if not isinstance(message, dict) or message.get('jsonrpc') != '2.0' or not isinstance(message.get('method'), str):
        return {'jsonrpc': '2.0', 'id': message.get('id') if isinstance(message, dict) else None,
                'error': {'code': -32600, 'message': 'Invalid Request'}}
    if 'id' not in message:
        return None
    method = message['method']
    params = message.get('params', {})
    envelope = {'jsonrpc': '2.0', 'id': message['id']}
    if not isinstance(params, dict):
        return {**envelope, 'error': {'code': -32602, 'message': 'Params must be an object'}}
    if method == 'initialize':
        requested = params.get('protocolVersion')
        value = {'protocolVersion': requested if requested in PROTOCOLS else '2025-06-18',
                 'capabilities': {'tools': {'listChanged': False}},
                 'serverInfo': {'name': 'faro-catalog', 'version': '1.0.0'},
                 'instructions': 'Synthetic metadata only. Compare catalog claims with code and business rules.'}
    elif method == 'ping':
        value = {}
    elif method == 'tools/list':
        value = {'tools': TOOLS}
    elif method == 'tools/call':
        arguments = params.get('arguments', {})
        if not isinstance(arguments, dict):
            return {**envelope, 'error': {'code': -32602, 'message': 'Arguments must be an object'}}
        catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
        if params.get('name') == 'list_objects' and not arguments:
            value = result({'objects': list(catalog['objects']), 'source': catalog['source']})
        elif params.get('name') == 'describe_object' and set(arguments) == {'name'}:
            obj = arguments['name']
            if isinstance(obj, str) and obj in catalog['objects']:
                value = result(catalog['objects'][obj])
            else:
                value = {**result({'error': 'Unknown object'}), 'isError': True}
        else:
            value = {**result({'error': 'Unknown tool or invalid arguments'}), 'isError': True}
    else:
        return {**envelope, 'error': {'code': -32601, 'message': 'Method not found'}}
    return {**envelope, 'result': value}


def main():
    for line in sys.stdin:
        try:
            response = handle(json.loads(line))
        except json.JSONDecodeError:
            response = {'jsonrpc': '2.0', 'id': None,
                        'error': {'code': -32700, 'message': 'Parse error'}}
        except Exception:
            # Keep stdout valid JSON-RPC and do not leak local paths.
            response = {'jsonrpc': '2.0', 'id': None,
                        'error': {'code': -32603, 'message': 'Internal error'}}
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
