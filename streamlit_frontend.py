import streamlit as st
import requests
import json
from typing import Dict, List, Optional

# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# Backend API base URL
API_BASE = "http://localhost:8000/api"

def make_api_call(endpoint: str, method="GET", data=None, require_auth=True):
    """Make an API call to the backend"""
    headers = {"Content-Type": "application/json"}
    
    if require_auth and st.session_state.access_token:
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
    elif require_auth and not st.session_state.access_token:
        st.error("Not authenticated")
        return None
    
    url = f"{API_BASE}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        if response.status_code in [200, 201]:
            try:
                return response.json()
            except:
                return response.text
        elif response.status_code == 401:
            st.session_state.access_token = None
            st.session_state.user_email = None
            st.error("Authentication required. Please log in.")
            st.rerun()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None

def login_page():
    """Display login page"""
    st.title("Wishlist App")
    
    tab_login, tab_register = st.tabs(["Login", "Register"])
    
    with tab_login:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if email and password:
                data = make_api_call("/auth/login", "POST", {
                    "email": email,
                    "password": password
                }, require_auth=False)
                
                if data and "access_token" in data:
                    st.session_state.access_token = data["access_token"]
                    st.session_state.user_email = email
                    st.success("Successfully logged in!")
                    st.rerun()
            else:
                st.warning("Please enter email and password")
    
    with tab_register:
        st.subheader("Register")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        
        if st.button("Register"):
            if reg_email and reg_password and len(reg_password) >= 8:
                data = make_api_call("/auth/register", "POST", {
                    "email": reg_email,
                    "password": reg_password
                }, require_auth=False)
                
                if data:
                    st.success("Registration successful! You can now login.")
            else:
                st.warning("Please enter email and password (at least 8 characters)")

def logout():
    """Handle logout"""
    if st.session_state.access_token:
        make_api_call("/auth/logout", "POST", {}, require_auth=True)
    st.session_state.access_token = None
    st.session_state.user_email = None
    st.success("Logged out successfully")
    st.rerun()

def dashboard():
    """Main dashboard after login"""
    st.sidebar.title(f"Welcome, {st.session_state.user_email}")
    
    if st.sidebar.button("Logout"):
        logout()
    
    st.title("Your Wishlists")
    
    # Fetch wishlists
    wishlists = make_api_call("/wishlists", "GET", None, require_auth=True)
    
    if wishlists:
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.subheader("Create Wishlist")
            title = st.text_input("Title")
            description = st.text_area("Description (optional)")
            is_public = st.checkbox("Make Public")
            
            if st.button("Create"):
                if title:
                    new_wishlist = make_api_call("/wishlists", "POST", {
                        "title": title,
                        "description": description,
                        "is_public": is_public
                    })
                    
                    if new_wishlist:
                        st.success("Wishlist created!")
                        st.rerun()
                else:
                    st.warning("Please enter a title")
        
        with col1:
            st.subheader("Your Wishlists")
            
            if isinstance(wishlists, list) and len(wishlists) > 0:
                for wl in wishlists:
                    with st.expander(f"{wl['title']} ({'Public' if wl['is_public'] else 'Private'})"):
                        st.write(f"**ID:** {wl['id']}")
                        st.write(f"**Description:** {wl['description'] or 'No description'}")
                        
                        # Show share token if public
                        if wl['is_public'] and wl.get('share_token'):
                            st.write(f"**Share Token:** {wl['share_token']}")
                        
                        # Edit wishlist form
                        st.write("**Edit Wishlist:**")
                        edit_title = st.text_input("New Title", value=wl['title'], key=f"title_{wl['id']}")
                        edit_desc = st.text_area("New Description", value=wl['description'] or "", key=f"desc_{wl['id']}")
                        edit_public = st.checkbox("Make Public", value=wl['is_public'], key=f"pub_{wl['id']}")
                        
                        if st.button(f"Update Wishlist {wl['id']}", key=f"update_{wl['id']}"):
                            updated_data = make_api_call(f"/wishlists/{wl['id']}", "PUT", {
                                "title": edit_title,
                                "description": edit_desc,
                                "is_public": edit_public
                            })
                            
                            if updated_data:
                                st.success("Wishlist updated!")
                                st.rerun()
                        
                        # Delete button
                        if st.button(f"Delete Wishlist {wl['id']}", key=f"delete_{wl['id']}", type="secondary"):
                            delete_confirm = st.checkbox(f"Confirm deletion of '{wl['title']}'", key=f"confirm_{wl['id']}")
                            if delete_confirm:
                                deleted = make_api_call(f"/wishlists/{wl['id']}", "DELETE")
                                if deleted:
                                    st.success("Wishlist deleted!")
                                    st.rerun()
                        
                        # Manage gifts in this wishlist
                        st.write("---")
                        st.write("**Gifts in this wishlist:**")
                        
                        # Fetch gifts for this wishlist
                        gifts = make_api_call(f"/wishlists/{wl['id']}/gifts", "GET")
                        if gifts:
                            for gift in gifts:
                                with st.container():
                                    st.write(f"- **{gift['name']}** - {gift['description'] or 'No description'}")
                                    st.write(f"  Price: {gift['price'] or 'N/A'} | Link: {gift['link'] or 'N/A'}")
                                    
                                    # Edit gift buttons
                                    col_a, col_b = st.columns(2)
                                    with col_a:
                                        if st.button(f"Edit Gift {gift['id']}", key=f"edit_gift_{gift['id']}"):
                                            # Toggle edit form visibility
                                            edit_key = f"edit_form_{gift['id']}"
                                            if edit_key not in st.session_state:
                                                st.session_state[edit_key] = True
                                            else:
                                                st.session_state[edit_key] = not st.session_state[edit_key]
                                    
                                    with col_b:
                                        if st.button(f"Delete Gift {gift['id']}", key=f"del_gift_{gift['id']}", type="secondary"):
                                            del_confirm = st.checkbox(f"Confirm deletion of '{gift['name']}'", key=f"conf_del_{gift['id']}")
                                            if del_confirm:
                                                make_api_call(f"/gifts/{gift['id']}", "DELETE")
                                                st.rerun()
                                    
                                    # Show edit form if toggled
                                    if st.session_state.get(edit_key, False):
                                        with st.form(key=f"edit_gift_form_{gift['id']}"):
                                            new_name = st.text_input("Name", value=gift['name'])
                                            new_desc = st.text_input("Description", value=gift['description'] or "")
                                            new_price = st.text_input("Price", value=gift['price'] or "")
                                            new_link = st.text_input("Link", value=gift['link'] or "")
                                            
                                            if st.form_submit_button("Update Gift"):
                                                make_api_call(f"/gifts/{gift['id']}", "PUT", {
                                                    "name": new_name,
                                                    "description": new_desc,
                                                    "price": float(new_price) if new_price else None,
                                                    "link": new_link
                                                })
                                                st.session_state[edit_key] = False
                                                st.rerun()
                        
                        # Add gift form
                        st.write("**Add a gift:**")
                        with st.form(key=f"add_gift_{wl['id']}"):
                            gift_name = st.text_input("Gift Name", key=f"gname_{wl['id']}")
                            gift_desc = st.text_input("Description", key=f"gdesc_{wl['id']}")
                            gift_price = st.text_input("Price", key=f"gprice_{wl['id']}")
                            gift_link = st.text_input("Link", key=f"glink_{wl['id']}")
                            
                            if st.form_submit_button("Add Gift"):
                                if gift_name:
                                    new_gift = make_api_call(f"/wishlists/{wl['id']}/gifts", "POST", {
                                        "name": gift_name,
                                        "description": gift_desc,
                                        "price": float(gift_price) if gift_price else None,
                                        "link": gift_link
                                    })
                                    
                                    if new_gift:
                                        st.success("Gift added!")
                                        st.rerun()
                                else:
                                    st.warning("Please enter a gift name")
            else:
                st.info("No wishlists yet. Create one using the form on the right!")

def main():
    """Main application"""
    if not st.session_state.access_token:
        login_page()
    else:
        dashboard()

if __name__ == "__main__":
    main()