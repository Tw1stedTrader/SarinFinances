"""Sarin Finances — sign-in gate.

Every page calls require_login() first. It uses Streamlit's built-in
Google sign-in and only lets through the email addresses listed in
secrets under ALLOWED_EMAILS. Nothing else renders until then.
"""

import streamlit as st


def _allowed_emails() -> set[str]:
    raw = st.secrets.get("ALLOWED_EMAILS", [])
    if isinstance(raw, str):
        raw = [raw]
    return {e.strip().lower() for e in raw if e and e.strip()}


def require_login() -> str:
    """Stop the page unless a permitted Google account is signed in.

    Returns the signed-in email so a page can show it if it wants to.
    """
    if not st.user.is_logged_in:
        st.title("Sarin Finances")
        st.button("Sign In With Google", type="primary", on_click=st.login)
        st.stop()

    email = (st.user.email or "").strip().lower()
    if email not in _allowed_emails():
        st.title("Sarin Finances")
        st.error("This Google account is not allowed to open this app.")
        st.button("Sign Out", on_click=st.logout)
        st.stop()

    return email


def sign_out_button() -> None:
    """Small sign-out control for the sidebar."""
    st.sidebar.button("Sign Out", on_click=st.logout, key="sign_out")
