#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import make_response
from flask import request
import pymysql.cursors
import threading
from random import randint
import json
import datetime
from datetime import time
from flask_cors import CORS, cross_origin

# Connect to the database
connection = pymysql.connect(host='160.153.128.9',
                             user='spss',
                             password='MehmetTas2517',
                             db='spssbitirme',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)  # database bilgileri

baglanti = connection.cursor()  # baglanti adlı nesnemizi oluşturduk

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/login', methods=[
    'POST'])  # post metodu ile 127.0.0.1:500/login şeklinde post isteği atarsak json formatında olmalı bu iste

def login():
    baglanti.execute('SELECT * FROM users WHERE email = %s AND password = %s', (request.json["mail"], request.json[
        "pass"]))  # json formatında mail ve pass gönderdik örnek: {"mail":mail, "pass":password} gerisi zaten sql sorgusu
    kullanici = baglanti.fetchone()
    if kullanici:
        msg = {"isSuccess": True, "data": kullanici}
    else:
        msg = {"isSuccess": False, "data": "HATALI ŞİFRE"}

    return jsonify(msg)

@app.route('/user/update', methods=['POST'])
def userupdate():
    print(request.json["id"])
    baglanti.execute(
        'UPDATE users SET user_name=%s, email=%s, phone=%s,il=%s, ilce=%s, adres=%s, tc=%s, dogumtarihi=%s WHERE id=%s',
        (request.json["adi"], request.json["mail"], request.json["telefon"], request.json["il"], request.json["ilce"],
         request.json["adres"], request.json["tc"], request.json["dogumtarihi"], request.json["id"]))
    baglanti.connection.commit()  # sql sorgusunu işlettikten sonra commit metodu ile databaseye kesinlikle işleneceğini söylüyoruz
    msg = 'İşlem Başarılı Bir Şekilde Saglandı'
    return jsonify({"isSuccess": True, "message": msg})


@app.route('/user/kullanici/sil', methods=['POST'])
def userDelete():
    baglanti.execute("DELETE FROM users WHERE id=%s", (request.json["id"]))
    baglanti.connection.commit()
    msg = 'İşlem Başarılı Bir Şekilde Saglandı'
    return jsonify({"isSuccess": True, "message": msg})


@app.route('/user/calisanEkle', methods=['POST'])
def kullaniciEkle():
    baglanti.execute('INSERT INTO users (user_name,company_name,phone,email,password,tc,il,ilce,adres,dogumtarihi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (
    request.json["adi"], request.json["sirket"], request.json["telefon"], request.json["mail"],
    request.json["sifre"], request.json["tc"], request.json["il"], request.json["ilce"], request.json["adres"], request.json["dogumtarihi"]))
    baglanti.connection.commit()  # sql sorgusunu işlettikten sonra commit metodu ile databaseye kesinlikle işleneceğini söylüyoruz
    msg = 'You have successfully registered!'
    return jsonify({"isSuccess": True, "message": msg})


@app.route('/user/degisiklikTalebi/ekle', methods=['POST'])
def degisiklikTalebi():
    baglanti.execute('INSERT INTO talepler (user_id,talep_tarih,normal_tarih,sebep) VALUES (%s, %s, %s,%s)', (
     request.json["userID"], request.json["talepTarihi"], request.json["normalTarih"], request.json["sebep"]
    ))
    baglanti.connection.commit()  # sql sorgusunu işlettikten sonra commit metodu ile databaseye kesinlikle işleneceğini söylüyoruz
    msg = 'You have successfully registered!'
    return jsonify({"isSuccess": True, "message": msg})

@app.route('/user/degisiklikTalebi/getir', methods=['POST'])
def izinKayitlar():
    baglanti.execute('SELECT * FROM talepler WHERE user_id=%s',(request.json["userID"]))
    izinKayitlar = baglanti.fetchall()  # sql sorgusunu işlettikten sonra commit metodu ile databaseye kesinlikle işleneceğini söylüyoruz
    if izinKayitlar:

        return jsonify({"isSuccess": True, "message": izinKayitlar})
    else:
        return jsonify({"isSuccess": False, "message": "Hiç Kullanıcı yok"})

@app.route('/user/degisiklikTalebi/guncelle', methods=['POST'])
def izinTalepGuncelle():
    baglanti.execute('UPDATE talepler SET isComplete=%s WHERE id=%s',(request.json["kod"], request.json["id"]))
    baglanti.connection.commit()  # sql sorgusunu işlettikten sonra commit metodu ile databaseye kesinlikle işleneceğini söylüyoruz
    msg = 'İşlem Başarılı Bir Şekilde Saglandı'
    return jsonify({"isSuccess": True, "message": msg})

@app.route('/admin/degisiklikTalebi/getir', methods=['POST'])
def adminİzinKayit():
    baglanti.execute('SELECT talepler.id,users.user_name,talep_tarih,normal_tarih,sebep,isComplete FROM talepler INNER JOIN users ON users.id=talepler.user_id WHERE isComplete=0')
    adminizinKayitlar = baglanti.fetchall()  # sql sorgusunu işlettikten sonra commit metodu ile databaseye kesinlikle işleneceğini söylüyoruz
    if adminizinKayitlar:

        return jsonify({"isSuccess": True, "message": adminizinKayitlar})
    else:
        return jsonify({"isSuccess": False, "message": "Hiç Kullanıcı yok"})



@app.route('/register', methods=['POST'])
def register():
    baglanti.execute('INSERT INTO users (user_name,company_name,phone,email,password) VALUES (%s, %s, %s, %s, %s)', (
    request.json["user_name"], request.json["company_name"], request.json["phone"], request.json["email"],
    request.json["password"]))
    baglanti.connection.commit()  # sql sorgusunu işlettikten sonra commit metodu ile databaseye kesinlikle işleneceğini söylüyoruz
    msg = 'You have successfully registered!'
    return jsonify({"isSuccess": True, "message": msg})


@app.route('/user/all', methods=['POST'])
def userall():
    baglanti.execute('SELECT * FROM users')
    kullanicilar = baglanti.fetchall()  # sql sorgusunu işlettikten sonra commit metodu ile databaseye kesinlikle işleneceğini söylüyoruz
    if kullanicilar:

        return jsonify({"isSuccess": True, "message": kullanicilar})
    else:
        return jsonify({"isSuccess": False, "message": "Hiç Kullanıcı yok"})


@app.route("/user/one", methods=['POST'])
@cross_origin()
def users():
    print(request.json["id"])
    baglanti.execute('SELECT * FROM users WHERE id = %s', (request.json["id"]))
    kullanici = baglanti.fetchone()
    if kullanici:
        print(kullanici)
        return jsonify({"isSuccess": True, "message": kullanici})
    else:
        return jsonify({"isSuccess": False, "message": "Kullanıcı yok"})


@app.route("/user/calisanlar", methods=['POST'])
def calisanlar():
    print("girdi")
    baglanti.execute('SELECT * FROM users WHERE isAdmin = 0')
    kullanici = baglanti.fetchall()
    if kullanici:
        return jsonify({"isSuccess": True, "message": kullanici})
    else:
        return jsonify({"isSuccess": False, "message": "Kullanıcı yok"})

@app.route("/user/yoneticiler", methods=['POST'])
def yoneticiler():
    print("girdi")
    baglanti.execute('SELECT * FROM users WHERE isAdmin = 1')
    kullanici = baglanti.fetchall()
    if kullanici:
        return jsonify({"isSuccess": True, "message": kullanici})
    else:
        return jsonify({"isSuccess": False, "message": "Kullanıcı yok"})

@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'HTTP 404 Error': 'The content you looks for does not exist. Please check your request.'}), 404)


def some_long_task1():
    # json formatında mail ve pass gönderdik örnek: {"mail":mail, "pass":password} gerisi zaten sql sorgusu
    baglanti.execute('SELECT * FROM users WHERE isAdmin = 0')
    kullanici = baglanti.fetchall()

    # time(hour = 0, minute = 0, second = 0)
    start_date = datetime.datetime(2020, 1, 1, 00, 00, 00)
    end_date = datetime.datetime(2020, 1, 7, 23, 59, 59)
    delta = datetime.timedelta(hours=1)

    while start_date <= end_date:
        print(start_date)
        start_date += delta
        for data in kullanici:
            calisiyor = randint(0, 1)
            baglanti.execute(
                'INSERT INTO plans (user_id, tarih_saat,isVisible) VALUES (%s, %s,%s)',
                (data["id"], start_date, calisiyor))
            # sql sorgusunu işlettikten sonra commit metodu ile databaseye kesinlikle işleneceğini söylüyoruz
            baglanti.connection.commit()
            # msg = 'You have successfully registered!'
            # return jsonify({"isSuccess": "true", "message": msg})

            threading.Timer(604800.0, some_long_task1).start()


if __name__ == '__main__':
    app.run(debug=True)  # !flask/bin/python
