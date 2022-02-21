import settings
import requests
import html
INTEGRATIONS = []

MESSAGE_COMPLETE = """
🖥✅Deployment of <b>{hostname}</b> complete!
""".strip()
MESSAGE_ERROR = """
🖥❌Deployment of <b>{hostname}</b> <b>FAILED</b>!
{currentStep} out of {totalSteps}.
<b>{stepName}</b>
<i>{stepMessage}</i>
"""
MESSAGE_IN_PROGRESS = """
🖥⏳Deployment of <b>{hostname}</b> in progress...
{currentStep} out of {totalSteps}.
<b>{stepName}</b>
<i>{stepMessage}</i>
"""
TELEGRAM_INTEGRATION_MIDS = {}


def telegram_integration(storage_item_original):
    storage_item = {}
    for k, v in storage_item_original.items():
        if isinstance(v, str):
            storage_item[k] = html.escape(v)
        else:
            storage_item[k] = v
    if storage_item["complete"]:
        message = MESSAGE_COMPLETE.format(**storage_item)
    elif storage_item["error"]:
        message = MESSAGE_ERROR.format(**storage_item)
    else:
        message = MESSAGE_IN_PROGRESS.format(**storage_item)
    if storage_item["hostname"] in TELEGRAM_INTEGRATION_MIDS and not storage_item["complete"]:
        requests.post(f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/editMessageText",
                      json={"chat_id": settings.TELEGRAM_CHAT, "message_id": TELEGRAM_INTEGRATION_MIDS[storage_item['hostname']], "text": message, "parse_mode": "HTML"})
    elif storage_item['complete'] or storage_item["error"]:
        requests.post(f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage",
                      json={"chat_id": settings.TELEGRAM_CHAT, "text": message, "parse_mode": "HTML"})
        if storage_item['hostname'] in TELEGRAM_INTEGRATION_MIDS:
            del TELEGRAM_INTEGRATION_MIDS[storage_item['hostname']]
    else:
        r = requests.post(f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage",
                          json={"chat_id": settings.TELEGRAM_CHAT, "text": message, "parse_mode": "HTML"})
        r = r.json()
        print(r)
        TELEGRAM_INTEGRATION_MIDS[storage_item['hostname']
                                  ] = r["result"]["message_id"]


if settings.TELEGRAM_INTEGRATION:
    INTEGRATIONS.append(telegram_integration)
