set dotenv-load

default:
  just --list

[working-directory: 'wids-agent-api']
build-api:
  @cp ../uv.lock .
  @cp -r ../wids-ai-agents .
  -docker build -t wids-agent-api .
  @rm uv.lock
  @rm -r wids-ai-agents

run-api:
  fastapi dev wids-agent-api/app/main.py --port 8000 --reload

run-docker-compose:
  cp ./uv.lock ./wids-agent-api/
  cp -r ./wids-ai-agents ./wids-agent-api/
  -docker compose up -d
  rm wids-agent-api/uv.lock
  rm -r wids-agent-api/wids-ai-agents
