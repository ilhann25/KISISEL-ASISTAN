import pyodbc

def get_db_connection():
    try:
        # SQL Server bağlantısı için gerekli ayarlar
        connection = pyodbc.connect(
            'DRIVER={SQL Server};'        # SQL Server sürücüsü
            'SERVER=DESKTOP-BLTT0DI;'       # Sunucu adı/IP adresi
            'DATABASE=PersonFaceRecognitionDB;'  # Veritabanı adı
            'UID=Sa;'          # Kullanıcı adı
            'PWD=ilhan25;'                  # Şifre
        )
        print("Veritabanına başarıyla bağlandı.")
        return connection
    except pyodbc.Error as e:
        print(f"Veritabanı bağlantısında hata oluştu: {e}")
        return None

def create_users_table():
    try:
        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            # Kullanıcıların kaydedileceği tabloyu oluştur
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
                CREATE TABLE Users (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    Name NVARCHAR(100),
                    FaceEncoding VARBINARY(MAX)
                )
            ''')
            conn.commit()
            print("Users tablosu başarıyla oluşturuldu.")
            cursor.close()
            conn.close()
        else:
            print("Tablo oluşturulamadı, veritabanı bağlantısı başarısız.")
    except pyodbc.Error as e:
        print(f"Tablo oluşturma işleminde hata oluştu: {e}")
