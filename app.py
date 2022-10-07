from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
app=Flask( __name__ )
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tco.db'
db=SQLAlchemy(app)


# class Unit (db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     unit_name = db.Column(db.String(30), nullable=False)

class Component(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    component = db.Column(db.String(30), nullable=False)
    comments = db.Column(db.String(30), nullable=False)
    component_price=db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Component %r>' % self.id

class General(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(30), nullable=False)
    energy_price = db.Column(db.Float, nullable=False, default=0.04)
    annual_increase = db.Column(db.Float, nullable=False, default=1.5)
    number_years = db.Column(db.Integer, nullable=False, default=30)

    def __repr__(self):
        return '<General %r>' % self.id

class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eff_driver = db.Column(db.Float, nullable=False)
    eff_other = db.Column(db.Float, nullable=False)
    power_pump = db.Column(db.Float, nullable=False)
    power_aux = db.Column(db.Float, nullable=False)
    scenario = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Point %r>' % self.id

class Maintenance (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_type = db.Column(db.String(30), nullable=False)
    period = db.Column(db.Integer, nullable=False)
    main_price = db.Column(db.Integer, nullable=False)
    main_comments = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Maintenance %r>' % self.id


#Главная страница формы
@app.route('/', methods=['POST','GET'])
@app.route('/form_page', methods=['POST','GET'])
def form_page():
    unit_components = Component.query.all()
    component=0
    component_price=0
    comments=0

    maintenances = Maintenance.query.all()
    main_type = 0
    period = 0
    main_price = 0
    main_comments=0
    i=0
    j=0

    unit_name='P-001'
    energy_price=0.04
    annual_increase=1.5
    number_years = 30

    points = Point.query.all()
    k=0
    eff_driver = 0
    eff_other = 0
    power_pump = 0
    power_aux = 0
    scenario = 0

    return render_template('form_page.html', points=points,eff_driver=eff_driver,eff_other=eff_other,power_pump=power_pump,power_aux=power_aux,scenario=scenario,k=k, i=i,j=j,unit_components=unit_components, component=component,component_price=component_price, comments=comments, main_type=main_type, period=period,main_price=main_price, main_comments=main_comments, maintenances=maintenances, unit_name=unit_name, energy_price=energy_price, annual_increase=annual_increase, number_years=number_years )

#Обработка формы добавление компонента
@app.route('/form_page/add_component', methods=['POST','GET'])
def form_page_add_component():

    unit_components = Component.query.all()
    component=0
    component_price=0
    comments=0

    if request.method=="POST":
        unit_components = Component.query.all()
        component_price = request.form["component_price"]
        comments = request.form["comments"]
        component = request.form["component"]
        unit_component=Component(component=component,component_price=component_price,comments=comments)
        try:
            db.session.add(unit_component)
            db.session.commit()
            return redirect(url_for('form_page'))
        except:
            return "При добалении данных произошла ошибка"
    else:
        return render_template('form_page.html', unit_components=unit_components, component=component,component_price=component_price,comments=comments)

#Обработка формы добавление обслуживания
@app.route('/form_page/add_maintenance', methods=['POST','GET'])
def form_page_add_maintenance():
    maintenances = Maintenance.query.all()
    main_type = 0
    period = 0
    main_price = 0
    main_comments = 0
    if request.method=="POST":
        maintenances = Maintenance.query.all()
        main_type = request.form["main_type"]
        period = request.form["period"]
        main_price = request.form["main_price"]
        main_comments = request.form["main_comments"]
        maintenance=Maintenance(main_type=main_type,period=period,main_price=main_price,main_comments=main_comments)
        try:
            db.session.add(maintenance)
            db.session.commit()
            return redirect(url_for('form_page'))
        except:
            return "При добалении данных произошла ошибка"
    else:
        return render_template('form_page.html', maintenances=maintenances, main_type=main_type,period=period,main_price=main_price,main_comments=main_comments)

#Обработка формы добавление общих данных
@app.route('/form_page/add_general', methods=['POST','GET'])
def form_page_add_general():

    generals = General.query.all()

    if request.method=="POST":
        # generals = General.query.get_or_404(id)
        # try:
        #     db.session.delete(maintenance)
        #     db.session.commit()
        # except:
        #     return "При удалении данных произошла ошибка"
        generals = General.query.all()
        unit_name = request.form["unit_name"]
        energy_price = request.form["energy_price"]
        annual_increase = request.form["annual_increase"]
        number_years = request.form["number_years"]
        general=General(unit_name=unit_name,energy_price=energy_price,annual_increase=annual_increase,number_years=number_years)
        try:
            db.session.add(general)
            db.session.commit()
            return redirect(url_for('form_page'))
        except:
            return "При добалении данных произошла ошибка"
    else:
        return render_template('form_page.html', generals=generals, energy_price=energy_price,annual_increase=annual_increase,number_years=number_years)

@app.route('/form_page/add_point', methods=['POST','GET'])
def form_page_add_point():
    points = Point.query.all()
    eff_driver = 0
    eff_other = 0
    power_pump = 0
    power_aux = 0
    scenario = 0
    if request.method=="POST":
        points = Point.query.all()
        eff_driver = request.form["eff_driver"]
        eff_other = request.form["eff_other"]
        power_pump = request.form["power_pump"]
        power_aux = request.form["power_aux"]
        scenario = request.form["scenario"]
        point=Point(eff_driver=eff_driver,eff_other=eff_other,power_pump=power_pump,power_aux=power_aux,scenario=scenario)
        try:
            db.session.add(point)
            db.session.commit()
            return redirect(url_for('form_page'))
        except:
            return "При добалении данных произошла ошибка"
    else:
        return render_template('form_page.html', points=points, eff_driver=eff_driver,eff_other=eff_other,power_pump=power_pump,power_aux=power_aux,scenario=scenario)


@app.route('/form_page/<int:id>/del_man')
def delete_maintenance(id):
    maintenance = Maintenance.query.get_or_404(id)
    try:
        db.session.delete(maintenance)
        db.session.commit()
        return redirect('/form_page')
    except:
        return "При удалении сведений об обслуживании произошла ошибка"


@app.route('/form_page/<int:id>/del_point')
def delete_point(id):
    point = Point.query.get_or_404(id)
    try:
        db.session.delete(point)
        db.session.commit()
        return redirect('/form_page')
    except:
        return "При удалении operating point произошла ошибка"




@app.route('/form_page/<int:id>/del')
def delete_component(id):
    unit_component = Component.query.get_or_404(id)
    try:
        db.session.delete(unit_component)
        db.session.commit()
        return redirect('/form_page')
    except:
        return "При удалении компонента произошла ошибка"

@app.route('/maintenance', methods=['POST','GET'])
def maintenance():
     unit_components = Component.query.all()
     maintenances = Maintenance.query.all()
     prices=[]
     per=[]
     for maintenance in maintenances:
         prices.append(maintenance.main_price)
         per.append(maintenance.period)

     generals = General.query.all()
     annual_increase = generals[-1].annual_increase #annual_increase = 1.5
     n=generals[-1].number_years #n = 30
     #[maintenances[-1].period,maintenances[-1].main_price]
     main_type = 0
     period = 0
     main_price = 0
     main_comments = 0

     i = 1
     x = 0
     mains=[]
     while i <= n:
         for j in range(len(per)):
             if i%per[j]==0:
                x+=prices[j] * (1 + (annual_increase / 100)) ** (i - 1)
         mains.append(round(x))
         i+=1


     a = np.array(mains)
#     b = np.array(main_vfd)
     plt.switch_backend('agg')
     plt.plot(a, label='Costs')
#     plt.plot(b, label='VFD')
     plt.title('Mainenance Cost,  MEUR, per Pump Unit')
     plt.xlabel('Year')
     plt.ylabel('Maintenance Cost, EUR')
     plt.legend()
     plt.grid()
     plt.xticks(np.arange(1, n + 1, 1.0))
     plt.rcParams["figure.figsize"] = (16, 8)
     plt.savefig('static/maintenance.png')
     years=range(1,n+1)
     # plt.show()
     # plt.close(fig)
     return render_template('maintenance.html',mains=mains,a=a, years=years)

#Конец обработки форм


#Обработка  форм
@app.route('/unit', methods=['POST','GET'])
def unit():
    unit_form = 0
    # if unit_form.validate_on_submit():
    #     unit_form=0
    #     pass
    return render_template('form_page.html')

@app.route('/points', methods=['POST','GET'])
def points():
    points_form = points_form
    # if points_form.validate_on_submit():
    #     points_form=0
    #     pass
    return render_template('form_page.html', points_form=points_form)


@app.route('/efficiency', methods=['POST','GET'])
def efficiency():
    generals = General.query.all()
    points = Point.query.all()

    # eff_driver = points[0].eff_driver
    # eff_other = points[0].eff_other
    # power_pump = points[0].power_pump
    # power_aux = points[0].power_aux
    # scenario = points[0].scenario

    unit_name = generals[0].unit_name
    energy_price = generals[0].energy_price
    annual_increase = generals[0].annual_increase
    return render_template('efficiency.html',unit_name=unit_name,energy_price=energy_price,annual_increase=annual_increase,points=points)

@app.route('/energy', methods=['POST','GET'])
def energy():

    return render_template('energy.html')

@app.route('/capex', methods=['POST','GET'])
def capex():
    unit_components = Component.query.all()
    generals = General.query.all()
    unit_name = generals[0].unit_name
    total_capex_direct=0
    direct=[]
    for i in range(len(unit_components)):
        total_capex_direct+=unit_components[i].component_price
        direct.append(unit_components[i].component_price)
    direct.append(total_capex_direct)

    labels=[]
    for j in range(len(unit_components)):
        labels.append(unit_components[j].component)
    labels.append('total_capex_direct')

    #labels = ['Pump', 'Baseplate', 'Driver','Coupling','Supply_System','Fluid_Coupling','vfd','Lube_oil_system','transformer','harmonic_filter','others','instruments','Total Cost',]
    #direct = [unit_components[-1].pump, unit_components[-1].baseplate, unit_components[-1].driver, unit_components[-1].coupling, unit_components[-1].Supply_System, unit_components[-1].Fluid_Coupling, unit_components[-1].vfd, unit_components[-1].Lube_oil_system,
              #unit_components[-1].transformer, unit_components[-1].harmonic_filter, unit_components[-1].others, unit_components[-1].instruments, total_capex_direct]
    #throttle = [units[-1].pump_throttle, units[-1].baseplate_throttle, units[-1].motor_throttle,total_capex_throttle]

    x = np.arange(len(labels))  # the label locations
    width = 0.20  # the width of the bars


    fig, ax = plt.subplots(figsize=(15,10))
    rects1 = ax.bar(x - width / 2, direct, width, label='Total cost')
    #rects2 = ax.bar(x + width / 2, throttle, width, label='Throttle')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('EURO')
    ax.set_title('CAPEX for '+unit_name)
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    #ax.bar_label(rects2, padding=3)
    fig.savefig('static/capex.png')  # save the figure to file
    plt.close(fig)
    #plt.savefig('myfig')


    try:
        return render_template('capex.html',x=x,unit_name=unit_name,unit_components=unit_components,total_capex_direct=total_capex_direct)
    except:
        return render_template('capex.html', unit_name=unit_name,unit_components=unit_components, total_capex_direct=total_capex_direct)

if __name__=="__main__":
    app.run(debug=True)