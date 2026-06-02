# -*- coding: utf-8 -*-
"""יוצר שאלון Google Forms חי בחשבון של תום, דרך Forms API."""
import os, json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/forms.body"]
GMAIL_DIR = os.path.expanduser("~/.gmail")
CLIENT = os.path.join(GMAIL_DIR, "client_secret.json")
TOKEN = os.path.join(GMAIL_DIR, "token_forms.json")

def get_creds():
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return creds

service = build("forms", "v1", credentials=get_creds())

# 1) create the form (only title/documentTitle allowed at creation)
form = service.forms().create(body={
    "info": {
        "title": "שאלון סיכום — קורס נוירופדגוגיה ו-AI · פתח תקווה",
        "documentTitle": "שאלון סיכום נוירופדגוגיה",
    }
}).execute()
form_id = form["formId"]

# 2) add description + questions via batchUpdate
requests = [
    {"updateFormInfo": {
        "info": {"description": "תודה על המסע המשותף. כמה שאלות קצרות לסיכום הקורס — נשמח שתמלאו כאן ועכשיו."},
        "updateMask": "description"}},
]

items = [
    ("שם מלא", "short", True, None),
    ("שם בית הספר", "short", True, None),
    ("מה הם הדברים המרכזיים שאני לוקח/ת מההכשרה?", "para", False,
     "אפשר לכתוב כמה דברים — תובנה, פרקטיקה, מחשבה."),
    ("בכמה אתם מעריכים את תחושת המסוגלות העצמית שלכם אל מול הבינה המלאכותית?", "short", True,
     "נא לכתוב מספר בין 1 ל-100."),
    ("בהנחה שהייתי רוצה להשתתף בתהליך המשך, מה הייתי רוצה לקבל בו?", "para", False, None),
    ("דבר נוסף שרציתי לומר", "para", False, None),
]

for i, (title, kind, required, desc) in enumerate(items):
    q = {"required": required,
         "textQuestion": {"paragraph": kind == "para"}}
    item = {"title": title, "questionItem": {"question": q}}
    if desc:
        item["description"] = desc
    requests.append({"createItem": {"item": item, "location": {"index": i}}})

service.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()

responder = form["responderUri"]
edit = f"https://docs.google.com/forms/d/{form_id}/edit"
print("FORM_ID:", form_id)
print("RESPONDER_URL:", responder)
print("EDIT_URL:", edit)
