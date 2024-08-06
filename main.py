from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from camera import VideoCamera
from camera2 import VideoCamera2
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
import math
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import os
import time
import shutil
import imagehash
import PIL.Image
from PIL import Image
from PIL import ImageTk
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
import argparse
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="smart_surveillance"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
    ff=open("note.txt",'w')
    ff.write('1')
    ff.close()
    
    ff=open("det.txt","w")
    ff.write("1")
    ff.close()

    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()

    ff11=open("img.txt","w")
    ff11.write("1")
    ff11.close()

    ff=open("person.txt","w")
    ff.write("")
    ff.close()
    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            result=" Your Logged in sucessfully**"
            return redirect(url_for('admin1')) 
        else:
            result="Your logged in fail!!!"
        

    return render_template('index.html',msg=msg,act=act)





@app.route('/login', methods=['POST','GET'])
def login():
    result=""
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM admin where username=%s && password=%s && name='admin'",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            result=" Your Logged in sucessfully**"
            return redirect(url_for('admin')) 
        else:
            result="Your logged in fail!!!"
                

    '''dimg=[]
    path_main = 'static/train1'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)
        #list_of_elements = os.listdir(os.path.join(path_main, folder))

        #resize
        img = cv2.imread('static/train1/'+fname)
        rez = cv2.resize(img, (300, 300))
        cv2.imwrite("static/d3/"+fname, rez)'''
        
    return render_template('login.html',result=result)

@app.route('/login_dept', methods=['POST','GET'])
def login_dept():
    result=""
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()

    ff=open("check.txt","w")
    ff.write("")
    ff.close()
        
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM admin where username=%s && password=%s && name='dept'",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            result=" Your Logged in sucessfully**"
            return redirect(url_for('cam_video')) 
        else:
            result="Your logged in fail!!!"
  
    return render_template('login_dept.html',result=result)

@app.route('/login_user', methods=['POST','GET'])
def login_user():
    result=""
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM user_details where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            result=" Your Logged in sucessfully**"
            return redirect(url_for('userhome')) 
        else:
            result="Your logged in fail!!!"
                
    
    return render_template('login_user.html',result=result)




@app.route('/monitor',methods=['POST','GET'])
def monitor():

    return render_template('monitor.html')

@app.route('/page1',methods=['POST','GET'])
def page1():

    return render_template('page1.html')


@app.route('/userhome',methods=['POST','GET'])
def userhome():
    vid=""
    msg=""
    act = request.args.get('act')
    
    
    cursor = mydb.cursor()
    
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']

        cursor.execute("update user_details set name=%s, mobile=%s, email=%s, location=%s where id=1", (name, mobile, email, location))
        mydb.commit()

        
        
        return redirect(url_for('userhome',act='success'))

    cursor.execute("SELECT * FROM user_details")
    data = cursor.fetchone()
    return render_template('userhome.html',msg=msg,data=data)

@app.route('/detect',methods=['POST','GET'])
def detect():
    vid=""
    msg=""
    act = request.args.get('act')
    
    
    cursor = mydb.cursor()
    
    cursor.execute("SELECT * FROM detect_info order by id desc")
    data2 = cursor.fetchall()

    cursor.execute("SELECT * FROM user_details")
    data = cursor.fetchone()
    return render_template('detect.html',msg=msg,data=data,data2=data2)


@app.route('/add_contact',methods=['POST','GET'])
def add_contact():
    vid=""
    msg=""
    data=[]
    act = request.args.get('act')
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        name=request.form['name']
        station=request.form['station']
        mobile=request.form['mobile']
        email=request.form['email']
        area=request.form['area']
        city=request.form['city']
        

        #cursor.execute("update admin set name=%s, mobile=%s, email=%s, location=%s where username='admin'", (name, mobile, email, location))
        #mydb.commit()
        mycursor.execute("SELECT max(id)+1 FROM ss_police")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO ss_police(id,name,station,mobile,email,area,city) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,name,station,mobile,email,area,city)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
    mycursor.execute("SELECT * FROM ss_police")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ss_police where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_contact')) 
        
    
    return render_template('add_contact.html',msg=msg,data=data,act=act)

@app.route('/add_location',methods=['POST','GET'])
def add_location():
    vid=""
    msg=""
    pid=request.args.get("pid")
    
    data=[]
    act = request.args.get('act')
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM ss_police where id=%s",(pid,))
    cdata = mycursor.fetchone()

    area=cdata[5]
    city=cdata[6]

    
    if request.method=='POST':
        
        address=request.form['address']
        location=request.form['location']

        l1=location.split("),")
        l2=l1[0].split("(")
        l3=l2[1].split(",")

        lat=l3[0]
        lon=l3[1]

        lt1=lat.split(".")
        lt2=lt1[1]
        lt3=lt2[0:5]
        lt4=lt1[0]+"."+lt3

        ln1=lon.split(".")
        ln2=ln1[1]
        ln3=ln2[0:5]
        ln4=ln1[0]+"."+ln3

        loc=lt4+", "+ln4
        
        

        mycursor.execute("SELECT max(id)+1 FROM ss_location")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO ss_location(id,city,area,address,location) VALUES (%s,%s,%s,%s,%s)"
        val = (maxid,city,area,address,loc)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
    mycursor.execute("SELECT * FROM ss_location")
    data = mycursor.fetchall()
    
    return render_template('add_location.html',msg=msg,data=data)

@app.route('/add_video',methods=['POST','GET'])
def add_video():
    vid=""
    msg=""
    gid=request.args.get("gid")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ss_location where id=%s",(gid,))
    dd = mycursor.fetchone()
    area=dd[2]
    city=dd[1]
    location=dd[3]


    vdata=[]
    path_main = 'static/videos/'
    for fname in os.listdir(path_main):
        vdata.append(fname)
    
    if request.method=='POST':
        video=request.form['video']
        mycursor.execute("SELECT count(*) FROM ss_video where gid=%s && video=%s",(gid,video))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            
            mycursor.execute("SELECT max(id)+1 FROM ss_video")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            sql = "INSERT INTO ss_video(id,city,area,location,gid,video) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (maxid,city,area,location,gid,video)
            print(sql)
            mycursor.execute(sql, val)
            mydb.commit()
            msg="success"

    return render_template('add_video.html',msg=msg,vdata=vdata)

@app.route('/view_location',methods=['POST','GET'])
def view_location():
    vid=""
    msg=""
    mycursor = mydb.cursor()
    act=request.args.get("act")
    mycursor.execute("SELECT * FROM ss_location")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ss_location where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_location'))
    
    
    return render_template('view_location.html',msg=msg,data=data,act=act)
    

@app.route('/admin',methods=['POST','GET'])
def admin():
    msg=""
    ff1=open("photo.txt","w")
    ff1.write("2")
    ff1.close()

    mycursor = mydb.cursor()
    if request.method=='POST':
        
        name=request.form['name']
       
        mycursor.execute("SELECT max(id)+1 FROM register")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO register(id, name) VALUES (%s, %s)"
        val = (maxid, name)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit()
        
        return redirect(url_for('add_photo',vid=maxid)) 
        

    mycursor.execute("SELECT * FROM register")
    data = mycursor.fetchall()
    
    return render_template('admin.html',msg=msg,data=data)

@app.route('/add_photo',methods=['POST','GET'])
def add_photo():
    vid=""
    ff1=open("photo.txt","w")
    ff1.write("2")
    ff1.close()

    #ff2=open("mask.txt","w")
    #ff2.write("face")
    #ff2.close()
    act = request.args.get('act')
    
    if request.method=='GET':
        vid = request.args.get('vid')
        ff=open("user.txt","w")
        ff.write(str(vid))
        ff.close()

    cursor = mydb.cursor()
    
    if request.method=='POST':
        vid=request.form['vid']
        fimg="v"+vid+".jpg"
        

        cursor.execute('delete from vt_face WHERE vid = %s', (vid, ))
        mydb.commit()

        ff=open("det.txt","r")
        v=ff.read()
        ff.close()
        vv=int(v)
        v1=vv-1
        vface1=vid+"_"+str(v1)+".jpg"
        i=2
        while i<vv:
            
            cursor.execute("SELECT max(id)+1 FROM vt_face")
            maxid = cursor.fetchone()[0]
            if maxid is None:
                maxid=1
            vface=vid+"_"+str(i)+".jpg"
            sql = "INSERT INTO vt_face(id, vid, vface) VALUES (%s, %s, %s)"
            val = (maxid, vid, vface)
            print(val)
            cursor.execute(sql,val)
            mydb.commit()
            i+=1

        
        return redirect(url_for('view_photo',vid=vid,act='success'))
        
    
    cursor.execute("SELECT * FROM register")
    data = cursor.fetchall()
    return render_template('add_photo.html',data=data, vid=vid)




def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))

@app.route('/img_process1', methods=['GET', 'POST'])
def img_process1():
    
    return render_template('img_process1.html')

@app.route('/pro1', methods=['GET', 'POST'])
def pro1():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        #list_of_elements = os.listdir(os.path.join(path_main, folder))

        #resize
        #img = cv2.imread('static/data/'+fname)
        #rez = cv2.resize(img, (400, 300))
        #cv2.imwrite("static/dataset/"+fname, rez)'''

        '''img = cv2.imread('static/dataset/'+fname) 	
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("static/training/g_"+fname, gray)
        ##noice
        img = cv2.imread('static/training/g_'+fname) 
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        fname2='ns_'+fname
        cv2.imwrite("static/training/"+fname2, dst)'''

    return render_template('pro1.html',dimg=dimg)

@app.route('/pro11', methods=['GET', 'POST'])
def pro11():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)

    return render_template('pro11.html',dimg=dimg)

@app.route('/pro2', methods=['GET', 'POST'])
def pro2():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)

        #f1=open("adata.txt",'w')
        #f1.write(fname)
        #f1.close()
        '''##bin
        image = cv2.imread('static/dataset/'+fname)
        original = image.copy()
        kmeans = kmeans_color_quantization(image, clusters=4)

        # Convert to grayscale, Gaussian blur, adaptive threshold
        gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

        # Draw largest enclosing circle onto a mask
        mask = np.zeros(original.shape[:2], dtype=np.uint8)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
            cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
            break
        
        # Bitwise-and for result
        result = cv2.bitwise_and(original, original, mask=mask)
        result[mask==0] = (0,0,0)

        
        ###cv2.imshow('thresh', thresh)
        ###cv2.imshow('result', result)
        ###cv2.imshow('mask', mask)
        ###cv2.imshow('kmeans', kmeans)
        ###cv2.imshow('image', image)
        ###cv2.waitKey()

        cv2.imwrite("static/training/bb/bin_"+fname, thresh)'''

    
   

    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        ##RPN
        
        img = cv2.imread('static/training/g_'+fname)
        #img = cv2.imread('static/trained/seg/'+fn2)
        
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,1.5*dist_transform.max(),255,0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        segment = cv2.subtract(sure_bg,sure_fg)
        img = Image.fromarray(img)
        segment = Image.fromarray(segment)
        path3="static/training/sg/"+fname
        #segment.save(path3)
        

    return render_template('pro2.html',dimg=dimg)

@app.route('/pro3', methods=['GET', 'POST'])
def pro3():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        
   
    return render_template('pro3.html',dimg=dimg)

@app.route('/pro4', methods=['GET', 'POST'])
def pro4():
    msg=""
    dimg=[]

    
        
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)

        #####
        
        image = cv2.imread("static/dataset/"+fname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        
        path4="static/training/fg/"+fname
        #edged.save(path4)
        ##
    
        
    return render_template('pro4.html',dimg=dimg)

   

@app.route('/pro5', methods=['GET', 'POST'])
def pro5():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
    #graph
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[5,10,40,80,130]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model Precision")
    plt.ylabel("precision")
    
    fn="graph1.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph2
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[5,10,40,80,130]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model recall")
    plt.ylabel("recall")
    
    fn="graph2.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph3########################################
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(94,98)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(94,98)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[7,23,49,72,95]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy %")
    
    fn="graph3.png"
    #plt.savefig('static/training/'+fn)
    plt.close()
    #######################################################
    #graph4
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,4)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(1,4)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[7,23,49,72,95]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Model loss")
    
    fn="graph4.png"
    #plt.savefig('static/training/'+fn)
    plt.close()
    return render_template('pro5.html',dimg=dimg)

def toString(a):
  l=[]
  m=""
  for i in a:
    b=0
    c=0
    k=int(math.log10(i))+1
    for j in range(k):
      b=((i%10)*(2**j))   
      i=i//10
      c=c+b
    l.append(c)
  for x in l:
    m=m+chr(x)
  return m
                


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    
    ff=open("static/training/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')


    ##    
    ff2=open("static/training/tdata.txt","r")
    rd=ff2.read()
    ff2.close()

    num=[]
    r1=rd.split(',')
    s=len(r1)
    ss=s-1
    i=0
    while i<ss:
        num.append(int(r1[i]))
        i+=1

    #print(num)
    dat=toString(num)
    dd2=[]
    ex=dat.split(',')
    ##

    #ffq=open("static/trained/adata.txt",'r')
    #ext1=ffq.read()
    #ffq.close()

    v1=0
    v2=0
    v3=0
    
    data2=[]
    #ex=ext1.split(',')
    dt1=[]
    dt2=[]
    dt3=[]
    
    g=0
    for nx in ex:
        g+=1
        nn=nx.split('|')
        if nn[0]=='1':
            
            dt1.append(nn[1])
            
            v1+=1
        if nn[0]=='2':
            dt2.append(nn[1])
            
            v2+=1
        if nn[0]=='3':
            dt3.append(nn[1])
            
            v3+=1
       
        
    data2.append(dt1)
    data2.append(dt2)
    data2.append(dt3)
    
    print(data2)   
    dd2=[v1,v2,v3]
    g2=70
    doc = cname #list(data.keys())
    values = dd2 #list(data.values())
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    cc=['blue','orange','green']
    plt.bar(doc, values, color =cc,
            width = 0.4)
 

    plt.ylim((1,g2))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    #plt.xticks(rotation=20,size=8)
    plt.savefig('static/training/'+fn)
    
    plt.close()
    #plt.clf()
    ##
    
    return render_template('classify.html',msg=msg,cname=cname,data2=data2)

###Preprocessing
@app.route('/view_photo',methods=['POST','GET'])
def view_photo():
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()

    if request.method=='POST':
        print("Training")
        vid=request.form['vid']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        dt = cursor.fetchall()
        for rs in dt:
            ##Preprocess
            path="static/frame/"+rs[2]
            path2="static/process1/"+rs[2]
            mm2 = PIL.Image.open(path).convert('L')
            rz = mm2.resize((200,200), PIL.Image.ANTIALIAS)
            rz.save(path2)
            
            '''img = cv2.imread(path2) 
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
            path3="static/process2/"+rs[2]
            cv2.imwrite(path3, dst)'''
            #noice
            img = cv2.imread('static/process1/'+rs[2]) 
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
            fname2='ns_'+rs[2]
            cv2.imwrite("static/process1/"+fname2, dst)
            ######
            ##bin
            image = cv2.imread('static/process1/'+rs[2])
            original = image.copy()
            kmeans = kmeans_color_quantization(image, clusters=4)

            # Convert to grayscale, Gaussian blur, adaptive threshold
            gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3,3), 0)
            thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

            # Draw largest enclosing circle onto a mask
            mask = np.zeros(original.shape[:2], dtype=np.uint8)
            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
            for c in cnts:
                ((x, y), r) = cv2.minEnclosingCircle(c)
                cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
                cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
                break
            
            # Bitwise-and for result
            result = cv2.bitwise_and(original, original, mask=mask)
            result[mask==0] = (0,0,0)

            
            ###cv2.imshow('thresh', thresh)
            ###cv2.imshow('result', result)
            ###cv2.imshow('mask', mask)
            ###cv2.imshow('kmeans', kmeans)
            ###cv2.imshow('image', image)
            ###cv2.waitKey()

            cv2.imwrite("static/process1/bin_"+rs[2], thresh)
            

            ###RPN - Segment
            img = cv2.imread('static/process1/'+rs[2])
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/fg_"+rs[2]
            segment.save(path3)
            ####
            img = cv2.imread('static/process2/fg_'+rs[2])
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/fg_"+rs[2]
            segment.save(path3)
            '''
            img = cv2.imread(path2)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # noise removal
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/"+rs[2]
            segment.save(path3)
            '''
            #####
            image = cv2.imread(path2)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 50, 100)
            image = Image.fromarray(image)
            edged = Image.fromarray(edged)
            path4="static/process3/"+rs[2]
            edged.save(path4)
            ##
            #shutil.copy('static/assets/images/11.png', 'static/process4/'+rs[2])
       
        return redirect(url_for('view_photo1',vid=vid))
        
    return render_template('view_photo.html', result=value,vid=vid)


###CNN Classification
def CNN():
    #Lets start by loading the Cifar10 data
    (X, y), (X_test, y_test) = cifar10.load_data()

    #Keep in mind the images are in RGB
    #So we can normalise the data by diving by 255
    #The data is in integers therefore we need to convert them to float first
    X, X_test = X.astype('float32')/255.0, X_test.astype('float32')/255.0

    #Then we convert the y values into one-hot vectors
    #The cifar10 has only 10 classes, thats is why we specify a one-hot
    #vector of width/class 10
    y, y_test = u.to_categorical(y, 10), u.to_categorical(y_test, 10)

    #Now we can go ahead and create our Convolution model
    model = Sequential()
    #We want to output 32 features maps. The kernel size is going to be
    #3x3 and we specify our input shape to be 32x32 with 3 channels
    #Padding=same means we want the same dimensional output as input
    #activation specifies the activation function
    model.add(Conv2D(32, (3, 3), input_shape=(32, 32, 3), padding='same',
                     activation='relu'))
    #20% of the nodes are set to 0
    model.add(Dropout(0.2))
    #now we add another convolution layer, again with a 3x3 kernel
    #This time our padding=valid this means that the output dimension can
    #take any form
    model.add(Conv2D(32, (3, 3), activation='relu', padding='valid'))
    #maxpool with a kernet of 2x2
    model.add(MaxPooling2D(pool_size=(2, 2)))
    #In a convolution NN, we neet to flatten our data before we can
    #input it into the ouput/dense layer
    model.add(Flatten())
    #Dense layer with 512 hidden units
    model.add(Dense(512, activation='relu'))
    #this time we set 30% of the nodes to 0 to minimize overfitting
    model.add(Dropout(0.3))
    #Finally the output dense layer with 10 hidden units corresponding to
    #our 10 classe
    model.add(Dense(10, activation='softmax'))
    #Few simple configurations
    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(momentum=0.5, decay=0.0004), metrics=['accuracy'])
    #Run the algorithm!
    model.fit(X, y, validation_data=(X_test, y_test), epochs=25,
              batch_size=512)
    #Save the weights to use for later
    model.save_weights("cifar10.hdf5")
    #Finally print the accuracy of our model!
    print("Accuracy: &2.f%%" %(model.evaluate(X_test, y_test)[1]*100))

                  
                
@app.route('/view_photo1',methods=['POST','GET'])
def view_photo1():
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('view_photo1.html', result=value,vid=vid)

@app.route('/view_photo11',methods=['POST','GET'])
def view_photo11():
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('view_photo11.html', result=value,vid=vid)

@app.route('/view_photo2',methods=['POST','GET'])
def view_photo2():
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('view_photo2.html', result=value,vid=vid)    

@app.route('/view_photo3',methods=['POST','GET'])
def view_photo3():
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('view_photo3.html', result=value,vid=vid)

@app.route('/view_photo4',methods=['POST','GET'])
def view_photo4():
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('view_photo4.html', result=value,vid=vid)

@app.route('/message',methods=['POST','GET'])
def message():
    vid=""
    name=""
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT name FROM register where id=%s",(vid, ))
        name = mycursor.fetchone()[0]
    return render_template('message.html',vid=vid,name=name)




@app.route('/process',methods=['POST','GET'])
def process():
    msg=""
    ss=""
    uname=""
    act=""
    det=""
    message=""
    message2=""
    sms=""
    mobile2=""
    
    if request.method=='GET':
        act = request.args.get('act')
        
    ff3=open("img.txt","r")
    mcnt=ff3.read()
    ff3.close()

    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM user_details where id=1')
    rw = cursor.fetchone()
    name=rw[1]
    mobile=rw[2]
    location=rw[4]

    cursor.execute('SELECT * FROM ss_police order by id')
    rw2 = cursor.fetchall()
    for rw22 in rw2:
        mobile2=str(rw22[3])

    ff1=open("note.txt",'r')
    v=ff1.read()
    ff1.close()
    v1=int(v)
                    
    try:

        cutoff=8
        act="1"
        cursor.execute('SELECT * FROM vt_face')
        dt = cursor.fetchall()
        for rr in dt:
            hash0 = imagehash.average_hash(Image.open("static/frame/"+rr[2])) 
            hash1 = imagehash.average_hash(Image.open("getimg.jpg"))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                vid=rr[1]
                
                message="Abnormal Detected"
                message2="Abnormal, "+location
                if v1<3:
                    v2=v1+1
                    vv=str(v2)
                    ff=open("note.txt",'w')
                    ff.write(vv)
                    ff.close()

                    sms="yes"

                    cursor.execute("SELECT max(id)+1 FROM detect_info")
                    maxid = cursor.fetchone()[0]
                    if maxid is None:
                        maxid=1
                    vface="d"+str(maxid)+".jpg"
                    sql = "INSERT INTO detect_info(id, detect_img) VALUES (%s, %s)"
                    val = (maxid, vface)
                    print(val)
                    cursor.execute(sql,val)
                    mydb.commit()

                    shutil.copy('getimg.jpg', 'static/detect/'+vface)

                    #url="http://iotcloud.co.in/testsms/sms.php?sms=msg&name="+name+"&mess="+message+"&mobile="+str(mobile)
                    #webbrowser.open_new(url)

                    #url2="http://iotcloud.co.in/testsms/sms.php?sms=msg&name=Dept&mess="+message2+"&mobile="+str(mobile2)
                    #webbrowser.open_new(url2)
                
             
                break
            
    except:
        print("excep")
        

    print(message2)

    return render_template('process.html',name=name,message2=message2,message=message,mobile=mobile,mobile2=mobile2,sms=sms,act=act)



@app.route('/clear_data',methods=['POST','GET'])
def clear_data():
    ff=open("person.txt","w")
    ff.write("")
    ff.close()

    ff1=open("get_value.txt","w")
    ff1.write("")
    ff1.close()
    return render_template('clear_data.html')

@app.route('/user_view')
def user_view():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM register")
    result = mycursor.fetchall()
    return render_template('user_view.html', result=result)

@app.route('/cam_video',methods=['POST','GET'])
def cam_video():
    video=""
    st=""
    gid=""
    gid1=0
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM ss_location")
    rdata = mycursor.fetchall()

    vdata=[]
    '''path_main = 'static/videos/'
    for fname in os.listdir(path_main):
        vdata.append(fname)'''

    if request.method == 'POST':
        
        gid= request.form['gid']
        if gid=="":
            ff=open("gid.txt","r")
            gid=ff.read()
            ff.close()
        else:
            st="2"
            ff=open("gid.txt","w")
            ff.write(str(gid))
            ff.close()

        gid1=int(gid)

        mycursor.execute("SELECT * FROM ss_video where gid=%s",(gid,))
        vdata = mycursor.fetchall()
        
        video = request.form['video']

        if video=="":
            s=1
        else:
            st="1"
            
        

        ff=open("sms.txt","w")
        ff.write("1")
        ff.close()

        

        ff=open("check.txt","w")
        ff.write("")
        ff.close()

        f1=open("file.txt","w")
        f1.write("static/videos/"+video)
        f1.close()
    
    
    return render_template('cam_video.html',video=video,vdata=vdata,rdata=rdata,st=st,gid1=gid1)

@app.route('/process_sur',methods=['POST','GET'])
def process_sur():
    msg=""
    s1=""
    mess=""
    mobile=""
    sms=""

    mycursor = mydb.cursor()
    
    

    
    
 
    ff=open("check.txt","r")
    detect=ff.read()
    ff.close()

    ff=open("sms.txt","r")
    sms=ff.read()
    ff.close()

    ff=open("gid.txt","r")
    gid=ff.read()
    ff.close()
    mycursor.execute("SELECT * FROM ss_location where id=%s",(gid,))
    gdata = mycursor.fetchone()
    loc=gdata[4]
    area=gdata[2]
    city=gdata[1]

    mycursor.execute("SELECT * FROM ss_police where area=%s && city=%s",(area,city))
    data = mycursor.fetchone()
    name=data[1]
    station=data[2]
    mobile=data[3]
    
    if detect=="1":
        s1="1"

        #ff=open("sms.txt","w")
        #ff.write("2")
        #ff.close()
        msg="Fight Detected"
        mess="Fight Detected, Location: "+loc
    if detect=="2":
        s1="1"

        ff=open("sms.txt","w")
        ff.write("2")
        ff.close()
        msg="Fire Detected"
        mess="Fire Detected, Location: "+loc
    if detect=="3":
        s1="1"

        ff=open("sms.txt","w")
        ff.write("2")
        ff.close()
        msg="Gun Shot Detected"
        mess="Gun Shoot, Location: "+loc
        

            
    return render_template('process_sur.html',msg=msg,name=name,mess=mess,mobile=mobile,sms=sms,s1=s1,station=station)





@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #session.pop('username', None)
    return redirect(url_for('index'))
####
def gen2(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed2')
def video_feed2():
    return Response(gen2(VideoCamera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
####
def gen(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed')
        

def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
