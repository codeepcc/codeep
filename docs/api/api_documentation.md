# Codeep AI - REST API Documentation

## Overview

Codeep AI provides a secure REST API for task execution in isolated MicroVM environments. The API supports user authentication, task management, quota tracking, and result retrieval.

### Base URL
```
https://api.codeep.cc/v1
```

### Authentication
All API requests (except registration and login) require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Response Format
All responses are in JSON format with the following structure:
```json
{
  "data": {},
  "message": "Success message",
  "error": null
}
```

### Error Responses
```json
{
  "msg": "Error message",
  "error": "Detailed error description"
}
```

## Authentication Endpoints

### Register User
Create a new user account.

**POST** `/auth/register`

**Request Body:**
```json
{
  "username": "string (required)",
  "email": "string (required)",
  "password": "string (required)"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "api_key": "string",
    "daily_limit": "integer",
    "created_at": "string (ISO 8601)"
  }
}
```

**Error Responses:**
- `400`: Missing required fields
- `409`: Username or email already exists
- `500`: Registration failed

### Login User
Authenticate and receive JWT token.

**POST** `/auth/login`

**Request Body:**
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Response (200):**
```json
{
  "access_token": "string",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "api_key": "string",
    "daily_limit": "integer",
    "created_at": "string (ISO 8601)"
  }
}
```

**Error Responses:**
- `400`: Missing username or password
- `401`: Invalid credentials
- `500`: Login failed

### Get Current User
Retrieve information about the authenticated user.

**GET** `/auth/me`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "api_key": "string",
    "daily_limit": "integer",
    "created_at": "string (ISO 8601)"
  }
}
```

**Error Responses:**
- `401`: Invalid token
- `404`: User not found
- `500`: Retrieval failed

## Quota Management

### Get User Quota
Retrieve current quota usage information.

**GET** `/auth/quota`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "daily_limit": 100,
  "used_today": 5,
  "remaining": 95
}
```

### Validate Quota
Check if user has remaining quota for today.

**GET** `/auth/quota/validate`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "valid": true,
  "daily_limit": 100,
  "used_today": 5,
  "remaining": 95
}
```

**Error Response (429):**
```json
{
  "valid": false,
  "msg": "Daily quota exceeded",
  "daily_limit": 100,
  "used_today": 100
}
```

## Task Management

### Create Task
Submit a new task for execution.

**POST** `/tasks/tasks`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "prompt": "string (required) - The task description/instruction",
  "toolset": ["array of strings - optional tools to enable"]
}
```

**Response (201):**
```json
{
  "message": "Task created successfully",
  "task": {
    "task_id": "string",
    "user_id": "integer",
    "prompt": "string",
    "toolset": ["array"],
    "status": "queued",
    "created_at": "string (ISO 8601)",
    "updated_at": "string (ISO 8601)"
  }
}
```

**Error Responses:**
- `400`: Missing prompt
- `401`: Invalid token
- `404`: User not found
- `500`: Task creation failed

### Get User Tasks
Retrieve all tasks for the authenticated user.

**GET** `/tasks/tasks`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "tasks": [
    {
      "task_id": "string",
      "user_id": "integer",
      "prompt": "string",
      "toolset": ["array"],
      "status": "completed|processing|queued|failed",
      "result": "string or null",
      "error_message": "string or null",
      "created_at": "string (ISO 8601)",
      "updated_at": "string (ISO 8601)",
      "started_at": "string (ISO 8601) or null",
      "completed_at": "string (ISO 8601) or null"
    }
  ]
}
```

### Get Specific Task
Retrieve details of a specific task.

**GET** `/tasks/tasks/{task_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "task": {
    "task_id": "string",
    "user_id": "integer",
    "prompt": "string",
    "toolset": ["array"],
    "status": "completed|processing|queued|failed",
    "result": "string or null",
    "error_message": "string or null",
    "created_at": "string (ISO 8601)",
    "updated_at": "string (ISO 8601)",
    "started_at": "string (ISO 8601) or null",
    "completed_at": "string (ISO 8601) or null"
  }
}
```

**Error Responses:**
- `401`: Invalid token
- `404`: Task not found

### Update Task
Update task status or information (typically used by the system).

**PUT** `/tasks/tasks/{task_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "status": "string (optional)",
  "result": "string (optional)",
  "error_message": "string (optional)",
  "started_at": "string (ISO 8601) (optional)",
  "completed_at": "string (ISO 8601) (optional)"
}
```

**Response (200):**
```json
{
  "message": "Task updated successfully",
  "task": { ... }
}
```

### Delete Task
Remove a task from the system.

**DELETE** `/tasks/tasks/{task_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "message": "Task deleted successfully"
}
```

## Queue Management

### Get Task Results
Retrieve detailed results and download URLs for a completed task.

**GET** `/tasks/tasks/{task_id}/results`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "task_id": "string",
  "status": "completed",
  "result": "parsed JSON result or string",
  "result_urls": {
    "output.json": "https://...",
    "error.log": "https://...",
    "screenshot.png": "https://...",
    "result.txt": "https://..."
  },
  "completed_at": "2023-12-01T10:30:00Z"
}
```

**Error Response (202):**
```json
{
  "task_id": "string",
  "status": "processing",
  "message": "Task is not completed yet"
}
```

### Get Queue Status
Retrieve current queue statistics.

**GET** `/tasks/queue/status`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "queue_lengths": {
    "normal": 5,
    "premium": 2
  },
  "consumer_stats": {
    "active_consumers": 3,
    "processing_tasks": 2
  },
  "total_queued": 7
}
```

## Dashboard & Analytics

### Get Dashboard Statistics
Retrieve comprehensive user dashboard statistics including quota usage, task statistics, and recent activity.

**GET** `/dashboard/stats`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "user_info": {
    "username": "string",
    "email": "string",
    "daily_limit": 100,
    "api_key": "abcd1234..."
  },
  "quota_info": {
    "used_today": 5,
    "remaining_today": 95,
    "daily_limit": 100
  },
  "task_stats": {
    "total": 50,
    "completed": 45,
    "failed": 2,
    "processing": 1,
    "queued": 2,
    "success_rate": 90.0
  },
  "cost_estimate": {
    "today": 0.05,
    "monthly": 0.45,
    "currency": "USD"
  },
  "recent_tasks": [
    {
      "task_id": "string",
      "prompt": "Analyze dataset...",
      "status": "completed",
      "created_at": "2023-12-01T10:00:00Z",
      "completed_at": "2023-12-01T10:05:00Z"
    }
  ]
}
```

### Get Task History
Retrieve paginated task history with filtering options.

**GET** `/dashboard/tasks/history`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20, max: 100)
- `status`: Filter by status (queued, processing, completed, failed)
- `from`: Filter from date (ISO 8601)
- `to`: Filter to date (ISO 8601)

**Response (200):**
```json
{
  "tasks": [...], // Array of task objects
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8
  }
}
```

### Get Usage Analytics
Retrieve detailed usage analytics and trends over time.

**GET** `/dashboard/usage`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `days`: Number of days to analyze (default: 30, max: 365)

**Response (200):**
```json
{
  "period": {
    "start_date": "2023-11-01",
    "end_date": "2023-12-01",
    "days": 30
  },
  "summary": {
    "total_tasks": 45,
    "completed_tasks": 42,
    "failed_tasks": 3,
    "success_rate": 93.33
  },
  "daily_breakdown": [
    {
      "date": "2023-12-01",
      "total": 5,
      "completed": 5,
      "failed": 0
    }
  ],
  "quota_usage": [
    {
      "date": "2023-12-01",
      "requests": 5,
      "limit": 100
    }
  ]
}
```

## Health Check

### System Health
Check if the API is operational.

**GET** `/health`

**Response (200):**
```json
{
  "status": "healthy",
  "service": "Codeep AI API"
}
```

## Rate Limiting

- Authentication endpoints: 10 requests per minute per IP
- Task creation: Limited by daily user quota
- All other endpoints: 100 requests per minute per user

## Error Codes

- `400`: Bad Request - Invalid input parameters
- `401`: Unauthorized - Invalid or missing authentication
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource doesn't exist
- `409`: Conflict - Resource already exists
- `429`: Too Many Requests - Rate limit exceeded
- `500`: Internal Server Error - Unexpected server error

## SDK Examples

### Python
```python
import requests

# Login
response = requests.post('https://api.codeep.cc/v1/auth/login', json={
    'username': 'your_username',
    'password': 'your_password'
})
token = response.json()['access_token']

# Create task
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('https://api.codeep.cc/v1/tasks/tasks',
                        headers=headers,
                        json={
                            'prompt': 'Analyze this dataset and create a visualization',
                            'toolset': ['code_executor', 'file_reader']
                        })
task = response.json()['task']

# Check task status
task_id = task['task_id']
response = requests.get(f'https://api.codeep.cc/v1/tasks/tasks/{task_id}',
                       headers=headers)
status = response.json()['task']['status']
```

### JavaScript/Node.js
```javascript
const axios = require('axios');

// Login
const loginResponse = await axios.post('https://api.codeep.cc/v1/auth/login', {
    username: 'your_username',
    password: 'your_password'
});
const token = loginResponse.data.access_token;

// Create task
const taskResponse = await axios.post('https://api.codeep.cc/v1/tasks/tasks', {
    prompt: 'Generate a report from this data',
    toolset: ['code_executor', 'browser_screenshot']
}, {
    headers: { Authorization: `Bearer ${token}` }
});

const taskId = taskResponse.data.task.task_id;

// Poll for completion
const checkStatus = async () => {
    const statusResponse = await axios.get(`https://api.codeep.cc/v1/tasks/tasks/${taskId}`, {
        headers: { Authorization: `Bearer ${token}` }
    });
    return statusResponse.data.task;
};
```

## Changelog

### v1.0.0
- Initial API release
- User authentication and registration
- Task creation and management
- Quota system
- Queue status monitoring
- Health check endpoint