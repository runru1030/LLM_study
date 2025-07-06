def pretty_print_messages(response):
    messages = response.get("messages") if isinstance(response, dict) else response

    if not isinstance(messages, list):
        messages = [messages]
    print("=" * 40)
    for msg in messages:
        role = (
            getattr(msg, "role", None)
            or getattr(msg, "type", None)
            or msg.__class__.__name__
        )
        content = getattr(msg, "content", str(msg))
        print(f"[{role.upper()}]")
        print(content)
        print("-" * 40)
    print("=" * 40)

    # 토큰 사용량 출력
    total_input_tokens = 0
    total_output_tokens = 0
    total_total_tokens = 0

    for msg in messages:
        # response_metadata에서 토큰 정보 추출
        response_metadata = getattr(msg, "response_metadata", {})
        if isinstance(response_metadata, dict):
            token_usage = response_metadata.get("token_usage", {})
            total_input_tokens += token_usage.get("prompt_tokens", 0)
            total_output_tokens += token_usage.get("completion_tokens", 0)
            total_total_tokens += token_usage.get("total_tokens", 0)

    if total_total_tokens > 0:
        print(f"input_tokens: {total_input_tokens}")
        print(f"output_tokens: {total_output_tokens}")
        print(f"total_tokens: {total_total_tokens}")
