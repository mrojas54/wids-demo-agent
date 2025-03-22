from app.routes.chat import router as chat_router
from app.routes.ping import router as ping_router
from app.routes.summaries import router as summaries_router

all_routes = [chat_router, ping_router, summaries_router]
__all__ = ["chat_router", "ping_router", "summaries_router"]
