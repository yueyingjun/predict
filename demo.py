from flask import Flask,request,render_template
import pandas as pd
data = pd.read_csv('./house_price.csv')
data1 = data.dropna()
data2 = pd.get_dummies(data1[['dist', 'floor']])
pd.set_option('display.max_columns', None)
data3 = data2.drop(['dist_shijingshan', 'floor_high'], axis=1)
data4 = pd.concat([data3, data1[['roomnum', 'halls', 'AREA', 'subway', 'school', 'price']]], axis=1)
from sklearn import linear_model
from sklearn.model_selection import train_test_split
x = data4.iloc[:, :-1]
y = data4.iloc[:, -1:]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
model = linear_model.LinearRegression().fit(x_train, y_train)


app=Flask(__name__)

@app.route("/",methods=["get"])
def index():
    return render_template("bootstrap.html")


#  1. 如果发送数据

#  2. 如何接受数据

#  3. 如何进一步处理数据
@app.route("/send",methods=["post"])
def send():
    print(request.form)
    arr=[0,0,0,0,0,0,0,0,0,0,0,0]
    # 处理城市的信息
    dist=request.form["dist"]
    if int(dist)==-1:
        pass
    else:
        arr[int(dist)]=1

    # 处理楼层的信息
    floor=request.form["floor"]
    if int(floor)==-1:
        pass
    else:
        arr[int(floor)]=1

    print(arr)

    # 获取多少室
    roomnum=request.form["roomnum"]

    arr[7]=int(roomnum)

    # 获取厅的数量
    halls=request.form["halls"]
    arr[8]=int(halls)

    # 房屋面积

    area = request.form["area"]
    arr[9] = int(area)
    print(arr)

    # 是否朝阳

    subway = request.form["subway"]
    arr[10] = int(subway)

    # 是否学区房
    school = request.form["school"]
    arr[11] = int(school)

    result = model.predict([arr])
    result = str(round(result[0][0], 2))



    return render_template("bootstrap.html",datas=result)

app.run(port=8888)