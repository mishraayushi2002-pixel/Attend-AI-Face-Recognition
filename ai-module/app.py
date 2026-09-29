import os, json, uuid
from datetime import datetime, timezone
from pathlib import Path
import cv2
import face_recognition
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from scipy.ndimage import sobel

app=Flask(__name__); CORS(app)
ENCODINGS=Path(os.getenv('ENCODINGS_DIR','encodings')); ENCODINGS.mkdir(parents=True,exist_ok=True)
TOLERANCE=float(os.getenv('FACE_RECOGNITION_TOLERANCE','0.50'))
def load_image(file):
    raw=np.frombuffer(file.read(),np.uint8); bgr=cv2.imdecode(raw,cv2.IMREAD_COLOR)
    if bgr is None: raise ValueError('Invalid image')
    return bgr,cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
def analyze(rgb,bgr,location):
    top,right,bottom,left=location; face=bgr[top:bottom,left:right]; gray=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
    blur=float(cv2.Laplacian(gray,cv2.CV_64F).var()); texture=float(np.mean(np.hypot(sobel(gray,0),sobel(gray,1)))); area=(bottom-top)*(right-left)/(bgr.shape[0]*bgr.shape[1])
    landmarks=face_recognition.face_landmarks(rgb,[location]); eye_score=0.0
    if landmarks:
        pts=landmarks[0].get('left_eye',[])+landmarks[0].get('right_eye',[])
        eye_score=float(np.std([p[1] for p in pts])) if pts else 0.0
    quality=min(1,blur/180); texture_score=min(1,texture/35); size_score=min(1,area/.12); landmark_score=min(1,eye_score/4)
    score=.35*quality+.3*texture_score+.2*size_score+.15*landmark_score
    reasons=[]
    if blur<35: reasons.append('Image too blurred')
    if texture<8: reasons.append('Low texture suggests a screen or print')
    if area<.025: reasons.append('Move closer to the camera')
    if not landmarks: reasons.append('Facial landmarks are not clear')
    return score, reasons
def saved():
    result=[]
    for p in ENCODINGS.glob('*.json'):
        try:
            data=json.loads(p.read_text()); result.append((data['studentId'],data.get('rollNumber'),np.array(data['encoding'])))
        except Exception: continue
    return result
@app.get('/health')
def health(): return jsonify(status='ok',service='Face Recognition AI',studentsLoaded=len(saved()),timestamp=datetime.now(timezone.utc).isoformat())
@app.get('/stats')
def stats(): return jsonify(success=True,studentsLoaded=len(saved()),tolerance=TOLERANCE)
@app.post('/train')
def train():
    student_id=request.form.get('studentId'); files=request.files.getlist('images')
    if not student_id or not 5<=len(files)<=10:return jsonify(success=False,message='Student ID and 5–10 images are required'),422
    encodings=[]; rejected=[]
    for idx,file in enumerate(files):
        try:
            bgr,rgb=load_image(file); locations=face_recognition.face_locations(rgb,model=os.getenv('DETECTION_MODEL','hog'))
            if len(locations)!=1: rejected.append({'image':idx,'reason':'Exactly one face is required'}); continue
            score,reasons=analyze(rgb,bgr,locations[0])
            if score<.25: rejected.append({'image':idx,'reason':', '.join(reasons)}); continue
            values=face_recognition.face_encodings(rgb,locations)[0]; encodings.append(values)
        except Exception as exc: rejected.append({'image':idx,'reason':str(exc)})
    if len(encodings)<3:return jsonify(success=False,message='Not enough usable face samples',rejected=rejected),422
    # Medoid-style outlier rejection followed by mean encoding provides a stable profile.
    matrix=np.vstack(encodings); center=np.median(matrix,axis=0); distances=np.linalg.norm(matrix-center,axis=1); keep=matrix[distances<=np.percentile(distances,80)]
    encoding=np.mean(keep,axis=0); ref=f'{student_id}.json'; (ENCODINGS/ref).write_text(json.dumps({'studentId':student_id,'encoding':encoding.tolist(),'samples':len(keep),'trainedAt':datetime.now(timezone.utc).isoformat()}))
    return jsonify(success=True,encodingRef=ref,accepted=len(keep),rejected=rejected)
@app.post('/recognize')
def recognize():
    if 'image' not in request.files:return jsonify(recognized=False,livenessDetected=False,reason='Image required'),422
    try:
        bgr,rgb=load_image(request.files['image']); locations=face_recognition.face_locations(rgb,model=os.getenv('DETECTION_MODEL','hog'))
        if len(locations)!=1:return jsonify(recognized=False,livenessDetected=False,livenessScore=0,reason='No face found' if not locations else 'Multiple faces detected')
        live,reasons=analyze(rgb,bgr,locations[0]); threshold=float(os.getenv('LIVENESS_THRESHOLD','.38'))
        if live<threshold:return jsonify(recognized=False,livenessDetected=False,livenessScore=round(live,3),reason=', '.join(reasons) or 'Liveness check failed')
        probe=face_recognition.face_encodings(rgb,locations)[0]; known=saved()
        if not known:return jsonify(recognized=False,livenessDetected=True,livenessScore=round(live,3),reason='No registered faces')
        distances=face_recognition.face_distance([x[2] for x in known],probe); index=int(np.argmin(distances)); d=float(distances[index]); confidence=max(0,min(1,1-d))
        if d>TOLERANCE:return jsonify(recognized=False,livenessDetected=True,livenessScore=round(live,3),confidence=round(confidence,3),reason='Face not recognized')
        return jsonify(recognized=True,studentId=known[index][0],rollNumber=known[index][1],confidence=round(confidence,3),livenessDetected=True,livenessScore=round(live,3),reason='Match verified')
    except Exception as exc:return jsonify(recognized=False,livenessDetected=False,reason=str(exc)),422
@app.delete('/delete-encoding/<student_id>')
def delete(student_id):
    path=ENCODINGS/f'{student_id}.json'
    if path.exists():path.unlink()
    return jsonify(success=True)
if __name__=='__main__':app.run(host='0.0.0.0',port=5001)
