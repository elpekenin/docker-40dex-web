import os

db_uri  = os.getenv("DB_URI")

db_ip   = os.getenv("DB_IP")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_auth = os.getenv("DB_AUTH")

rm_pass = os.getenv("RM_PASS")

scheme = os.getenv("SV_SCHEME")
domain = os.getenv("SV_DOMAIN")

gh_link = os.getenv("GH_LINK")
