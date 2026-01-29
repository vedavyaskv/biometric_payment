import os
import shutil
import cv2
import numpy as np
import json

# -------------------------------------------------
# CHECK IF USER DATA ALREADY EXISTS
# -------------------------------------------------
def check_user_exists(email, full_name, mobile):
    """
    Scans all registered users to check if the new credentials 
    already exist in the system.
    """
    base_path = "dataset"
    if not os.path.exists(base_path):
        return False, ""

    # Iterate through every folder in the dataset
    for user_folder in os.listdir(base_path):
        json_path = f"{base_path}/{user_folder}/user.json"
        
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                try:
                    data = json.load(f)
                    # Check for matches against unique enrollment criteria
                    if data.get("email") == email:
                        return True, "Email ID already registered"
                    if data.get("full_name") == full_name:
                        return True, "Full Name already exists"
                    if data.get("mobile") == mobile:
                        return True, "Mobile Number already exists"
                except json.JSONDecodeError:
                    continue
                    
    return False, ""

# -------------------------------------------------
# GET ALL REGISTERED USERS
# -------------------------------------------------
def get_all_users():
    """Returns a list of folder names (sanitized emails) from the dataset."""
    if not os.path.exists("dataset"):
        return []
    return [
        u for u in os.listdir("dataset")
        if os.path.isdir(f"dataset/{u}")
    ]


# -------------------------------------------------
# READ USER METADATA
# -------------------------------------------------
def get_user_data(username):
    """Fetches full JSON metadata for a specific user folder."""
    user_file = f"dataset/{username}/user.json"
    if not os.path.exists(user_file):
        return None

    with open(user_file, "r") as f:
        return json.load(f)


# -------------------------------------------------
# UPDATE FAILED ATTEMPTS
# -------------------------------------------------
def update_failed_attempts(username, success):
    """Resets or increments failed login attempts in user metadata."""
    user_file = f"dataset/{username}/user.json"
    if not os.path.exists(user_file):
        return

    with open(user_file, "r") as f:
        data = json.load(f)

    if success:
        data["failed_attempts"] = 0
    else:
        # Initialize key if it doesn't exist to prevent crashes
        data["failed_attempts"] = data.get("failed_attempts", 0) + 1

    with open(user_file, "w") as f:
        json.dump(data, f, indent=4)


# -------------------------------------------------
# UPDATE WALLET BALANCE & TRANSACTIONS
# -------------------------------------------------
# def update_transaction(username, amount, receiver_id):
#     """Updates the user's balance and records the transaction history."""
#     user_file = f"dataset/{username}/user.json"
#     if not os.path.exists(user_file):
#         return False

#     with open(user_file, "r") as f:
#         data = json.load(f)

#     # Deduct amount from balance
#     current_balance = data.get("balance", 0)
#     if current_balance >= amount:
#         data["balance"] = current_balance - amount
        
#         # Log transaction
#         transaction_entry = {
#             "to": receiver_id,
#             "amount": amount,
#             "timestamp": os.popen('date').read().strip() # Simplified timestamp
#         }
        
#         if "transactions" not in data:
#             data["transactions"] = []
#         data["transactions"].append(transaction_entry)

#         with open(user_file, "w") as f:
#             json.dump(data, f, indent=4)
#         return True
    
#     return False

import os, shutil, cv2, numpy as np, json

def get_all_users():
    if not os.path.exists("dataset"): return []
    return [u for u in os.listdir("dataset") if os.path.isdir(f"dataset/{u}")]

def get_user_data(username):
    path = f"dataset/{username}/user.json"
    if not os.path.exists(path): return None
    with open(path, "r") as f: return json.load(f)

def update_transaction(username, amount, receiver_id):
    path = f"dataset/{username}/user.json"
    data = get_user_data(username)
    if not data: return False
    
    curr_bal = float(data.get("balance", 0))
    if curr_bal >= amount:
        data["balance"] = curr_bal - amount
        if "transactions" not in data: data["transactions"] = []
        data["transactions"].append({"to": receiver_id, "amount": amount})
        with open(path, "w") as f: json.dump(data, f, indent=4)
        return True
    return False

def check_user_exists(email, name, mobile):
    for u in get_all_users():
        d = get_user_data(u)
        if d['email'] == email or d['mobile'] == mobile: return True, "User Exists"
    return False, ""

def delete_user(u):
    if os.path.exists(f"dataset/{u}"): shutil.rmtree(f"dataset/{u}")
# -------------------------------------------------
# UPDATE PROFILE PHOTO
# -------------------------------------------------
def update_profile_photo(username, uploaded_file):
    path = f"dataset/{username}/profile.jpg"

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is not None:
        cv2.imwrite(path, img)


# -------------------------------------------------
# DELETE USER COMPLETELY
# -------------------------------------------------
def delete_user(username):
    """Removes all files, photos, and QR codes associated with the user."""
    path = f"dataset/{username}"
    if os.path.exists(path):
        shutil.rmtree(path)


# -------------------------------------------------
# RENAME USER (FOLDER LEVEL)
# -------------------------------------------------
def rename_user(old_name, new_name):
    old_path = f"dataset/{old_name}"
    new_path = f"dataset/{new_name}"

    if not os.path.exists(old_path) or os.path.exists(new_path):
        return False

    os.rename(old_path, new_path)
    return True