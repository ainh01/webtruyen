from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient, DESCENDING, ASCENDING
from bson import ObjectId
from typing import Optional, List
import os
from datetime import datetime
import math

app = FastAPI(title="OTruyen API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_uri_str = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
db_name_str = os.getenv('DB_NAME', 'otruyen_db')

client = MongoClient(mongo_uri_str)
db = client[db_name_str]
client.admin.command('ping')

# Collections
comics_collection = db['comics']
chapters_collection = db['chapters']
categories_collection = db['categories']
images_collection = db['images']

# Helper functions
def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable"""
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

def serialize_list(docs):
    """Convert list of MongoDB documents to JSON serializable"""
    return [serialize_doc(doc) for doc in docs]

def create_success_response(data, message=""):
    """Create standard success response"""
    return {
        "status": "success",
        "message": message,
        "data": data
    }

def create_comic_response(comic_data):
    """Create comic detail response similar to otruyenapi"""
    if not comic_data:
        return None
    
    # Get chapters for this comic
    chapters = list(chapters_collection.find(
        {"comic_slug": comic_data["slug"]}
    ).sort("chapter_name", ASCENDING))
    
    # Group chapters by server
    servers = {}
    for chapter in chapters:
        server_name = chapter.get("server_name", "Server #1")
        if server_name not in servers:
            servers[server_name] = []
        
        servers[server_name].append({
            "filename": chapter.get("filename", ""),
            "chapter_name": chapter.get("chapter_name", ""),
            "chapter_title": chapter.get("chapter_title", ""),
            "chapter_api_data": chapter.get("chapter_api_url", "")
        })
    
    # Convert to list format
    chapters_list = []
    for server_name, server_data in servers.items():
        chapters_list.append({
            "server_name": server_name,
            "server_data": server_data
        })
    
    return {
        "seoOnPage": {
            "og_type": "website",
            "titleHead": f"{comic_data['name']} - ",
            "seoSchema": {
                "@context": "https://schema.org",
                "@type": "website",
                "name": f"{comic_data['name']} - ",
                "url": f"https://otruyen.cc/truyen-tranh/{comic_data['slug']}",
                "image": f"https://img.otruyenapi.com/uploads/comics/{comic_data.get('thumb_url', '')}",
                "director": comic_data.get('author', ['Unknown'])[0] if comic_data.get('author') else "Unknown"
            },
            "descriptionHead": comic_data.get('content', '')[:200] + "..." if comic_data.get('content') else "",
            "og_image": [f"comics/{comic_data.get('thumb_url', '')}"],
            "updated_time": int(datetime.now().timestamp() * 1000),
            "og_url": f"truyen-tranh/{comic_data['slug']}"
        },
        "breadCrumb": [
            {
                "name": "Trang chủ",
                "slug": "/",
                "position": 1
            },
            *[
                {
                    "name": cat["name"],
                    "slug": f"/the-loai/{cat['slug']}",
                    "position": 2
                } for cat in comic_data.get('category', [])
            ][:1],  # Only first category
            {
                "name": comic_data['name'],
                "isCurrent": True,
                "position": 3
            }
        ],
        "params": {
            "slug": comic_data['slug'],
            "crawl_check_url": ""
        },
        "item": {
            "_id": comic_data['_id'],
            "name": comic_data['name'],
            "slug": comic_data['slug'],
            "origin_name": comic_data.get('origin_name', []),
            "content": comic_data.get('content', ''),
            "status": comic_data.get('status', 'ongoing'),
            "thumb_url": comic_data.get('thumb_url', ''),
            "sub_docquyen": comic_data.get('sub_docquyen', False),
            "author": comic_data.get('author', []),
            "category": comic_data.get('category', []),
            "chapters": chapters_list,
            "updatedAt": comic_data.get('updatedAt', datetime.now().isoformat())
        },
        "APP_DOMAIN_CDN_IMAGE": "https://img.otruyenapi.com"
    }

@app.get("/")
async def home():
    """Trang chủ - lấy truyện mới cập nhật"""
    try:
        # Lấy truyện mới cập nhật (có chapters)
        recent_comics = list(comics_collection.find(
            {"chapters_count": {"$gt": 0}}
        ).sort("last_crawl", DESCENDING).limit(24))
        
        items = []
        for comic in recent_comics:
            items.append({
                "_id": str(comic['_id']),
                "name": comic['name'],
                "slug": comic['slug'],
                "origin_name": comic.get('origin_name', []),
                "thumb_url": comic.get('thumb_url', ''),
                "updatedAt": comic.get('updatedAt'),
                "chapters_count": comic.get('chapters_count', 0),
                "category": comic.get('category', [])
            })
        
        data = {
            "seoOnPage": {
                "og_type": "website",
                "titleHead": "Trang chủ - ",
                "seoSchema": {
                    "@context": "https://schema.org",
                    "@type": "website",
                    "name": "Trang chủ - ",
                    "url": "https://otruyen.cc",
                    "image": "https://img.otruyenapi.com/uploads/comics/logo.png"
                },
                "descriptionHead": "Đọc truyện tranh online miễn phí",
                "og_image": ["comics/logo.png"],
                "updated_time": int(datetime.now().timestamp() * 1000),
                "og_url": ""
            },
            "breadCrumb": [
                {
                    "name": "Trang chủ",
                    "isCurrent": True,
                    "position": 1
                }
            ],
            "params": {
                "type_slug": "",
                "filterCategory": [],
                "filterCountry": [],
                "filterStatus": "",
                "sort": "",
                "crawl_check_url": ""
            },
            "items": items,
            "pagination": {
                "totalPage": 1,
                "currentPage": 1,
                "totalComics": len(items)
            },
            "APP_DOMAIN_CDN_IMAGE": "https://img.otruyenapi.com"
        }
        
        return create_success_response(data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/danh-sach/{type_slug}")
async def comic_list(
    type_slug: str,
    page: int = Query(1, ge=1),
    limit: int = Query(24, ge=1),
    sort: str = Query("new"),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """Danh sách truyện theo type"""
    try:
        # Build query
        query = {"chapters_count": {"$gt": 0}}
        
        # Filter by category if provided
        if category:
            query["category.slug"] = category
        
        # Filter by status if provided
        if status:
            query["status"] = status
        
        # Sort options
        sort_option = DESCENDING
        if sort == "new":
            sort_option = ("last_crawl", DESCENDING)
        elif sort == "az":
            sort_option = ("name", ASCENDING)
        elif sort == "update":
            sort_option = ("updatedAt", DESCENDING)
        
        # Calculate pagination
        total_comics = comics_collection.count_documents(query)
        total_pages = math.ceil(total_comics / limit)
        skip = (page - 1) * limit
        
        # Get comics
        comics = list(comics_collection.find(query)
            .sort([sort_option])
            .skip(skip)
            .limit(limit))
        
        items = []
        for comic in comics:
            items.append({
                "_id": str(comic['_id']),
                "name": comic['name'],
                "slug": comic['slug'],
                "origin_name": comic.get('origin_name', []),
                "thumb_url": comic.get('thumb_url', ''),
                "updatedAt": comic.get('updatedAt'),
                "chapters_count": comic.get('chapters_count', 0),
                "category": comic.get('category', [])
            })
        
        # Get type name
        type_names = {
            "truyen-moi": "Truyện Mới",
            "truyen-hot": "Truyện Hot",
            "truyen-full": "Truyện Full",
            "truyen-moi-cap-nhat": "Truyện Mới Cập Nhật"
        }
        
        type_name = type_names.get(type_slug, type_slug.replace("-", " ").title())
        
        data = {
            "seoOnPage": {
                "og_type": "website",
                "titleHead": f"{type_name} - ",
                "seoSchema": {
                    "@context": "https://schema.org",
                    "@type": "website",
                    "name": f"{type_name} - ",
                    "url": f"https://otruyen.cc/danh-sach/{type_slug}",
                    "image": "https://img.otruyenapi.com/uploads/comics/logo.png"
                },
                "descriptionHead": f"Danh sách {type_name}",
                "og_image": ["comics/logo.png"],
                "updated_time": int(datetime.now().timestamp() * 1000),
                "og_url": f"danh-sach/{type_slug}"
            },
            "breadCrumb": [
                {
                    "name": "Trang chủ",
                    "slug": "/",
                    "position": 1
                },
                {
                    "name": type_name,
                    "isCurrent": True,
                    "position": 2
                }
            ],
            "params": {
                "type_slug": type_slug,
                "filterCategory": [category] if category else [],
                "filterCountry": [],
                "filterStatus": status if status else "",
                "sort": sort,
                "crawl_check_url": ""
            },
            "items": items,
            "pagination": {
                "totalPage": total_pages,
                "currentPage": page,
                "totalComics": total_comics
            },
            "APP_DOMAIN_CDN_IMAGE": "https://img.otruyenapi.com"
        }
        
        return create_success_response(data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/the-loai")
async def get_categories():
    """Lấy danh sách thể loại"""
    try:
        categories = list(categories_collection.find().sort("name", ASCENDING))
        
        data = {
            "seoOnPage": {
                "og_type": "website",
                "titleHead": "Thể loại - ",
                "seoSchema": {
                    "@context": "https://schema.org",
                    "@type": "website",
                    "name": "Thể loại - ",
                    "url": "https://otruyen.cc/the-loai",
                    "image": "https://img.otruyenapi.com/uploads/comics/logo.png"
                },
                "descriptionHead": "Danh sách thể loại truyện tranh",
                "og_image": ["comics/logo.png"],
                "updated_time": int(datetime.now().timestamp() * 1000),
                "og_url": "the-loai"
            },
            "breadCrumb": [
                {
                    "name": "Trang chủ",
                    "slug": "/",
                    "position": 1
                },
                {
                    "name": "Thể loại",
                    "isCurrent": True,
                    "position": 2
                }
            ],
            "params": {
                "slug": "",
                "crawl_check_url": ""
            },
            "items": serialize_list(categories),
            "APP_DOMAIN_CDN_IMAGE": "https://img.otruyenapi.com"
        }
        
        return create_success_response(data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/the-loai/{category_slug}")
async def get_comics_by_category(
    category_slug: str,
    page: int = Query(1, ge=1)
):
    """Lấy truyện theo thể loại"""
    try:
        # Check if category exists
        category = categories_collection.find_one({"slug": category_slug})
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Build query
        query = {
            "chapters_count": {"$gt": 0},
            "category.slug": category_slug
        }
        
        # Pagination
        limit = 24
        total_comics = comics_collection.count_documents(query)
        total_pages = math.ceil(total_comics / limit)
        skip = (page - 1) * limit
        
        # Get comics
        comics = list(comics_collection.find(query)
            .sort("last_crawl", DESCENDING)
            .skip(skip)
            .limit(limit))
        
        items = []
        for comic in comics:
            items.append({
                "_id": str(comic['_id']),
                "name": comic['name'],
                "slug": comic['slug'],
                "origin_name": comic.get('origin_name', []),
                "thumb_url": comic.get('thumb_url', ''),
                "updatedAt": comic.get('updatedAt'),
                "chapters_count": comic.get('chapters_count', 0),
                "category": comic.get('category', [])
            })
        
        data = {
            "seoOnPage": {
                "og_type": "website",
                "titleHead": f"{category['name']} - ",
                "seoSchema": {
                    "@context": "https://schema.org",
                    "@type": "website",
                    "name": f"{category['name']} - ",
                    "url": f"https://otruyen.cc/the-loai/{category_slug}",
                    "image": "https://img.otruyenapi.com/uploads/comics/logo.png"
                },
                "descriptionHead": f"Truyện tranh thể loại {category['name']}",
                "og_image": ["comics/logo.png"],
                "updated_time": int(datetime.now().timestamp() * 1000),
                "og_url": f"the-loai/{category_slug}"
            },
            "breadCrumb": [
                {
                    "name": "Trang chủ",
                    "slug": "/",
                    "position": 1
                },
                {
                    "name": category['name'],
                    "isCurrent": True,
                    "position": 2
                }
            ],
            "params": {
                "slug": category_slug,
                "crawl_check_url": ""
            },
            "items": items,
            "pagination": {
                "totalPage": total_pages,
                "currentPage": page,
                "totalComics": total_comics
            },
            "APP_DOMAIN_CDN_IMAGE": "https://img.otruyenapi.com"
        }
        
        return create_success_response(data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/truyen-tranh/{comic_slug}")
async def get_comic_detail(comic_slug: str):
    """Lấy chi tiết truyện"""
    try:
        comic = comics_collection.find_one({"slug": comic_slug})
        if not comic:
            raise HTTPException(status_code=404, detail="Comic not found")
        
        comic_data = create_comic_response(comic)
        return create_success_response(comic_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tim-kiem")
async def search_comics(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1)
):
    """Tìm kiếm truyện"""
    try:
        # Build search query
        query = {
            "chapters_count": {"$gt": 0},
            "$or": [
                {"name": {"$regex": keyword, "$options": "i"}},
                {"origin_name": {"$regex": keyword, "$options": "i"}},
                {"slug": {"$regex": keyword, "$options": "i"}}
            ]
        }
        
        # Pagination
        limit = 24
        total_comics = comics_collection.count_documents(query)
        total_pages = math.ceil(total_comics / limit)
        skip = (page - 1) * limit
        
        # Get comics
        comics = list(comics_collection.find(query)
            .sort("last_crawl", DESCENDING)
            .skip(skip)
            .limit(limit))
        
        items = []
        for comic in comics:
            items.append({
                "_id": str(comic['_id']),
                "name": comic['name'],
                "slug": comic['slug'],
                "origin_name": comic.get('origin_name', []),
                "thumb_url": comic.get('thumb_url', ''),
                "updatedAt": comic.get('updatedAt'),
                "chapters_count": comic.get('chapters_count', 0),
                "category": comic.get('category', [])
            })
        
        data = {
            "seoOnPage": {
                "og_type": "website",
                "titleHead": f"Tìm kiếm: {keyword} - ",
                "seoSchema": {
                    "@context": "https://schema.org",
                    "@type": "website",
                    "name": f"Tìm kiếm: {keyword} - ",
                    "url": f"https://otruyen.cc/tim-kiem?keyword={keyword}",
                    "image": "https://img.otruyenapi.com/uploads/comics/logo.png"
                },
                "descriptionHead": f"Kết quả tìm kiếm cho: {keyword}",
                "og_image": ["comics/logo.png"],
                "updated_time": int(datetime.now().timestamp() * 1000),
                "og_url": f"tim-kiem?keyword={keyword}"
            },
            "breadCrumb": [
                {
                    "name": "Trang chủ",
                    "slug": "/",
                    "position": 1
                },
                {
                    "name": f"Tìm kiếm: {keyword}",
                    "isCurrent": True,
                    "position": 2
                }
            ],
            "params": {
                "keyword": keyword,
                "crawl_check_url": ""
            },
            "items": items,
            "pagination": {
                "totalPage": total_pages,
                "currentPage": page,
                "totalComics": total_comics
            },
            "APP_DOMAIN_CDN_IMAGE": "https://img.otruyenapi.com"
        }
        
        return create_success_response(data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chapter/{chapter_id}")
async def get_chapter_images(chapter_id: str):
    """Lấy ảnh của chapter (tương tự chapter_api_data)"""
    try:
        # Tìm chapter theo API URL hoặc ID
        chapter = chapters_collection.find_one({
            "$or": [
                {"chapter_api_url": {"$regex": chapter_id, "$options": "i"}},
                {"_id": ObjectId(chapter_id) if ObjectId.is_valid(chapter_id) else None}
            ]
        })
        
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        
        # Lấy domain CDN từ URL đầu tiên nếu có
        domain_cdn = "https://sv1.otruyencdn.com"
        if chapter.get('images'):
            first_image = chapter['images'][0]
            parsed_url = first_image['url'].split('/uploads/')[0]
            if parsed_url:
                domain_cdn = parsed_url
        
        data = {
            "domain_cdn": domain_cdn,
            "item": {
                "_id": str(chapter.get('_id', '')),
                "comic_name": chapter.get('comic_name', ''),
                "chapter_name": chapter.get('chapter_name', ''),
                "chapter_title": chapter.get('chapter_title', ''),
                "chapter_path": "",  # Not stored in our DB
                "chapter_image": [
                    {
                        "image_page": img.get('page', i+1),
                        "image_file": img.get('filename', f'page_{i+1}.jpg')
                    } for i, img in enumerate(chapter.get('images', []))
                ]
            }
        }
        
        return create_success_response(data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
