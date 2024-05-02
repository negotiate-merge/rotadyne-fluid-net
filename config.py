LOCAL = True

# Using local chirpstack server
if LOCAL:
    # Chirpstack specific
    server = "<ip_address_or_hostname>"
    api_token = "<api_token_from_chirpsatck_ui>"
    app_id = "<application_id_from_chirpstack_ui>"
    # GUI - ssh specific
    r_user = "<remote_host_user>"
    r_key_path = "<path_to_private_ssh_key_for_r_user>"

# Using gcloud chirpstack server
else:
    # Chirpstack specific
    server = "<ip_address_or_hostname>"
    api_token = "<api_token_from_chirpsatck_ui>"
    app_id = "<application_id_from_chirpstack_ui>"
    # GUI - ssh specific
    r_user = "<remote_host_user>"
    r_key_path = "<path_to_private_ssh_key_for_r_user>"