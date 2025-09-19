
import hashlib
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from database import connection

app = FastAPI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ping")
def ping():
    try:
        supabase = connection.connect()
        response = supabase.table('users').select("*").limit(1).execute()
        return JSONResponse(content={"success": True, "status": "Database connection successful"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


async def user_exists(supabase, username: str) -> bool:
    response = supabase.table('users').select("*").eq("username", username).execute()
    return response.data is not None

'''
Example curl

curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario1", "password": "tu_contraseña"}'
'''
@app.post("/api/register")
async def register(payload: dict):
    supabase = connection.connect()
    username = payload.get("username")
    password = payload.get("password")  


    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    
    if not await user_exists(supabase, username):
        raise HTTPException(status_code=400, detail="Username already exists")

    
    response = supabase.table("users").insert({"username": username, "password": password }).execute()
    if response.data is None:
        raise HTTPException(status_code=500, detail="Failed to register user")
    
    return JSONResponse(content={"success": True, "message": "User registered successfully"})

'''
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario1",
    "password": "passwordsegura"
  }'
'''

@app.post("/api/login")
async def login(payload: dict):
    supabase = connection.connect()
    username = payload.get("username")
    password = payload.get("password")

    response = supabase.table('users').select("*").eq("username", username).eq("password", password).execute()

    if len(response.data) == 0:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return JSONResponse(content={"success": True, "message": "Login successful"})
if __name__ == "__main__":
    app.run()
