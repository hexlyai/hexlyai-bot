from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user(telegram_id):
    res = supabase.table("users").select("*").eq("telegram_id", str(telegram_id)).limit(1).execute()
    return res.data[0] if res.data else None

def mark_user_paid(telegram_id, email=None):
    user = {"telegram_id": str(telegram_id), "paid": True, "email": email}
    supabase.table("users").upsert(user, on_conflict="telegram_id").execute()

def insert_ads(platform, ad_list):
    for ad in ad_list:
        rec = {"platform": platform, **ad}
        supabase.table("ads").insert(rec).execute()

def latest_ads(limit=5, platform=None):
    q = supabase.table("ads").select("*").order("created_at", desc=True).limit(limit)
    if platform:
        q = q.eq("platform", platform)
    return q.execute().data
