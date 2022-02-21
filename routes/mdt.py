from fastapi import APIRouter, Response
import time
import integrations
from collections import OrderedDict
router = APIRouter()

DEVICE_STORAGE = OrderedDict()


@router.get("/PostEvent", responses={204: {"model": None}})
async def post_event(computerName, stepName, currentStep, totalSteps, message, messageID):
    if messageID == "41003" and computerName in DEVICE_STORAGE:
        DEVICE_STORAGE[computerName]["stepTS"] = time.time()
    else:
        DEVICE_STORAGE[computerName] = dict(
            hostname=computerName, stepName=stepName, stepMessage=message, currentStep=currentStep, totalSteps=totalSteps, stepTS=time.time(), complete=messageID == "41015", error=messageID == "41014")
        for integration in integrations.INTEGRATIONS:
            integration(DEVICE_STORAGE[computerName])
    return Response(status_code=204)


@router.get("/deployments")
async def deployments():
    return DEVICE_STORAGE
