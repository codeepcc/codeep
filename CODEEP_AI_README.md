# Codeep AI Python SDK

A Python SDK for the Codeep AI REST API with full LangChain compatibility.

## Features

- **Complete API Coverage**: Supports all Codeep AI API endpoints including health checks
- **LangChain Compatible**: Implements `BaseLLM` for seamless LangChain integration
- **Type Safety**: Full type hints and Pydantic models
- **Comprehensive Error Handling**: Custom exceptions for different error conditions
- **Async Ready**: Built on requests with session management
- **Comprehensive**: Authentication, task management, quota tracking, analytics, and dashboard

## Installation

```bash
pip install codeep  # Includes the codeforge_ai package
```

Or install from source:

```bash
git clone <repository>
cd <repository>
pip install -e .
```

## Configuration

The SDK supports environment-based configuration for different deployment environments.

### Environment Variables

Create a `.env` file in your project root:

```bash
cp .env.example .env
```

Edit the `.env` file:

```env
# Development environment (uses localhost:5001)
CODEEP_ENVIRONMENT=development

# Or production environment (uses https://api.codeep.cc/v1)
CODEEP_ENVIRONMENT=production

# You can also manually set the API URL
CODEEP_API_BASE_URL=https://api.codeep.cc/v1
```

### Programmatic Configuration

```python
from codeforge_ai import Config

# Set environment
Config.set_environment("development")  # Uses localhost:5001
Config.set_environment("production")   # Uses https://api.codeep.cc/v1

# Or set custom URL
Config.set_base_url("https://your-custom-api.com/v1")

# Check current configuration
print(f"Environment: {Config.ENVIRONMENT}")
print(f"API URL: {Config.get_base_url()}")
```

## Quick Start

### Basic Usage

```python
from codeforge_ai import CodeepClient

# Initialize client
client = CodeepClient()

# Login
client.login("your_username", "your_password")

# Create and run a task
task = client.create_task(
    prompt="Analyze this dataset and create a visualization",
    toolset=["code_executor", "file_reader"]
)

# Wait for completion
result = client.wait_for_completion(task.task_id)
print(result.result)
```

### LangChain Integration

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Get LangChain compatible LLM
llm = client.llm

# Create a chain
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write a short summary about {topic}"
)

chain = LLMChain(llm=llm, prompt=prompt)

# Run the chain
result = chain.run(topic="artificial intelligence")
print(result)
```

## API Reference

### CodeepClient

Main client class that provides access to all API functionality.

#### Authentication Methods

```python
# Register new user
client.register("username", "email@example.com", "password")

# Login
client.login("username", "password")

# Set token manually
client.set_token("your_jwt_token")

# Get current user info
user = client.get_current_user()

# Check quota
quota = client.get_quota()
```

#### Task Management

```python
# Create task
task = client.create_task("Your prompt here", toolset=["tool1", "tool2"])

# Get task status
task = client.get_task("task_id")

# Wait for completion
completed_task = client.wait_for_completion("task_id", timeout=600)

# Get all user tasks
tasks = client.get_user_tasks()

# Get detailed results
results = client.get_task_results("task_id")
```

#### Analytics & Dashboard

```python
# Get dashboard stats
stats = client.get_dashboard_stats()

# Get task history
history = client.get_task_history(page=1, per_page=20, status="completed")

# Get usage analytics
analytics = client.get_usage_analytics(days=30)
```

### CodeepLLM

LangChain compatible LLM implementation.

#### Parameters

- `client`: TaskClient instance (required)
- `model_name`: Model identifier (default: "codeep-ai")
- `toolset`: List of tools to enable (optional)
- `timeout`: Task timeout in seconds (default: 300)
- `poll_interval`: Polling interval in seconds (default: 5)

#### Usage

```python
from codeep import CodeepLLM

# Initialize with authenticated client
llm = CodeepLLM(client=task_client)

# Direct call
response = llm("Hello, world!")

# With parameters
response = llm("Complex task", toolset=["code_executor"], timeout=600)
```

## Error Handling

The SDK raises appropriate exceptions for different error conditions:

```python
try:
    result = client.llm("Your prompt")
except RuntimeError as e:
    print(f"Task failed: {e}")
except TimeoutError as e:
    print(f"Task timed out: {e}")
```

## Advanced Usage

### Custom Toolsets

```python
# Specify tools for specific tasks
task = client.create_task(
    prompt="Process this data file",
    toolset=["file_reader", "data_processor", "visualization"]
)
```

### Polling Configuration

```python
# Custom timeout and polling
result = client.wait_for_completion(
    task_id="task_123",
    timeout=1200,  # 20 minutes
    poll_interval=10  # Check every 10 seconds
)
```

### LangChain Chains

```python
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate

# Multiple steps with Codeep AI
step1 = LLMChain(
    llm=client.llm,
    prompt=PromptTemplate.from_template("Step 1: {input}"),
    output_key="step1_output"
)

step2 = LLMChain(
    llm=client.llm,
    prompt=PromptTemplate.from_template("Step 2: {step1_output}"),
    output_key="final_output"
)

chain = SequentialChain(
    chains=[step1, step2],
    input_variables=["input"],
    output_variables=["final_output"]
)

result = chain({"input": "initial prompt"})
```

## Data Models

### User Model

```python
class User:
    id: int
    username: str
    email: str
    api_key: str
    daily_limit: int
    created_at: str
```

### Task Model

```python
class Task:
    task_id: str
    user_id: int
    prompt: str
    toolset: Optional[List[str]]
    status: str  # "queued", "processing", "completed", "failed"
    result: Optional[str]
    error_message: Optional[str]
    created_at: str
    updated_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
```

## Rate Limiting

The SDK respects API rate limits:
- Authentication: 10 requests/minute per IP
- Tasks: Limited by user daily quota
- Other endpoints: 100 requests/minute per user

## Health Check

```python
# Check API health
import requests
response = requests.get("https://api.codeep.cc/v1/health")
print(response.json())  # {"status": "healthy", "service": "Codeep AI API"}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.