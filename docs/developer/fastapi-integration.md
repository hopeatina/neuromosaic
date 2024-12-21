---
title: "FastAPI Integration"
description: "Learn how to work with and extend the FastAPI backend"
---

# FastAPI Integration

This guide explains how to work with NeuroMosaic's FastAPI backend, including adding new endpoints and integrating with the frontend.

## API Structure

The backend is organized into:

1. Core API routes
2. WebSocket connections
3. Background tasks
4. Data models

## Core Routes

### Basic Route Structure

```python
from fastapi import APIRouter, Depends, HTTPException
from neuromosaic.models import ExperimentConfig, Architecture
from typing import List, Dict, Any

router = APIRouter(prefix="/api/v1")

@router.post("/experiments")
async def create_experiment(
    config: ExperimentConfig,
    background_tasks: BackgroundTasks
) -> Dict[str, str]:
    """Create and start a new experiment"""
    try:
        experiment_id = await experiments.create(config)
        background_tasks.add_task(
            run_experiment,
            experiment_id,
            config
        )
        return {"id": experiment_id}
    except ValueError as e:
        raise HTTPException(400, str(e))
```

### Data Models

```python
from pydantic import BaseModel, Field

class ArchitectureConfig(BaseModel):
    name: str
    parameters: Dict[str, Any]
    constraints: List[str] = Field(default_factory=list)

class ExperimentConfig(BaseModel):
    name: str
    architecture_type: str
    search_config: Dict[str, Any]
    max_trials: int = 100
    objectives: List[str]
```

## WebSocket Integration

### Real-time Updates

```python
from fastapi import WebSocket
from neuromosaic.messaging import MessageQueue

@router.websocket("/ws/experiments/{experiment_id}")
async def experiment_websocket(
    websocket: WebSocket,
    experiment_id: str
):
    await websocket.accept()
    queue = MessageQueue()

    try:
        # Subscribe to updates
        await queue.subscribe(f"experiment.{experiment_id}")

        while True:
            # Send updates to client
            message = await queue.get()
            await websocket.send_json(message)

    except WebSocketDisconnect:
        await queue.unsubscribe(f"experiment.{experiment_id}")
```

### Message Broadcasting

```python
from neuromosaic.events import EventEmitter

class ExperimentUpdater:
    def __init__(self):
        self.emitter = EventEmitter()

    async def broadcast_update(
        self,
        experiment_id: str,
        data: Dict[str, Any]
    ):
        """Broadcast update to all subscribers"""
        await self.emitter.emit(
            f"experiment.{experiment_id}",
            data
        )
```

## Background Tasks

### Task Management

```python
from neuromosaic.tasks import TaskManager

class ExperimentTaskManager:
    def __init__(self):
        self.task_manager = TaskManager()

    async def run_experiment(
        self,
        experiment_id: str,
        config: ExperimentConfig
    ):
        """Run experiment in background"""
        task = self.task_manager.create_task(
            name=f"experiment_{experiment_id}",
            func=self._run_experiment,
            args=(experiment_id, config)
        )
        await task.start()

    async def _run_experiment(
        self,
        experiment_id: str,
        config: ExperimentConfig
    ):
        """Actual experiment execution"""
        try:
            search = ArchitectureSearch(config)
            async for result in search.run_async():
                await self.broadcast_update(
                    experiment_id,
                    result
                )
        except Exception as e:
            await self.broadcast_error(
                experiment_id,
                str(e)
            )
```

## Database Integration

### Models and Schemas

```python
from sqlalchemy import Column, String, JSON
from neuromosaic.database import Base

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String, primary_key=True)
    name = Column(String)
    config = Column(JSON)
    status = Column(String)
    results = Column(JSON)
```

### CRUD Operations

```python
from neuromosaic.database import AsyncSession
from sqlalchemy.future import select

class ExperimentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        experiment: ExperimentConfig
    ) -> str:
        """Create new experiment record"""
        db_experiment = Experiment(
            id=generate_id(),
            name=experiment.name,
            config=experiment.dict(),
            status="pending"
        )
        self.session.add(db_experiment)
        await self.session.commit()
        return db_experiment.id

    async def get(self, experiment_id: str) -> Experiment:
        """Get experiment by ID"""
        query = select(Experiment).where(
            Experiment.id == experiment_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
```

## Frontend Integration

### API Client

```python
from neuromosaic.client import ApiClient

class NeuroMosaicClient:
    def __init__(self, base_url: str):
        self.client = ApiClient(base_url)

    async def create_experiment(
        self,
        config: Dict[str, Any]
    ) -> str:
        """Create new experiment"""
        response = await self.client.post(
            "/api/v1/experiments",
            json=config
        )
        return response["id"]

    async def connect_websocket(
        self,
        experiment_id: str,
        callback: Callable
    ):
        """Connect to experiment updates"""
        await self.client.websocket_connect(
            f"/ws/experiments/{experiment_id}",
            callback
        )
```

## Authentication & Security

### JWT Authentication

```python
from fastapi.security import OAuth2PasswordBearer
from neuromosaic.auth import create_token, verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> Dict[str, Any]:
    """Verify JWT token and return user"""
    try:
        return await verify_token(token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication"
        )

@router.post("/experiments")
async def create_experiment(
    config: ExperimentConfig,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Create experiment (authenticated)"""
    config.user_id = user["id"]
    # ... rest of implementation
```

## Testing

### API Tests

```python
from fastapi.testclient import TestClient
from neuromosaic.main import app

client = TestClient(app)

def test_create_experiment():
    response = client.post(
        "/api/v1/experiments",
        json={
            "name": "test",
            "architecture_type": "resnet",
            "max_trials": 10
        }
    )
    assert response.status_code == 200
    assert "id" in response.json()
```

### WebSocket Tests

```python
import pytest
from fastapi.websockets import WebSocket

async def test_experiment_websocket():
    async with client.websocket_connect(
        "/ws/experiments/test"
    ) as websocket:
        data = await websocket.receive_json()
        assert "type" in data
        assert "payload" in data
```

## Best Practices

1. **API Design**

   - Use consistent naming
   - Version endpoints
   - Document responses

2. **Performance**

   - Implement caching
   - Use async operations
   - Optimize queries

3. **Error Handling**
   - Detailed error messages
   - Proper status codes
   - Validation feedback

## Troubleshooting

<Accordion title="Connection Issues">
- Check WebSocket status
- Verify endpoints
- Monitor connections
</Accordion>

<Accordion title="Performance Problems">
- Profile endpoints
- Check database queries
- Monitor memory usage
</Accordion>

## Next Steps

- Learn about [architecture types](/developer/adding-architectures)
- Explore [LLM integration](/developer/llm-providers)
- Study [visualization](/guides/visualize-results)
