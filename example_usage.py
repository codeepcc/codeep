#!/usr/bin/env python3
"""
Example usage of Codeep AI Python SDK with LangChain compatibility
"""

from src.codeep import CodeepClient, CodeepLLM, Config

def main():
    # Configure environment (optional)
    Config.set_environment("development")  # Uses localhost:5001
    # Config.set_environment("production")   # Uses https://api.codeep.cc/v1

    # Initialize client
    client = CodeepClient()

    # Example 1: Direct API usage
    print("=== Direct API Usage ===")

    # Note: These would require actual API credentials and a running server
    # For demonstration purposes only
    print("Client initialized successfully")
    print(f"Base URL: {client.base_url}")
    print(f"Environment: {Config.ENVIRONMENT}")
    print(f"LLM type: {client.llm._llm_type}")

    # Example 2: LangChain integration
    print("\n=== LangChain Integration ===")

    # Create LLM instance
    llm = client.llm

    print(f"Model name: {llm.model_name}")
    print(f"Timeout: {llm.timeout}s")
    print(f"Poll interval: {llm.poll_interval}s")

    # Example 3: Using with LangChain chains (conceptual)
    print("\n=== LangChain Chain Usage (Conceptual) ===")
    print("""
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate

    # Create prompt template
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Write a short summary about {topic}"
    )

    # Create chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run chain (would require actual API)
    # result = chain.run(topic="artificial intelligence")
    # print(result)
    """)

    # Example 4: Authentication flow
    print("\n=== Authentication Flow ===")
    print("""
    # Register new user
    # response = client.register("username", "email@example.com", "password")

    # Login
    # login_data = client.login("username", "password")
    # token = login_data['access_token']

    # Or set token directly
    # client.set_token("your_token_here")

    # Check quota
    # quota = client.get_quota()
    # print(f"Remaining: {quota['remaining']}")

    # Get current user
    # user = client.get_current_user()
    # print(f"User: {user.username}")
    """)

    # Example 5: Task management
    print("\n=== Task Management ===")
    print("""
    # Create a task
    # task = client.create_task(
    #     prompt="Analyze this dataset and create visualizations",
    #     toolset=["code_executor", "file_reader"]
    # )

    # Wait for completion
    # completed_task = client.wait_for_completion(task.task_id, timeout=600)

    # Get results
    # if completed_task.status == "completed":
    #     print(f"Result: {completed_task.result}")
    # else:
    #     print(f"Error: {completed_task.error_message}")
    """)

if __name__ == "__main__":
    main()