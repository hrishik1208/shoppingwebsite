import pickle
import json
from flask import Flask, render_template, request, jsonify   
app = Flask(__name__,template_folder='templates')
myfile=open("S.txt","r")
Myfile=open("S1.txt","r")
price={"apple":50,"banana":17,"grapes":10,"coconut":15,"amul lassi":10,"amul paneer":400,"amul cheese spread":300,"amul taaza":50,"pencil":1,"bag":200,"bottle":180,"notebook":200,"shampoo":250,"oil":120,"soap":90,"face cream":160}
l=myfile.readline()
L=Myfile.readline()
if l=="":
    p=dict()
    
else:
    myfile=open("S.txt","rb")
    p=pickle.load(myfile)
myfile.close()
Myfile.close()
if L=="":
    P=dict()
else:
    Myfile=open("S1.txt","rb")
    P=pickle.load(Myfile)
Myfile.close()
@app.route("/")
def home():
    return render_template("home.html")        

@app.route("/order")
def order():
    return render_template("Input_Output.html")        

@app.route("/submitJSON", methods=["POST"])
def processJSON():
    global p
    global P
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)
    l1=jsonObj['list1']
    lst1=l1.split(',')
    l2=jsonObj['list2']
    lst2=l2.split(',')
    SUM=0
    j=0
    d=False
    for i in range((len(lst2))):
        lst2[i]=int(lst2[i])
    for i in lst1:
        if i in price:
            SUM+=price[i]*lst2[j]
            j+=1
        else:
            d=True
            break
    if d==False:
        for i in range((len(lst2))):
            if lst1[i] in p:
                p[lst1[i]]+=lst2[i]
            else:
                p[lst1[i]]=lst2[i]
        myfile=open("S.txt","wb")
        pickle.dump(p,myfile)
        myfile.close()
        myfile=open("S.txt","rb")
        p=pickle.load(myfile)
        myfile.close()
        
        Myfile=open("S1.txt","wb")
        P[SUM]=l1
        pickle.dump(P,Myfile)
        Myfile.close()
        Myfile=open("S1.txt","rb")
        P=pickle.load(Myfile)
        Myfile.close()
        n=open("p.txt","w")
        n.write(str(lst1)+"\n")
        n.write(str(lst2)+"\n")
        n.close()
        s="Order Saved in text file and "
        return str(s)+"Total order costs you about "+str(SUM)
    else:
        return "Order Cancelled Because One Of The items You Ordered Is Not Available "

@app.route("/view")
def view():
    myfile=open("S.txt","rb")
    p=pickle.load(myfile)
    myfile.close()
    return render_template("view.html",p=p)

@app.route("/sold")
def sold():
    return render_template("sold.html")

@app.route("/submitjSON", methods=["POST"])
def processjSON():
    global p

    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)
    l1=jsonObj['List1']
    lst1=l1.split(',')
    l2=jsonObj['List2']
    lst2=l2.split(',')
    for i in range((len(lst2))):
        lst2[i]=int(lst2[i])
    d=False
    for i in lst1:
        if i not in p:
            d=True
            break
    if d==False:
        for i in range((len(lst2))):
            if lst1[i] in p:
                if p[lst1[i]]>lst2[i]:
                    p[lst1[i]]-=lst2[i]
                else:
                    p[lst1[i]]=0
        myfile=open("S.txt","wb")
        pickle.dump(p,myfile)
        myfile.close()
        myfile=open("S.txt","rb")
        p=pickle.load(myfile)
        myfile.close()
        s="Items Removed From Stock Successfully"
        return str(s)
    else:
        return "Process Cancelled Because One Of The items You Tried To Remove Not Found"
@app.route("/policy")
def policy():
    return render_template("policy.html")

@app.route("/history")
def history():
    c=0
    d=0
    for i in P:
        c+=i
    return render_template("history.html",c=c,P=P,d=d)

if __name__=="__main__":
    app.run()
