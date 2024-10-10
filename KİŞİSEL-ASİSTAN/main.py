from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
import cv2
import face_recognition
from deepface import DeepFace
import numpy as np
from models import save_user_to_db, get_all_users

app = Flask(__name__)
recognized_user = None
video_feed_active = True  # Video akışının kontrolü için bir bayrak

# Yüz tanıma için veritabanından kullanıcıları yükle
def load_known_faces():
    users = get_all_users()
    known_face_encodings = []
    known_face_names = []
    for name, face_encoding in users:
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)
    return known_face_encodings, known_face_names

known_face_encodings, known_face_names = load_known_faces()

# Global değişkenlere duygu durumu ekleyelim
recognized_user_emotion = None

def generate_frames():
    global recognized_user, recognized_user_emotion, video_feed_active
    cap = cv2.VideoCapture(0)  # Kamerayı aç

    while video_feed_active:
        success, frame = cap.read()  # Kameradan görüntü al
        if not success:
            break

        # Duygu analizi
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Renk formatını değiştir
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        if result:
            emotions = result[0]['emotion']
            dominant_emotion = max(emotions, key=emotions.get)
            recognized_user_emotion = dominant_emotion  # Tanınan kullanıcının duygu durumu sağ sol yuksrı aşağı gibi

            # Duygu metnini görüntüye yaz datasett
            cv2.putText(frame, f"Duygu: {dominant_emotion}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Yüz tanıma
        face_locations = face_recognition.face_locations(frame)#yüzün konumu burdabn bulunuyor
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        
        #yüzü veritabanıyla karşılaştırma
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Bilinmeyen"# eşleşme bulunmazsa

            # Tanınan yüzü kontrol ediyor ve eşleşme olursa yazıyorr
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                recognized_user = name  # Tanınan kullanıcının adını ayarlayın
                video_feed_active = False  # Video akışını durdur

            # Tanınan yüzün etrafında dikdörtgen çiz yeşill renklii
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
         
         #canlı video akışı
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()  # Video akışı durdurulduğunda kamerayı kapat

@app.route('/assistant')
def assistant():
    return render_template('assistant.html', user=recognized_user, emotion=recognized_user_emotion)



#canlı video akışı sonrsaı yönlendirme
@app.route('/video_feed')
def video_feed():
    global recognized_user, video_feed_active
    # Tanınan kullanıcı varsa yönlendirme işlemi
    if recognized_user:
        print(f"Tanınan kullanıcı yönlendiriliyor: {recognized_user}")  # Konsola yazdır
        temp_user = recognized_user  # Yönlendirme sonrası kullanılacak kullanıcı
        recognized_user = None  # Yönlendirmeden sonra tanınan kullanıcıyı sıfırla
        video_feed_active = False  # Video akışını durdur
        return redirect(url_for('assistant'))  # Sayfaya yönlendir
    else:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    #kontrolll
@app.route('/check_user')
def check_user():
    global recognized_user
    if recognized_user:
        return jsonify({"recognized": True})
    return jsonify({"recognized": False})



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  
    username = data.get('name')  
    # Kayıt işlemi için yüzü al
    cap = cv2.VideoCapture(0)
    success, frame = cap.read()
    cap.release()
    if success:
        # Yüzün özelliklerini çıkar
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_frame)
        if face_encodings:
            # Yüz bilgilerini veritabanına kaydet
            face_encoding = face_encodings[0]
            save_user_to_db(username, face_encoding)
            # Belleği güncelle (yeni kullanıcıyı ekle)
            known_face_encodings.append(face_encoding)
            known_face_names.append(username)
            return jsonify({"message": "Kayıt işlemi başarılı!"})
        else:
            return jsonify({"message": "Yüz tespit edilemedi."}), 400
    return jsonify({"message": "Kamera açılamadı."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)

