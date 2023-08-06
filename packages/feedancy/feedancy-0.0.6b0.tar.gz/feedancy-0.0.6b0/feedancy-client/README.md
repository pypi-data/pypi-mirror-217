# feedancy-client

The client is provided with async and sync adapters.

To install the async version with all its dependencies use:
```bash
pip install feedancy-client[asyncio]
```

To install the sync version with all its dependencies use:
```bash
pip install feedancy-client[sync]
```

To install both versions with all their dependencies use:
```bash
pip install feedancy-client[asyncio,sync]
```

## Client instantiation example

```python

from feedancy_client import new_client, Configuration
from feedancy_client.lib.adapter.requests import RequestsAdapter

client = new_client(RequestsAdapter(), Configuration(host="<your openapi server URL>"))
```