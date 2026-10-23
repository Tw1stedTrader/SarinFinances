"""Sarin Finances — Cloudflare D1 access layer.

One function matters: run_sql(). Every page calls it with a SQL string
(and optional parameters) and gets back a list of row dicts.
"""

import requests
import streamlit as st

_API = "https://api.cloudflare.com/client/v4/accounts/{account}/d1/database/{database}/query"


def _config() -> dict:
    try:
        return {
            "account": st.secrets["CF_ACCOUNT_ID"],
            "database": st.secrets["CF_D1_DATABASE_ID"],
            "token": st.secrets["CF_API_TOKEN"],
        }
    except KeyError as missing:
        raise RuntimeError(f"Missing secret: {missing.args[0]}") from None


@st.cache_resource
def _session() -> requests.Session:
    cfg = _config()
    s = requests.Session()
    s.headers.update(
        {
            "Authorization": f"Bearer {cfg['token']}",
            "Content-Type": "application/json",
        }
    )
    return s


def run_sql(sql: str, params: list | tuple | None = None) -> list[dict]:
    """Send one SQL statement to D1 and return its rows as a list of dicts.

    Use ? placeholders in the SQL and pass the values in `params`, e.g.
        run_sql("SELECT * FROM t WHERE id = ?", [42])
    Statements that return nothing (INSERT/UPDATE/CREATE) return [].
    """
    cfg = _config()
    url = _API.format(account=cfg["account"], database=cfg["database"])
    body = {"sql": sql, "params": list(params or [])}

    resp = _session().post(url, json=body, timeout=30)
    data = resp.json()

    if not data.get("success"):
        errors = data.get("errors") or [{"message": f"HTTP {resp.status_code}"}]
        raise RuntimeError("; ".join(e.get("message", str(e)) for e in errors))

    results = data.get("result") or []
    if not results:
        return []
    return results[0].get("results") or []
