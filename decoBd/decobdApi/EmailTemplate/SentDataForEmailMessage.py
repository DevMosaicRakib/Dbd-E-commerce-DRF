def replace_placeholders(message, user_data):
    """
    Replaces placeholders like {username}, {phone} in the message with actual user data.
    user_data is expected to be a dictionary with keys matching the placeholders.
    """
    # Log the user_data being passed
    # print("User data:", user_data)

    for key, value in user_data.items():
        placeholder = f'{{{key}}}'  # Placeholder format is {key}
        # Log the current placeholder and value being replaced
        # print(f"Replacing placeholder: {placeholder} with {value}")
        message = message.replace(placeholder, str(value))
    
    # Log the final message after replacement
    # print("Final message after placeholder replacement:", message)

    return message
