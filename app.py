from flask import Flask, render_template, url_for, request, redirect, flash,session, make_response
from flask_sqlalchemy import SQLAlchemy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pdfkit
app=Flask( __name__ )
app.secret_key='BAD_SECRET_KEY'
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tco.db'
# db=SQLAlchemy(app)

component_list=['Pump','Compressor','Baseplate','Driver','Coupling','Supply_System','Fluid_Coupling','VFD','Lube_Oil_System','Transformer','Harmonic_filter','Instruments','Fan','Mixer','Diesel','Turbine','Cabinet','Others']
user_components = []
user_maintenances = []
user_points= []

project_name='project 1'
unit_name='P-001'
energy_price=0.04
annual_increase=1.5
number_years = 30
currency= '$'
n1=1
n2=1
n3=0
capexy=0
main=0
energie=0


#Главная страница формы
@app.route('/', methods=['POST','GET'])
@app.route('/form_page', methods=['POST','GET'])
def form_page():
    global user_maintenances,user_components,user_points
    for i in range(len(user_components)):
        user_components[i][3] = i
    for y in range(len(user_maintenances)):
        user_maintenances[y][4] = y
    for z in range(len(user_points)):
        user_points[z][5] = z
    # for z in range(len(user_points)):
    #     user_points[z][5] = z
    #unit_components = Component.query.all()
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
    for i in range(len(user_points)):
        sum+=user_points[i][5]
    if sum<12:
        message='Please note that sum of scenarios for all points should be 12(months)'
    elif sum>12:
        message='Sum of scenarios is more than 12(months)!'

    k=0
    eff_driver = 0
    eff_other = 0
    power_pump = 0
    power_aux = 0
    scenario = 0
    a=0

    return render_template('form_page.html',user_points=user_points,user_maintenances=user_maintenances,user_components=user_components,sum=sum,message=message,component_list=component_list,a=a,m=m,eff_driver=eff_driver,eff_other=eff_other,power_pump=power_pump,power_aux=power_aux,scenario=scenario,k=k, i=i,j=j,component=component,component_price=component_price, comments=comments, main_type=main_type, period=period,main_price=main_price, main_comments=main_comments, unit_name=unit_name, energy_price=energy_price, annual_increase=annual_increase, number_years=number_years,project_name=project_name, currency=currency )

#Обработка формы добавление компонента
@app.route('/form_page/add_component', methods=['POST','GET'])
def form_page_add_component():
    global n1
    # unit_components = Component.query.all()
    # component=0
    # component_price=0
    # comments=0
    if request.method=="POST":
        #unit_components = Component.query.all()
        component_price = request.form["component_price"]
        comments = request.form["comments"]
        component = request.form["component"]
        user_components.append([component,component_price,comments,n1])
        n1+=1
        for i in range(len(user_components)):
            user_components[i][3] = i
        try:
            return redirect(url_for('form_page'))
        except:
            return "При добалении данных произошла ошибка"
    else:
        return render_template('form_page.html', user_components=user_components,component=component,component_price=component_price,comments=comments)

#Обработка формы добавление обслуживания
@app.route('/form_page/add_maintenance', methods=['POST','GET'])
def form_page_add_maintenance():
    # maintenances = Maintenance.query.all()
    # main_type = 0
    # period = 0
    # main_price = 0
    # main_comments = 0
    global n2
    if request.method=="POST":
        #maintenances = Maintenance.query.all()
        main_type = request.form["main_type"]
        period = request.form["period"]
        main_price = request.form["main_price"]
        main_comments = request.form["main_comments"]
        user_maintenances.append([main_type, period, main_price,main_comments, n2])
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
        return render_template('form_page.html', user_maintenances=user_maintenances,main_type=main_type,period=period,main_price=main_price,main_comments=main_comments)

#Обработка формы добавление общих данных
@app.route('/form_page/add_general', methods=['POST','GET'])
def form_page_add_general():
    global unit_name,energy_price,annual_increase,number_years,project_name,currency
    #generals = General.query.all()

    if request.method=="POST":
        # if request.form["currency"]!='':
        currency = request.form["currency"]
        if request.form["project_name"]!='':
            project_name = request.form["project_name"]
        if request.form["unit_name"]!='':
            unit_name = request.form["unit_name"]
        if request.form["energy_price"]!='':
            energy_price = request.form["energy_price"]
        if request.form["annual_increase"]!='':
            annual_increase = request.form["annual_increase"]
        if request.form["number_years"] != '':
            number_years = request.form["number_years"]
        flash('Updated successfully', 'success')
        return redirect(url_for('form_page'))
        # generals = General.query.all()
        # unit_name = request.form["unit_name"]
        # if unit_name=='':
        #     unit_name=generals[-1].unit_name
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
        # try:
        #     db.session.query(General).delete()
        #     db.session.add(general)
        #     db.session.commit()
        #     return redirect(url_for('form_page'))
        # except:
        #     return "При добалении данных произошла ошибка"
    else:
        return render_template('form_page.html', project_name=project_name,generals=generals, energy_price=energy_price,annual_increase=annual_increase,number_years=number_years)

@app.route('/form_page/add_point', methods=['POST','GET'])
def form_page_add_point():
    global n3
    # points = Point.query.all()
    # eff_driver = 0
    # eff_other = 0
    # power_pump = 0
    # power_aux = 0
    # scenario = 0
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
        for i in range(len(user_points)):
            sum += int(user_points[i][4])
        if sum + int(scenario) > 12:
            return "Sum of operating scenarios should not be more than 12 months/year "
        user_points.append([eff_driver, eff_other, power_pump,power_aux,scenario, n3,0,0,0])
        n3 += 1
        #point=Point(eff_driver=eff_driver,eff_other=eff_other,power_pump=power_pump,power_aux=power_aux,scenario=scenario)
        try:
            #db.session.add(point)
            #db.session.commit()
            return redirect(url_for('form_page'))
        except:
            return "При добалении данных произошла ошибка"
    else:
        return render_template('form_page.html', points=points, eff_driver=eff_driver,eff_other=eff_other,power_pump=power_pump,power_aux=power_aux,scenario=scenario)


@app.route('/form_page/<int:id>/del_man')
def delete_maintenance(id):
    global user_maintenances
    #     maintenance = Maintenance.query.get_or_404(id)
#     try:
#         db.session.delete(maintenance)
#         db.session.commit()
#         return redirect('/form_page')
    try:
        user_maintenances.pop(id)
        return redirect('/form_page')
    except:
        return "При удалении сведений об обслуживании произошла ошибка"

@app.route('/form_page/<int:id>/del_point')
def delete_point(id):
    global user_points
    #point = Point.query.get_or_404(id)
    try:
        #db.session.delete(point)
        #db.session.commit()
        user_points.pop(id)
        return redirect('/form_page')
    except:
        return "При удалении operating point произошла ошибка"

@app.route('/form_page/<int:id>/del')
def delete_component(id):
    global user_components

    # unit_component = Component.query.get_or_404(id)
    # try:
    #     db.session.delete(unit_component)
    #     db.session.commit()
    #     return redirect('/form_page')
    try:
        user_components.pop(id)
        return redirect('/form_page')
    except:
        return "При удалении компонента произошла ошибка"

@app.route('/maintenance', methods=['POST','GET'])
def maintenance():
     global main
     prices=[]
     per=[]
     for maintenance in user_maintenances:
         prices.append(int(maintenance[2]))
         per.append(int(maintenance[1]))
     # for maintenance in maintenances:
     #     prices.append(maintenance.main_price)
     #     per.append(maintenance.period)

     #generals = General.query.all()
     #unit_name = generals[0].unit_name
     #annual_increase = generals[-1].annual_increase
     n=int(number_years)

     i = 1
     x = 0
     mains=[]
     while i <= n:
         for j in range(len(per)):
             if i%per[j]==0:
                x+=prices[j] * (1 + (float(annual_increase) / 100)) ** (i - 1)
         mains.append(round(x))
         i+=1

     main=mains[-1]
     a = np.array(mains)
#     b = np.array(main_vfd)
     plt.switch_backend('agg')
     plt.plot(a, label='Costs')
#     plt.plot(b, label='VFD')
     plt.title('Mainenance Cost for '+ unit_name)
     plt.xlabel('Year')
     plt.ylabel('Maintenance Cost, ' + currency)
     plt.legend()
     plt.grid()
     plt.xticks(np.arange(1, n + 1, 1.0))
     plt.rcParams["figure.figsize"] = (16, 8)
     plt.savefig('static/maintenance.png')
     years=range(1,n+1)
     # plt.show()
     # plt.close(fig)
     return render_template('maintenance.html',mains=mains,a=a, years=years, unit_name=unit_name, currency=currency)

#Конец обработки форм

@app.route('/efficiency', methods=['POST','GET'])
def efficiency():
    #generals = General.query.all()
    #points = Point.query.all()

    for i in user_points:
        dr1=round((i[2] + i[3]) / (i[0] * i[1]) * 10000,2)
        dr2=round(dr1-(i[2] + i[3]),2)
        dr3=round(((i[2]+i[3])/(i[0]*i[1])*10000-(i[2]+i[3]))*(i[4]*725),2)
        i[6]=dr1
        i[7]=dr2
        i[8]=dr3
    total_loss=0
    for i in user_points:
        total_loss+=i[8]
    dr4=round(total_loss*float(energy_price),2)
    # unit_name = generals[-1].unit_name
    # energy_price = generals[-1].energy_price
    # annual_increase = generals[-1].annual_increase
    return render_template('efficiency.html',currency=currency,dr4=dr4,total_loss=total_loss,user_points=user_points,unit_name=unit_name,energy_price=energy_price,annual_increase=annual_increase)

@app.route('/energy', methods=['POST','GET'])
def energy():
    global energie
    n = int(number_years)
    years = range(1, n + 1)
    costs=[]
    for i in user_points:
        dr1=round((i[2] + i[3]) / (i[0] * i[1]) * 10000,2)
        dr2=round(dr1-(i[2] + i[3]),2)
        dr3=round(((i[2]+i[3])/(i[0]*i[1])*10000-(i[2]+i[3]))*(i[4]*725),2)
        i[6] = dr1
        i[7] = dr2
        i[8] = dr3
    total_loss = 0
    for i in user_points:
        total_loss += i[8]
    dr4 = round(total_loss * float(energy_price), 2)
    dr5=0
    for i in range(1,n+1):
        dr5+=dr4*(1 + (float(annual_increase) / 100)) ** (i - 1)
        costs.append(round(dr5,2))
    energie=costs[-1]
    return render_template('energy.html',costs=costs,years=years,energy_price=energy_price,annual_increase=annual_increase, currency=currency)


@app.route('/tco', methods=['POST', 'GET'])
def tco():
    global capexy, main, energie
    total_capex_direct = 0
    direct = []

    for i in range(len(user_components)):
        total_capex_direct += int(user_components[i][1])
        direct.append(int(user_components[i][1]))
    direct.append(total_capex_direct)
    capexy = total_capex_direct

    prices = []
    per = []
    for maintenance in user_maintenances:
        prices.append(int(maintenance[2]))
        per.append(int(maintenance[1]))
    n = int(number_years)
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
    # if capexy>0 and main>0 and energie>0:
    sizes = [int(capexy),int(main), int(energie)]

    fig1, ax1 = plt.subplots()

    ax1.pie(sizes, labels=labels,shadow=False, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.savefig('static/tco.png',bbox_inches=None)


    return render_template('tco.html',fig1=fig1,capexy=capexy,main=main,energie=energie, currency=currency,sizes=sizes, labels=labels,ax1=ax1)

@app.route('/capex', methods=['POST','GET'])
def capex():
    global capexy
    total_capex_direct=0
    direct=[]
    # for i in range(len(unit_components)):
    #     total_capex_direct+=unit_components[i].component_price
    #     direct.append(unit_components[i].component_price)
    #direct.append(total_capex_direct)

    for i in range(len(user_components)):
        total_capex_direct+=int(user_components[i][1])
        direct.append(int(user_components[i][1]))
    # direct.append(total_capex_direct)
    capexy=total_capex_direct
    labels=[]
    # for j in range(len(unit_components)):
    #     labels.append(unit_components[j].component)
    # labels.append('total_capex_direct')

    for j in range(len(user_components)):
        labels.append(user_components[j][0])
    labels.append('total_capex')


    # x = np.arange(len(labels))  # the label locations
    # width = 0.20  # the width of the bars
    #
    #
    # fig, ax = plt.subplots(figsize=(15,10))
    # rects1 = ax.bar(x - width / 2, direct, width, label='Total cost')
    #rects2 = ax.bar(x + width / 2, throttle, width, label='Throttle')


    # ax.set_ylabel(currency)
    # ax.set_title('CAPEX for '+unit_name)
    # ax.set_xticks(x, labels)
    # ax.legend()
    #
    # ax.bar_label(rects1, padding=3)
    # fig.savefig('static/capex.png')  # save the figure to file
    # plt.close(fig)

    labels.pop()
    sizes = direct
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels,shadow=False, startangle=90,autopct='%1.0f%%')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('static/capex2.png')

    try:
        return render_template('capex.html',user_components=user_components,x=x,unit_name=unit_name,total_capex_direct=total_capex_direct, currency=currency)
    except:
        return render_template('capex.html', user_components=user_components,unit_name=unit_name,total_capex_direct=total_capex_direct)

# @app.route('/create_pdf', methods=['POST','GET'])
# def create_pdf():
#     name = "Giovanni Smith"
#     html = render_template(
#         "form_page.html",
#         name=name)
#     pdf = pdfkit.from_string(html, False)
#     response = make_response(pdf)
#     response.headers["Content-Type"] = "application/pdf"
#     response.headers["Content-Disposition"] = "inline; filename=TCO.pdf"
#     return redirect('/form_page')
#     try:
#         pdf = pdfkit.from_string(html, False)
#         response = make_response(pdf)
#         response.headers["Content-Type"] = "application/pdf"
#         response.headers["Content-Disposition"] = "inline; filename=TCO.pdf"
#         return redirect('/form_page')
#     except:
#         return "Error while creating PDF"

if __name__=="__main__":
    app.run(debug=True)