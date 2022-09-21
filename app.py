from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
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
    energy_price = db.Column(db.Float, nullable=False, default=0.04)
    annual_increase = db.Column(db.Float, nullable=False, default=1.5)
    number_years = db.Column(db.Integer, nullable=False, default=30)

    def __repr__(self):
        return '<General %r>' % self.id

class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eff_driver = db.Column(db.Float, nullable=False)
    eff_other = db.Column(db.Float, nullable=False)
    power_consumption = db.Column(db.Float, nullable=False)
    operation_scen = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Point %r>' % self.id

class Maintenance (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_type = db.Column(db.String(30), nullable=False)
    period = db.Column(db.Integer, nullable=False)
    main_price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Maintenance %r>' % self.id


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
    i=0
    return render_template('form_page.html', i=i,unit_components=unit_components, component=component,component_price=component_price, comments=comments, main_type=main_type, period=period,main_price=main_price, maintenances=maintenances)


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

@app.route('/form_page/add_maintenance', methods=['POST','GET'])
def form_page_add_maintenance():
    maintenances = Maintenance.query.all()
    main_type = 0
    period = 0
    main_price = 0
    if request.method=="POST":
        maintenances = Maintenance.query.all()
        main_type = request.form["main_type"]
        period = request.form["period"]
        main_price = request.form["main_price"]
        maintenance=Maintenance(main_type=main_type,period=period,main_price=main_price)
        try:
            db.session.add(maintenance)
            db.session.commit()
            return redirect(url_for('form_page'))
        except:
            return "При добалении данных произошла ошибка"
    else:
        return render_template('form_page.html', maintenances=maintenances, main_type=main_type,period=period,main_price=main_price)


@app.route('/form_page/<int:id>/del_man')
def delete_maintenance(id):
    maintenance = Maintenance.query.get_or_404(id)
    try:
        db.session.delete(maintenance)
        db.session.commit()
        return redirect('/form_page')
    except:
        return "При удалении сведений об обслуживании произошла ошибка"






@app.route('/form_page/<int:id>/del')
def delete_component(id):
    unit_component = Component.query.get_or_404(id)
    try:
        db.session.delete(unit_component)
        db.session.commit()
        return redirect('/form_page')
    except:
        return "При удалении компонента произошла ошибка"


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

@app.route('/maintenance', methods=['POST','GET'])
def maintenance():

    # if maintenance_form.validate_on_submit():
    #     maintenance_form=0
    #     pass
    return render_template('form_page.html', maintenance_form=maintenance_form)

#Конец обработки форм





@app.route('/efficiency', methods=['POST','GET'])
def efficiency():

    return render_template('efficiency.html')

@app.route('/energy', methods=['POST','GET'])
def energy():
    return render_template('energy.html')



if __name__=="__main__":
    app.run(debug=True)