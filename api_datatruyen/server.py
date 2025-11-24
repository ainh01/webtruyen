import logging
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse, StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import httpx
import secrets
from datetime import timedelta, datetime
from jose import JWTError, jwt
from typing import List
from bson import ObjectId

from io import BytesIO
from PIL import Image
from fpdf import FPDF
import aiofiles
import tempfile
import os 

from model import User, UserInDB, UserLogin, UserInfo, UserResponse, UserActive, HomeForClient, FavoriteForUser, HistoryComicRequest

# Generate a random 32-byte key and convert it to a hexadecimal string
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"  # Algorithm used for signing the JWT (HMAC SHA-256)
ACCESS_TOKEN_EXPIRE_MINUTES = 300  # Token expiry time in minutes  

EXTERNAL_API_BASE_URL = os.getenv('EXTERNAL_API','mongodb://localhost:27017')
# EXTERNAL_API_BASE_URL = "https://otruyenapi.com/v1/api/"
IMAGE_API_BASE_URL = os.getenv('IMAGE_API', 'https://otruyenapi.com/vi/api/')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn, có thể giới hạn theo cần thiết
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức
    allow_headers=["*"],  # Cho phép tất cả các header
)

MONGO_URI = os.getenv('MONGODB_DATA_API',"mongodb://localhost:27017/")  
DATABASE_NAME = os.getenv('MONGODB_DATA_DB',"CNPM_truyentranh_db")
comic = "comic"
user = "user"
favorites = "favorites"
history = "history"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
comics_collection = db[comic]   
users_collection = db[user]
favorites_collection = db[favorites]
history_collection = db[history]

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to convert MongoDB documents to JSON serializable format
def serialize_document(doc):
    if isinstance(doc, list):
        # Recursively serialize list of documents
        return [serialize_document(d) for d in doc]
    elif isinstance(doc, dict):
        # Convert ObjectId fields to string
        return {key: str(value) if isinstance(value, ObjectId) else value for key, value in doc.items()}
    return doc

# JWT Token Handling
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception

@app.post("/register/")
async def register(user: User):
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists.")

    if await users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists.")

    hashed_password = hash_password(user.password)
    new_user = UserInDB(
        **user.dict(), hashed_password=hashed_password, created_at=datetime.utcnow()
    )

    await users_collection.insert_one(new_user.dict())
    return {"message": "Registration successful!"}

@app.post("/login/")
async def login(user: UserLogin):
    db_user = await users_collection.find_one({"email": user.email})
    
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password.")
    if not db_user.get("active", False):
        raise HTTPException(status_code=403, detail="Account loss access.")
    
    token = create_access_token(data={"sub": db_user["email"]})
    return {
        "message": "Login successful!",
        "user": db_user["username"],
        "token": token,
    }

#---------------------------------------#

@app.get("/user/", response_model=UserInfo)
async def get_user_info(current_user: str = Depends(get_current_user)):
    db_user = await users_collection.find_one({"email": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return UserInfo(username=db_user["username"], email=db_user["email"])

@app.post("/logout/")
async def logout():
    response = JSONResponse(content={"message": "Logout successful!"})
    response.delete_cookie(key="access_token", httponly=True, secure=True)
    return response

@app.get("/table_users", response_model=List[UserResponse])
async def get_table_users():
    # Lấy tất cả user từ MongoDB
    users = await users_collection.find().to_list(length=None)  # Chuyển đổi Cursor thành danh sách
    # Chuyển đổi dữ liệu thành danh sách các UserResponse
    response = [
        UserResponse(username=user["username"], 
                     email=user["email"], 
                     created_at=datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%S") if isinstance(user.get("created_at", ""), str) else user.get("created_at"), 
                     active=user["active"]) 
        for user in users
    ]
    return response

@app.post("/set_user_active/")
async def SetUserActive(response_model: UserActive):
    try:
        data = {
            "email": response_model.email,
            "active": response_model.active,
            "updated_at": datetime.utcnow()
        }

        result = await users_collection.update_one(
            {"email": response_model.email},  
            {"$set": data},  
            upsert=True  
        )

        return {"message": "Data set successfully", "modified_count": result.modified_count}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


#---------------------------------------#

# Hàm để lưu dữ liệu về danh sách truyện vào MongoDB
@app.post("/set_home_client")
async def SetHomeClient(comic_client: HomeForClient):
    try:
        data = {
            "id_comic": comic_client.id_comic,
            "switch": comic_client.switch,
            "updated_at": datetime.utcnow()
        }

        result = await comics_collection.update_one(
            {"id_comic": comic_client.id_comic},  
            {"$set": data},  
            upsert=True  
        )

        return {"message": "Data set successfully", "modified_count": result.modified_count}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/home_admin")
async def GetHomeAdmin():
    try:
        async with httpx.AsyncClient() as client:
            external_response = await client.get(f"{EXTERNAL_API_BASE_URL}the-loai/co-dai")
        
        if external_response.status_code != 200:
            raise HTTPException(
                status_code=external_response.status_code,
                detail=f"Error fetching external API: {external_response.text}"
            )
        
        external_data = external_response.json()
        
        if not isinstance(external_data, dict):
            raise HTTPException(status_code=500, detail="Invalid response format from external API.")
        
        external_comics = external_data.get("data", [])
        
        filtered_comics = []
        for comic in external_comics.get("items", []):
            comic_id = comic.get("_id")
            if not comic_id:
                continue 
            
            mongo_entry = await comics_collection.find_one({"id_comic": comic_id})
            
            if mongo_entry:
                comic["switch"] = mongo_entry.get("switch", "Unknown")
            else:
                comic["switch"] = "Online"
            
            # Thêm vào danh sách trả về
            filtered_comics.append(comic)
        
        return {"data": filtered_comics}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/home_client")
async def GetHomeClient():
    try:
        async with httpx.AsyncClient() as client:
            external_response = await client.get(f"{EXTERNAL_API_BASE_URL}the-loai/co-dai")
        
        if external_response.status_code != 200:
            raise HTTPException(
                status_code=external_response.status_code,
                detail=f"Error fetching external API: {external_response.text}"
            )
        
        external_data = external_response.json()
        
        if not isinstance(external_data, dict):
            raise HTTPException(status_code=500, detail="Invalid response format from external API.")
        
        external_comics = external_data.get("data", [])
        
        filtered_comics = []
        for comic in external_comics.get("items", []):
            comic_id = comic.get("_id")
            if not comic_id:
                continue 
            mongo_entry = await comics_collection.find_one({"id_comic": comic_id})
            
            if mongo_entry:
                if mongo_entry.get("switch") == "Offline":
                    continue
            
            # Thêm vào danh sách trả về
            filtered_comics.append(comic)
        
        return {"items": filtered_comics}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#---------------------------------------#

# Hàm để lưu dữ liệu yêu thích vào MongoDB

# 1. API thêm/cập nhật trạng thái yêu thích
@app.post("/set_favorite_client")
async def set_favorite_client(favorite_user: FavoriteForUser):
    try:
        # Dữ liệu cần cập nhật
        data = {
            "id_comic": favorite_user.id_comic,
            "email": favorite_user.email,
            "status": favorite_user.status,
            "updated_at": datetime.utcnow()
        }

        # Cập nhật hoặc thêm mới
        result = await favorites_collection.update_one(
            {"id_comic": favorite_user.id_comic, "email": favorite_user.email},  
            {"$set": data},  
            upsert=True  
        )

        return {"message": "Data set successfully", "modified_count": result.modified_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_favorite_client")
async def get_favorite_client(email: str, id_comic: str):
    try:
        favorite = await favorites_collection.find_one(
            {"email": email, "id_comic": id_comic }
        )
        if not favorite:
            return {"status": False}  # Mặc định là không yêu thích
        return {"status": favorite["status"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# 3. API lấy danh sách truyện yêu thích của một người dùng
@app.get("/get_favorite_list")
async def get_favorite_list(email: str):
    try:
        favorites = await favorites_collection.find({"email": email}).to_list(length=None)
        if not favorites:
            return {"data": []} 

        # Serialize the documents to make them JSON serializable
        favorites = serialize_document(favorites)
        
        return {"data": favorites}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    
#---------------------------------------#

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_pdf_from_images(image_urls: list, output_pdf_path: str):
    images = []  # Danh sách lưu trữ các hình ảnh
    try:
        # Tải tất cả hình ảnh từ các URL
        async with httpx.AsyncClient() as client:
            for url in image_urls:
                response = await client.get(url)
                response.raise_for_status()  # Kiểm tra lỗi khi tải ảnh
                
                # Chuyển dữ liệu từ response thành đối tượng hình ảnh PIL
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                images.append(image)  # Thêm hình ảnh vào danh sách
        
        # Kiểm tra xem có hình ảnh nào không
        if images:
            # Lưu tất cả hình ảnh vào PDF
            images[0].save(output_pdf_path, save_all=True, append_images=images[1:], resolution=100.0, quality=95)
            logger.info(f"PDF đã được tạo tại: {output_pdf_path}")
            return output_pdf_path
        else:
            logger.error("Không có hình ảnh nào được tải về.")
            raise HTTPException(status_code=500, detail="No images were downloaded.")
    
    except httpx.RequestError as e:
        logger.error(f"Error fetching images: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching images: {e}")

@app.post("/download_comic")
async def download_comic(comic_id: str, chapter_ids: list[str]):
    try:
        all_images = []
        logger.info(f"Starting to process comic: {comic_id} with chapters: {chapter_ids}")
        
        # Bước 1: Tải thông tin truyện từ API bên ngoài
        async with httpx.AsyncClient() as client:
            try:
                external_response = await client.get(f"{EXTERNAL_API_BASE_URL}truyen-tranh/{comic_id}")
                external_response.raise_for_status()
            except httpx.RequestError as e:
                logger.error(f"Error fetching comic details for {comic_id}: {e}")
                raise HTTPException(status_code=500, detail=f"Error fetching comic details: {e}")

            external_data = external_response.json()
            external_comics = external_data.get("data", {}).get("item", {}).get("chapters", [])
            
            server_data = []
            for chapter in external_comics:
                if "server_data" in chapter:
                    server_data.extend(chapter["server_data"])

        # Bước 2: Tải hình ảnh từ các chương truyện
        async with httpx.AsyncClient() as client:
            for chapter_id in chapter_ids:
                logger.info(f"Fetching chapter: {chapter_id}")
                
                # Tìm thông tin chapter tương ứng từ server_data
                chapter_api_data = next(
                    (chapter["chapter_api_data"] for chapter in server_data if chapter["chapter_name"] == chapter_id), 
                    None
                )
                
                if not chapter_api_data:
                    logger.error(f"Chapter ID {chapter_id} not found in server data.")
                    raise HTTPException(status_code=404, detail=f"Chapter ID {chapter_id} not found.")
                
                try:
                    chapter_response = await client.get(chapter_api_data)
                    chapter_response.raise_for_status()
                    
                    chapter_data = chapter_response.json()
                    chapter_images = chapter_data['data']['item'].get('chapter_image', [])
                    domain_cdn = chapter_data['data']['domain_cdn']
                    chapter_path = chapter_data['data']['item'].get('chapter_path', '')

                    # Tạo URL của tất cả hình ảnh trong chapter
                    image_urls = [
                        f"{domain_cdn}/{chapter_path}/{img['image_file']}" 
                        for img in chapter_images if 'image_file' in img
                    ]
                    
                    all_images.extend(image_urls)
                
                except Exception as e:
                    logger.error(f"Unexpected error while fetching chapter {chapter_id}: {e}")
                    raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

        # Bước 3: Tạo PDF từ các hình ảnh đã tải về
        logger.info("Creating PDF from images")
        
        # Tạo PDF từ hình ảnh và trả về kết quả
        pdf_buffer = await generate_pdf_from_images(all_images, f"{comic_id}.pdf")

        return StreamingResponse(
            pdf_buffer, 
            media_type="application/pdf", 
            headers={"Content-Disposition": f"attachment; filename={comic_id}.pdf"}
        )
        
    except Exception as e:
        logger.error(f"Unexpected error during comic download process: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    
    
#---------------------------------------#

# History comics

@app.post("/set_history_comics")
async def set_history_comics(request: HistoryComicRequest):
    try:
        data = request.dict()
        data["updated_at"] = datetime.utcnow()

        result = await history_collection.update_one(
            {"id_comic": data["id_comic"], "email": data["email"]},  
            {"$set": data},  
            upsert=True  
        )

        return {"message": "Data set successfully", "modified_count": result.modified_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_history_comics")
async def get_history_comics(email: str):
    try:
        histories = await history_collection.find({"email": email}).to_list(length=None)
        if not histories:
            return {"data": []} 

        # Serialize the documents to make them JSON serializable
        histories = serialize_document(histories)
        
        return {"data": histories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
