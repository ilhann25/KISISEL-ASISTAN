import numpy as np
from database import get_db_connection
import pyodbc

def save_user_to_db(name, face_encoding):
    """
    Kullanıcıyı veritabanına kaydeder.
    
    :param name: Kullanıcının adı
    :param face_encoding: Yüzün encoding değeri (numpy array)
    """
    try:
        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            
            # Numpy array'ini binary (VARBINARY) formatına dönüştür
            face_encoding_binary = face_encoding.tobytes()

            # SQL sorgusu ile veritabanına kullanıcı ekle
            query = "INSERT INTO Users (Name, FaceEncoding) VALUES (?, ?)"
            cursor.execute(query, (name, face_encoding_binary))
            conn.commit()
            print(f"{name} başarıyla veritabanına kaydedildi.")
            
            cursor.close()
            conn.close()
        else:
            print("Veritabanı bağlantısı başarısız olduğu için kullanıcı kaydedilemedi.")
    except pyodbc.Error as e:
        print(f"Kullanıcı kaydetme işleminde hata oluştu: {e}")

def get_all_users():
    """
    Tüm kullanıcıları veritabanından getirir ve kullanıcıların isimlerini ve yüz encoding'lerini döner.
    
    :return: Kullanıcıların isimleri ve yüz encoding'leri
    """
    try:
        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            
            # Tüm kullanıcıları çek
            query = "SELECT Name, FaceEncoding FROM Users"
            cursor.execute(query)
            
            users = []
            rows = cursor.fetchall()
            
            for row in rows:
                name = row.Name
                face_encoding_binary = row.FaceEncoding
                
                # Binary formatındaki yüz encoding'ini tekrar numpy array'e dönüştür
                face_encoding = np.frombuffer(face_encoding_binary, dtype=np.float64)
                
                users.append((name, face_encoding))
            
            cursor.close()
            conn.close()
            
            return users
        else:
            print("Veritabanı bağlantısı başarısız olduğu için kullanıcılar getirilemedi.")
            return []
    except pyodbc.Error as e:
        print(f"Kullanıcıları getirirken hata oluştu: {e}")
        return []

