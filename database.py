from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, declarative_base

# تنظیم URL دیتابیس SQLite
DATABASE_URL = "sqlite:///soil_data.db"

# ایجاد engine برای اتصال به دیتابیس
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# ایجاد Base برای مدل‌ها
Base = declarative_base()

# تعریف مدل SoilData
class SoilData(Base):
    __tablename__ = "soil_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    pH = Column(Float, nullable=False)
    moisture = Column(Integer, nullable=False)
    nitrogen = Column(Integer, nullable=False)
    phosphorus = Column(Integer, nullable=False)
    potassium = Column(Integer, nullable=False)
    soil_type = Column(String, nullable=False)
    health_score = Column(Integer, nullable=False)  # ستون health_score
    status = Column(String, nullable=False)

# ایجاد جداول در دیتابیس (اگر وجود ندارند)
Base.metadata.create_all(bind=engine)

# ایجاد SessionLocal برای ارتباط با دیتابیس
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)