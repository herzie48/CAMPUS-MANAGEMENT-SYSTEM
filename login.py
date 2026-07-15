import utils
import file_manager

def validate_password(password):
    """Validates that the password is at least 6 characters long and not empty."""
    if len(password) < 6:
        utils.print_error("Password must be at least 6 characters long.")
        return False
    return True

def login_user(users):
    """Handles the user login flow.
    
    Prompts for username and password, verifies them, and returns a tuple (username, role)
    if authentication is successful. Returns (None, None) otherwise.
    """
    utils.print_header("User Login")
    username = utils.get_valid_string("Enter Username: ")
    password = utils.get_valid_string("Enter Password: ")
    
    if username in users:
        if users[username]["password"] == password:
            utils.print_success(f"Login Successful! Welcome {username} ({users[username]['role']}).")
            return username, users[username]["role"]
        else:
            utils.print_error("Incorrect password.")
    else:
        utils.print_error("Username not found.")
        
    return None, None

def change_password(username, data):
    """Allows an authenticated user to change their password."""
    utils.print_header("Change Password")
    
    users = data["users"]
    if username not in users:
        utils.print_error("User not found.")
        return False
        
    old_password = utils.get_valid_string("Enter Current Password: ")
    if users[username]["password"] != old_password:
        utils.print_error("Current password does not match. Action cancelled.")
        return False
        
    while True:
        new_password = utils.get_valid_string("Enter New Password: ")
        if validate_password(new_password):
            break
            
    users[username]["password"] = new_password
    file_manager.save_users(users)
    utils.print_success("Password changed successfully!")
    return True

def add_user_account(username, password, role, data):
    """Helper function to create a new user login account.
    Usually called when adding students or faculty members.
    """
    users = data["users"]
    if username in users:
        # Account already exists
        return False
    users[username] = {
        "username": username,
        "password": password,
        "role": role
    }
    file_manager.save_users(users)
    return True

def remove_user_account(username, data):
    """Helper function to remove a user login account when a student or faculty is deleted."""
    users = data["users"]
    if username in users:
        del users[username]
        file_manager.save_users(users)
        return True
    return False
