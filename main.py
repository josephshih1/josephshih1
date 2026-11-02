pip install fastapi uvicorn sqlalchemy scikit-learn pandas numpy
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. 資料庫連線設定 (示範使用 SQLite，正式環境可換成 PostgreSQL)
DATABASE_URL = "sqlite:///./music.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. SQLAlchemy 資料庫模型
class SongModel(Base):
    __tablename__ = "songs"
    song_id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    artist_name = Column(String, index=True)
    danceability = Column(Float)
    energy = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)

Base.metadata.create_all(bind=engine)

# 3. Pydantic 傳輸模型 (API 輸出格式)
class SongResponse(BaseModel):
    song_id: str
    title: str
    artist_name: str
    danceability: float
    energy: float
    
    class Config:
        orm_mode = True

app = FastAPI(
    title="Music Search & Recommendation API",
    description="結合 MSD 與 Spotify 特徵的音樂搜尋與推薦系統",
    version="1.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# 1. 音樂搜尋 API
# ==========================================
@app.get("/search", response_model=list[SongResponse], summary="搜尋歌曲（依歌名或歌手）")
def search_songs(
    q: str = Query(..., description="搜尋關鍵字，例如：Taylor Swift 或 Song A"), 
    db: Session = Depends(get_db)
):
    # 透過 ilike 進行不分大小寫的模糊搜尋
    results = db.query(SongModel).filter(
        (SongModel.title.ilike(f"%{q}%")) | (SongModel.artist_name.ilike(f"%{q}%"))
    ).limit(10).all()
    
    return results


# ==========================================
# 2. 音樂推薦演算法 API (Content-based)
# ==========================================
@app.get("/recommend/{song_id}", response_model=list[SongResponse], summary="基於音訊特徵推薦相似歌曲")
def recommend_songs(
    song_id: str, 
    top_n: int = Query(5, description="推薦回傳的歌曲數量"), 
    db: Session = Depends(get_db)
):
    # 步驟 A：檢查目標歌曲是否存在
    target_song = db.query(SongModel).filter(SongModel.song_id == song_id).first()
    if not target_song:
        raise HTTPException(status_code=404, detail="找不到指定的歌曲 ID")
    
    # 步驟 B：取得資料庫中所有歌曲
    all_songs = db.query(SongModel).all()
    if len(all_songs) <= 1:
        return []
    
    # 步驟 C：建立音訊特徵矩陣
    features = ['danceability', 'energy', 'valence', 'tempo']
    song_ids = [s.song_id for s in all_songs]
    
    # 處理缺失值並轉為 NumPy 矩陣
    matrix = np.array([[getattr(s, f) if getattr(s, f) is not None else 0.0 for f in features] for s in all_songs])
    
    # 步驟 D：計算餘弦相似度 (Cosine Similarity)
    target_idx = song_ids.index(song_id)
    similarity_scores = cosine_similarity([matrix[target_idx]], matrix)[0]
    
    # 步驟 E：排序並排除自己，取出前 N 名
    similar_indices = np.argsort(similarity_scores)[::-1]
    recommended_indices = [idx for idx in similar_indices if idx != target_idx][:top_n]
    
    # 組裝推薦清單
    recommendations = [all_songs[idx] for idx in recommended_indices]
    return recommendations
