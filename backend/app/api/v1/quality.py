import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.core.database import get_db
from app.core.config import settings
from app.models.quality import FoodQualityAssessment
from app.schemas.quality import QualityAssessmentResponse
from app.ml.quality_classifier import quality_classifier

router = APIRouter()

@router.post("/assess-image")
async def assess_food_image(
    file: UploadFile = File(...),
    item_name: str = Form("Prepared Food Sample"),
    kitchen_id: Optional[int] = Form(1),
    db: Session = Depends(get_db)
):
    # Validate extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, and WebP images are supported")

    filename = f"quality_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    save_path = os.path.join(settings.UPLOAD_DIR, filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run ML computer vision analysis
    analysis = quality_classifier.analyze_image(save_path, item_name=item_name)

    # Store in database
    record = FoodQualityAssessment(
        kitchen_id=kitchen_id,
        item_name=item_name,
        image_path=f"/uploads/{filename}",
        visual_quality_category=analysis["visual_quality_category"],
        confidence_score=analysis["confidence_score"],
        detected_features=analysis["detected_features"],
        requires_human_inspection=analysis["requires_human_inspection"],
        human_verifier_notes=analysis["human_verifier_notes"],
        is_redistribution_approved=analysis["is_redistribution_approved"],
        safety_disclaimer=analysis["safety_disclaimer"]
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return record

@router.get("/history", response_model=List[QualityAssessmentResponse])
def get_quality_assessments(kitchen_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(FoodQualityAssessment)
    if kitchen_id:
        query = query.filter(FoodQualityAssessment.kitchen_id == kitchen_id)
    return query.order_by(FoodQualityAssessment.assessed_at.desc()).limit(30).all()
