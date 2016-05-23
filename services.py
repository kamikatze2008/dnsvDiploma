from protorpc.wsgi import service

import register_agent

# Map the RPC service and path (/PostService)
app = service.service_mappings([('/LifeGame', register_agent.LifeGame)])
