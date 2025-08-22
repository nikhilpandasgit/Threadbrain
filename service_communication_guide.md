# Complete Service Communication Guide

## 1. FRONTEND TO BACKEND COMMUNICATION

### A. From React Router v7 Client

#### Method 1: Using Environment Variables (Recommended)
```typescript
// In your React component or service file
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

// Fetch users
const fetchUsers = async () => {
  try {
    const response = await fetch(`${API_URL}/users`);
    const users = await response.json();
    return users;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};

// POST request example
const createUser = async (userData: any) => {
  try {
    const response = await fetch(`${API_URL}/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    return await response.json();
  } catch (error) {
    console.error('Error creating user:', error);
    throw error;
  }
};
```

#### Method 2: Create an API Service Class
```typescript
// services/api.ts
class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001';
  }

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async delete<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}

export const apiService = new ApiService();

// Usage in components:
// const users = await apiService.get<User[]>('/users');
// const newUser = await apiService.post<User>('/users', userData);
```

#### Method 3: Using React Router v7 Server Functions (Advanced)
```typescript
// app/routes/users.tsx
import type { LoaderFunctionArgs } from "react-router";

// Server-side data loading
export async function loader({ request }: LoaderFunctionArgs) {
  // This runs on the server, so use the internal Docker network
  const response = await fetch('http://server:8000/users');
  const users = await response.json();
  return { users };
}

// Client-side component
export default function Users() {
  const { users } = useLoaderData<typeof loader>();
  
  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

### B. React Component Examples

#### Using useState and useEffect
```typescript
// components/UserList.tsx
import { useState, useEffect } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
}

export function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
        const response = await fetch(`${API_URL}/users`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch users');
        }
        
        const userData = await response.json();
        setUsers(userData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Users</h2>
      {users.map(user => (
        <div key={user.id} className="user-card">
          <h3>{user.name}</h3>
          <p>{user.email}</p>
        </div>
      ))}
    </div>
  );
}
```

#### Using Custom Hook
```typescript
// hooks/useApi.ts
import { useState, useEffect } from 'react';

export function useApi<T>(endpoint: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
        const response = await fetch(`${API_URL}${endpoint}`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [endpoint]);

  return { data, loading, error };
}

// Usage:
// const { data: users, loading, error } = useApi<User[]>('/users');
```

## 2. BACKEND COMMUNICATION PATTERNS

### A. Enhanced FastAPI Backend
```python
# server/app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional

app = FastAPI(
    title="ThreadBrain API",
    version="1.0.0",
    description="Backend API for ThreadBrain application"
)

# CORS setup
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

# In-memory storage (replace with database)
users_db = [
    {"id": 1, "name": "Nik", "email": "nik@example.com"},
    {"id": 2, "name": "Kev", "email": "kev@example.com"}
]

# Routes
@app.get("/")
def root():
    return {"message": "FastAPI backend is running 🚀", "status": "healthy"}

@app.get("/users", response_model=List[User])
def get_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User)
def create_user(user: UserCreate):
    new_id = max([u["id"] for u in users_db]) + 1 if users_db else 1
    new_user = {"id": new_id, **user.dict()}
    users_db.append(new_user)
    return new_user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    user_idx = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if user_idx is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields
    update_data = user_update.dict(exclude_unset=True)
    users_db[user_idx].update(update_data)
    return users_db[user_idx]

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user_idx = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if user_idx is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_user = users_db.pop(user_idx)
    return {"message": f"User {deleted_user['name']} deleted successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": os.getenv("ENVIRONMENT", "unknown")}
```

## 3. NETWORK COMMUNICATION TYPES

### A. External Communication (Browser to Docker)
```
Browser -> http://localhost:5173 -> Client Container
Browser -> http://localhost:8001 -> Server Container
```

### B. Internal Communication (Container to Container)
```
Client Container -> http://server:8000 -> Server Container
```

### C. Communication URLs by Environment

#### Development Environment:
- **Frontend URL**: http://localhost:5173
- **Backend URL**: http://localhost:8001
- **Internal Backend**: http://server:8000 (from client container)

#### Production Environment:
- **Frontend URL**: http://localhost:80
- **Backend URL**: http://localhost:8000
- **Internal Backend**: http://server:8000 (from client container)

## 4. WEBSOCKET COMMUNICATION (Real-time)

### A. FastAPI WebSocket Setup
```python
# Add to server/app/main.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### B. React WebSocket Client
```typescript
// hooks/useWebSocket.ts
import { useState, useEffect, useRef } from 'react';

export function useWebSocket(url: string) {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [lastMessage, setLastMessage] = useState<string | null>(null);
  const [readyState, setReadyState] = useState<number>(WebSocket.CONNECTING);

  useEffect(() => {
    const ws = new WebSocket(url);
    
    ws.onopen = () => setReadyState(WebSocket.OPEN);
    ws.onclose = () => setReadyState(WebSocket.CLOSED);
    ws.onerror = () => setReadyState(WebSocket.CLOSED);
    ws.onmessage = (event) => setLastMessage(event.data);

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, [url]);

  const sendMessage = (message: string) => {
    if (socket && readyState === WebSocket.OPEN) {
      socket.send(message);
    }
  };

  return { lastMessage, sendMessage, readyState };
}

// Usage in component:
// const { lastMessage, sendMessage } = useWebSocket('ws://localhost:8001/ws');
```

## 5. ERROR HANDLING & RETRY LOGIC

```typescript
// utils/apiClient.ts
class ApiClient {
  private baseUrl: string;
  private retryCount: number;

  constructor(baseUrl: string, retryCount = 3) {
    this.baseUrl = baseUrl;
    this.retryCount = retryCount;
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {},
    attempt = 1
  ): Promise<T> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      if (attempt < this.retryCount) {
        console.warn(`Request failed, retrying... (${attempt}/${this.retryCount})`);
        await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
        return this.request<T>(endpoint, options, attempt + 1);
      }
      throw error;
    }
  }
}

export const apiClient = new ApiClient(
  import.meta.env.VITE_API_URL || 'http://localhost:8001'
);
```

## 6. AUTHENTICATION & AUTHORIZATION

### A. JWT Token Management
```typescript
// utils/auth.ts
class AuthService {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
    localStorage.setItem('authToken', token);
  }

  getToken(): string | null {
    if (!this.token) {
      this.token = localStorage.getItem('authToken');
    }
    return this.token;
  }

  removeToken() {
    this.token = null;
    localStorage.removeItem('authToken');
  }

  async authenticatedRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = this.getToken();
    
    const response = await fetch(`${import.meta.env.VITE_API_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    });

    if (response.status === 401) {
      this.removeToken();
      // Redirect to login or handle unauthorized
      throw new Error('Unauthorized');
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}

export const authService = new AuthService();
```

## 7. ENVIRONMENT CONFIGURATION

### Development (.env.development)
```env
VITE_API_URL=http://localhost:8001
VITE_WS_URL=ws://localhost:8001
VITE_ENVIRONMENT=development
```

### Production (.env.production)
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_ENVIRONMENT=production
```

## 8. TESTING COMMUNICATION

### A. Test Backend Endpoints
```bash
# Test all endpoints
curl http://localhost:8001/health
curl http://localhost:8001/users
curl -X POST http://localhost:8001/users -H "Content-Type: application/json" -d '{"name":"Test","email":"test@example.com"}'
```

### B. Test from Frontend
```typescript
// Quick test in browser console
fetch('http://localhost:8001/users')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

This covers all the major communication patterns between your React Router v7 frontend and FastAPI backend in Docker!