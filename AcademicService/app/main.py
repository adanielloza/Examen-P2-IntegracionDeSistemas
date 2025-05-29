from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="AcademicService (SolicitudService)")
bearer = HTTPBearer()

# Point these at your in-mesh DNS names (or localhost+port if port-forwarding)
SECURITY_VERIFY_URL = os.getenv("SECURITY_VERIFY_URL", "http://localhost:8005/verify")
SOAP_REGISTER_URL = os.getenv("SOAP_REGISTER_URL", "http://localhost:8006/")

class SolicitudIn(BaseModel):
    student_id: str
    type:       str

class Solicitud(BaseModel):
    id:         int
    student_id: str
    type:       str
    status:     str

# simple in-memory storage
_db      = {}
_next_id = 1

def verify_token(
    creds: HTTPAuthorizationCredentials = Depends(bearer)
):
    """
    Calls SecurityService /verify. Raises 401 if invalid.
    Returns the decoded claims dict on success.
    """
    token = creds.credentials
    resp = requests.get(SECURITY_VERIFY_URL,
                        headers={"Authorization": f"Bearer {token}"})
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return resp.json()

@app.post("/solicitudes", response_model=Solicitud)
def create_solicitud(
    req: SolicitudIn,
    user=Depends(verify_token)
):
    """
    1) Verify JWT (user)
    2) Call external SOAP to register cert
    3) Persist and return final status
    """
    global _next_id

    # --- 2) mock SOAP call ---
    # in real life you'd construct a proper SOAP envelope or use zeep.Client(...)
    soap_envelope = f"""
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <RegisterCertRequest>
          <studentId>{req.student_id}</studentId>
          <type>{req.type}</type>
        </RegisterCertRequest>
      </soap:Body>
    </soap:Envelope>
    """
    soap_resp = requests.post(
        SOAP_REGISTER_URL,
        data=soap_envelope,
        headers={"Content-Type": "text/xml"}
    )

    status = "procesado" if soap_resp.status_code == 200 else "rechazado"

    # --- 3) store and return ---
    record = Solicitud(
        id=         _next_id,
        student_id=req.student_id,
        type=       req.type,
        status=     status
    )
    _db[_next_id] = record
    _next_id += 1
    return record

@app.get("/solicitudes/{solicitud_id}", response_model=Solicitud)
def get_solicitud(
    solicitud_id: int,
    user=Depends(verify_token)
):
    """
    Fetch by ID (401 if token bad, 404 if not found)
    """
    record = _db.get(solicitud_id)
    if not record:
        raise HTTPException(status_code=404, detail="Solicitud not found")
    return record
