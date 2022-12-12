from flask import Flask, render_template, url_for, request, redirect, flash,session, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import json
import pdfkit
app=Flask( __name__ )
app.secret_key='BAD_SECRET_KEY'
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tco.db'
# db=SQLAlchemy(app)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

component_list=['Pump','Compressor','Baseplate','Driver','Coupling','Supply System','Fluid Coupling','VFD','Lube Oil System','Transformer','Harmonic Filter','Instruments','Fan','Mixer','Diesel','Turbine','Cabinet','Others']
main_eq=['Pump','Compressor','Fan','Mixer']
dr_eq=['Electric motor','Diesel','Turbine']
el_eq=['VFD','Transformer','Harmonic Filter','Cabinet','Instruments','Junction box']
ot_eq=['Baseplate','Gearbox','Supply System','Coupling','Fluid Coupling','Lube Oil System','Others']
non_eq=['Testing','QA requirements','Freight charges']
configurations=['Direct Drive Pump','VFD Drive Pump','Fluidcoupling Type']
energy_price=0.04
annual_increase=1.5

n1=1
n2=1
n3=0
# capexy=0


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('form_page'))


#Главная страница формы
@app.route('/', methods=['POST','GET'])
@app.route('/form_page', methods=['POST','GET'])
def form_page():
    if not "info" in session:
        session["info"] = []
    if not "energie" in session:
        session["energie"] = 0
    if not "capexy" in session:
        session["capexy"] = 0
    if not "user_components" in session:
        session["user_components"] = []
    if not "user_maintenances" in session:
        session["user_maintenances"] = []
    if not "user_points" in session:
        session["user_points"] = []
    if not "currency" in session:
        session["currency"] = '$'
    if not "project_name" in session:
        session["project_name"] = 'Project 1'
    if not "unit_name" in session:
        session["unit_name"] = 'P-001'
    if not "number_years" in session:
        session["number_years"] = 30
    if not "main" in session:
        session["main"] = 0
    for i in range(len(session["user_components"])):
        session["user_components"][i][3] = i
    for y in range(len(session["user_maintenances"])):
        session["user_maintenances"][y][4] = y
    for z in range(len(session["user_points"])):
        session["user_points"][z][5] = z
    component=0
    component_price=0
    comments=0
    # maintenances = Maintenance.query.all()
    main_type = 0
    period = 0
    main_price = 0
    main_comments=0
    i=0
    j=0
    m=0
    message=''
    sum=0
    #points = Point.query.all()
    for i in range(len(session["user_points"])):
        sum+=session["user_points"][i][5]
    if sum<12:
        message='Please note that sum of scenarios for all points should be 12 (months)'
    elif sum>12:
        message='Sum of scenarios is more than 12 (months)!'

    k=0
    eff_driver = 0
    eff_other = 0
    power_pump = 0
    power_aux = 0
    scenario = 0
    a=0

    #Capex module
    total_capex_direct=0
    direct=[]
    if session["user_components"] != []:
        for i in range(len(session["user_components"])):
            total_capex_direct+=int(session["user_components"][i][1])
            direct.append(int(session["user_components"][i][1]))
        session["capexy"]=total_capex_direct
        labels=[]

        for j in range(len(session["user_components"])):
            labels.append(session["user_components"][j][0])
        labels.append('total_capex')

        labels.pop()
        sizes = direct
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels,shadow=False, startangle=90,autopct='%1.0f%%')
        plt.title("CAPEX for "+session["unit_name"])
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        fig1.set_size_inches(6.8, 4.8)
        plt.show()
        plt.savefig('static/capex2.png')
    #end of CAPEX module

#Maintetnce module
    prices = []
    per = []
    for maintenance in session["user_maintenances"]:
        prices.append(int(maintenance[2]))
        per.append(int(maintenance[1]))

    n = int(session["number_years"])
    i = 0
    x = 0
    mains = []
    while i <= n:
        for j in range(len(per)):
            if i % per[j] == 0 and i>0:
                x += prices[j] * (1 + (float(annual_increase) / 100)) ** i
        mains.append(round(x))
        i += 1

    session["main"] = mains[-1]
    a = np.array(mains)
    #     b = np.array(main_vfd)
    plt.switch_backend('agg')
    plt.plot(a, label='Costs')
    #     plt.plot(b, label='VFD')
    plt.title('Mainenance Cost for ' + session["unit_name"])
    plt.xlabel('Year')
    plt.ylabel('Maintenance Cost, ' + session["currency"])
    plt.legend()
    plt.grid()
    plt.xticks(np.arange(0, n+1, 1.0))
    plt.rcParams["figure.figsize"] = (16, 8)
    plt.savefig('static/maintenance.png')


# Energy Module
    n = int(session["number_years"])
    costs = [0]
    for i in session["user_points"]:
        dr1 = round((i[2] + i[3]) / (i[0] * i[1]) * 10000, 2)
        dr2 = round(dr1 - (i[2] + i[3]), 2)
        dr3 = round(((i[2] + i[3]) / (i[0] * i[1]) * 10000 - (i[2] + i[3])) * (i[4] * 725), 2)
        i[6] = dr1
        i[7] = dr2
        i[8] = dr3
    total_loss = 0
    for i in session["user_points"]:
        total_loss += i[8]
    dr4 = round(total_loss * float(energy_price), 2)
    dr5 = 0
    for i in range(0, n ):
        dr5 += dr4 * (1 + (float(annual_increase) / 100)) ** i
        costs.append(round(dr5, 2))
    session["energie"] = costs[-1]

    #Energy chart
    a = np.array(costs)
    # #     b = np.array(main_vfd)
    plt.switch_backend('agg')
    plt.plot(a, label='Costs')
    #     plt.plot(b, label='VFD')
    plt.title('Energy Cost for ' + session["unit_name"])
    plt.xlabel('Year')
    plt.ylabel('Energy Cost, ' + session["currency"])
    plt.legend()
    plt.grid()
    plt.xticks(np.arange(0, n + 1, 1.0))
    plt.rcParams["figure.figsize"] = (16, 8)
    plt.savefig('static/energy.png')
    years = range(0, n+1)

    #TCO
    main=mains[-1]
    total_capex_direct = 0
    direct = []

    for i in range(len(session["user_components"])):
        total_capex_direct += int(session["user_components"][i][1])
        direct.append(int(session["user_components"][i][1]))
    direct.append(total_capex_direct)
    session["capexy"] = total_capex_direct

    prices = []
    per = []
    for maintenance in session["user_maintenances"]:
        prices.append(int(maintenance[2]))
        per.append(int(maintenance[1]))
    n = int(session["number_years"])
    i = 1
    x = 0
    mains = []
    while i <= n:
        for j in range(len(per)):
            if i % per[j] == 0:
                x += prices[j] * (1 + (annual_increase / 100)) ** (i - 1)
        mains.append(round(x))
        i += 1

    labels = ['CAPEX', 'Maintenance', 'Energy']
    if session["capexy"] > 0 and main > 0 and session["energie"] > 0:
        sizes = [int(session["capexy"]), int(main), int(session["energie"])]

        fig1, ax1 = plt.subplots()

        ax1.pie(sizes, labels=labels, shadow=False, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig('static/tco.png', bbox_inches=None)

    #Efficiency
    for i in session["user_points"]:
        dr1=round((i[2] + i[3]) / (i[0] * i[1]) * 10000,2)
        dr2=round(dr1-(i[2] + i[3]),2)
        dr3=round(((i[2]+i[3])/(i[0]*i[1])*10000-(i[2]+i[3]))*(i[4]*725),2)
        i[6]=dr1
        i[7]=dr2
        i[8]=dr3
    total_loss=0
    for i in session["user_points"]:
        total_loss+=i[8]
    dr4=round(total_loss*float(energy_price),2)

    session.modified = True
    return render_template('form_page.html',dr4=dr4,total_loss=total_loss,info=session["info"],configurations=configurations,main=main,capexy=session["capexy"],energie=session["energie"],costs=costs,mains=mains, years=years,total_capex_direct=total_capex_direct, non_eq=non_eq,ot_eq=ot_eq,main_eq=main_eq,dr_eq=dr_eq,el_eq=el_eq,user_points=session["user_points"],user_maintenances=session["user_maintenances"],user_components=session["user_components"],sum=sum,message=message,component_list=component_list,a=a,m=m,eff_driver=eff_driver,eff_other=eff_other,power_pump=power_pump,power_aux=power_aux,scenario=scenario,k=k, i=i,j=j,component=component,component_price=component_price, comments=comments, main_type=main_type, period=period,main_price=main_price, main_comments=main_comments, unit_name=session["unit_name"], energy_price=energy_price, annual_increase=annual_increase, number_years=session["number_years"],project_name=session["project_name"], currency=session["currency"] )

#Обработка формы добавление компонента
@app.route('/form_page/add_component', methods=['POST','GET'])
def form_page_add_component():
    global n1

    if request.method=="POST":
        #unit_components = Component.query.all()
        component = request.form["component"]
        component_price = request.form["component_price"]
        if component_price=='':
            component_price=0
        comments = request.form["comments"]
        if component=='' or component_price=='':
            return "Select component and enter its price"
        if not "user_components" in session:
            session["user_components"] = []
        session["user_components"].append([component,component_price,comments,n1])
        n1+=1
        for i in range(len(session["user_components"])):
            session["user_components"][i][3] = i
        try:
            return redirect(url_for('form_page'))
        except:
            return "При добалении данных произошла ошибка"
    else:
        return render_template('form_page.html', user_components=session["user_components"],component=component,component_price=component_price,comments=comments)

#Обработка формы добавление обслуживания
@app.route('/form_page/add_maintenance', methods=['POST','GET'])
def form_page_add_maintenance():
    global n2
    if request.method=="POST":
        main_type = request.form["main_type"]
        period = request.form["period"]
        if main_type=="Annual Maintenance-Spares" and period!=1:
            period=1
        main_price = request.form["main_price"]
        main_comments = request.form["main_comments"]
        session["user_maintenances"].append([main_type, period, main_price,main_comments, n2])
        n2 += 1
        return redirect(url_for('form_page'))

        #maintenance=Maintenance(main_type=main_type,period=period,main_price=main_price,main_comments=main_comments)
        try:
            db.session.add(maintenance)
            db.session.commit()
            return redirect(url_for('form_page'))
        except:
            return "При добалении данных произошла ошибка"
    else:
        return render_template('form_page.html', user_maintenances=session["user_maintenances"],main_type=main_type,period=period,main_price=main_price,main_comments=main_comments)

#Обработка формы добавление общих данных
@app.route('/form_page/add_general', methods=['POST','GET'])
def form_page_add_general():
    global unit_name,energy_price,annual_increase
    #generals = General.query.all()

    if request.method=="POST":
        session["currency"] = request.form["currency"]
        if request.form["project_name"]!='':
            session["project_name"] = request.form["project_name"]
        if request.form["unit_name"]!='':
            session["unit_name"] = request.form["unit_name"]
        if request.form["energy_price"]!='':
            energy_price = request.form["energy_price"]
        if request.form["annual_increase"]!='':
            annual_increase = request.form["annual_increase"]
        if request.form["number_years"] != '':
            session["number_years"] = request.form["number_years"]
        flash('Updated successfully', 'success')
        return redirect(url_for('form_page'))
        # generals = General.query.all()
        # unit_name = request.form["unit_name"]
        # energy_price = request.form["energy_price"]
        # if energy_price=='':
        #     energy_price=generals[-1].energy_price
        # annual_increase = request.form["annual_increase"]
        # if annual_increase=='':
        #     annual_increase=generals[-1].annual_increase
        # number_years = request.form["number_years"]
        # if number_years=='':
        #     number_years=generals[-1].number_years
        # general=General(unit_name=unit_name,energy_price=energy_price,annual_increase=annual_increase,number_years=number_years)

    else:
        return render_template('form_page.html', project_name=session["project_name"],generals=generals, energy_price=energy_price,annual_increase=annual_increase,number_years=session["number_years"])

@app.route('/form_page/add_point', methods=['POST','GET'])
def form_page_add_point():
    global n3
    # points = Point.query.all()

    if request.method=="POST":
        #points = Point.query.all()
        eff_driver = int(request.form["eff_driver"])
        eff_other = int(request.form["eff_other"])
        if eff_driver>100 or eff_driver<0 or eff_other>100 or eff_other<0:
            return "Efficiency values should be in range from 0 to 100"
        power_pump = int(request.form["power_pump"])
        power_aux = int(request.form["power_aux"])
        scenario = int(request.form["scenario"])
        sum = 0
        for i in range(len(session["user_points"])):
            sum += int(session["user_points"][i][4])
        if sum + int(scenario) > 12:
            return "Sum of operating scenarios should not be more than 12 months/year "
        session["user_points"].append([eff_driver, eff_other, power_pump,power_aux,scenario, n3,0,0,0])
        n3 += 1
        #point=Point(eff_driver=eff_driver,eff_other=eff_other,power_pump=power_pump,power_aux=power_aux,scenario=scenario)
        try:
            return redirect(url_for('form_page'))
        except:
            return "При добалении данных произошла ошибка"
    else:
        return render_template('form_page.html', points=points, eff_driver=eff_driver,eff_other=eff_other,power_pump=power_pump,power_aux=power_aux,scenario=scenario)


@app.route('/form_page/<int:id>/del_man')
def delete_maintenance(id):
    #     maintenance = Maintenance.query.get_or_404(id)

    try:
        session["user_maintenances"].pop(id)
        return redirect('/form_page')
    except:
        return "При удалении сведений об обслуживании произошла ошибка"

@app.route('/form_page/<int:id>/del_point')
def delete_point(id):
    #point = Point.query.get_or_404(id)
    try:
        #db.session.delete(point)
        #db.session.commit()
        session["user_points"].pop(id)
        return redirect('/form_page')
    except:
        return "При удалении operating point произошла ошибка"

@app.route('/form_page/<int:id>/del')
def delete_component(id):

    # unit_component = Component.query.get_or_404(id)
    # try:
    #     db.session.delete(unit_component)
    #     db.session.commit()
    try:
        session["user_components"].pop(id)
        return redirect('/form_page')
    except:
        return "При удалении компонента произошла ошибка"



@app.route('/efficiency', methods=['POST','GET'])
def efficiency():
    #generals = General.query.all()
    #points = Point.query.all()

    for i in session["user_points"]:
        dr1=round((i[2] + i[3]) / (i[0] * i[1]) * 10000,2)
        dr2=round(dr1-(i[2] + i[3]),2)
        dr3=round(((i[2]+i[3])/(i[0]*i[1])*10000-(i[2]+i[3]))*(i[4]*725),2)
        i[6]=dr1
        i[7]=dr2
        i[8]=dr3
    total_loss=0
    for i in session["user_points"]:
        total_loss+=i[8]
    dr4=round(total_loss*float(energy_price),2)
    # unit_name = generals[-1].unit_name
    # energy_price = generals[-1].energy_price
    return render_template('efficiency.html',currency=session["currency"],dr4=dr4,total_loss=total_loss,user_points=session["user_points"],unit_name=session["unit_name"],energy_price=energy_price,annual_increase=annual_increase)


@app.route('/tco', methods=['POST', 'GET'])
def tco():
    return render_template('tco.html',capexy=session["capexy"],main=main,energie=energie, currency=session["currency"], labels=labels,number_years=session["number_years"])


@app.route('/ProcessPrice/',methods=['POST','GET'])
def ProcessPrice():
    if request.method == "POST":
        x=0
        y=0
        userdata = request.get_json()
        # userdata=json.loads(userdata)
        x=userdata[1]['price']
        y=userdata[0]['item']
        y=y[6:]
        session["info"]=[int(y),int(x)]
        session["user_components"][int(y)][1]=int(x)

    return redirect(url_for('form_page'))

@app.route('/ProcessPrice2/',methods=['POST','GET'])
def ProcessPrice2():
    if request.method == "POST":
        session["info"].append(1)

    return redirect(url_for('form_page'))

@app.route('/create_pdf', methods=['POST','GET'])
def create_pdf():
    return 'this function will be added soon'

@app.route('/select_conf', methods=['POST','GET'])
def select_conf():
    return render_template('select_conf.html',configurations=configurations)

if __name__=="__main__":
    app.run(debug=True)
    app.config["TEMPLATES_AUTO_RELOAD"] = True