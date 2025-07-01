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
