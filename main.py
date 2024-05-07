from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import desc,or_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///profits.db"
db = SQLAlchemy(app)

class Profit(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String,nullable = False)
    revenue = db.Column(db.Integer,nullable = False)
    net_income = db.Column(db.Integer,nullable = False)



@app.route('/')
def home():
    total = db.session.query(func.sum(Profit.revenue)).scalar()
    income = db.session.query(func.sum(Profit.net_income)).scalar()
    kinder = db.session.query(func.sum(Profit.revenue)).filter(Profit.name == 'Kindle 전자책 팀').scalar()
    game = db.session.query(func.sum(Profit.revenue)).filter(Profit.name == '게임 팀').scalar()
    goods = db.session.query(func.sum(Profit.revenue)).filter(Profit.name == '굿즈 팀').scalar()
    consulting = db.session.query(func.sum(Profit.revenue)).filter(Profit.name == '입시 컨설팅 플랫폼 팀').scalar()
    ticket = db.session.query(func.sum(Profit.revenue)).filter(Profit.name == '잔여 티켓 플랫폼 팀').scalar()

    kinder_income = db.session.query(func.sum(Profit.net_income)).filter(Profit.name == 'Kindle 전자책 팀').scalar()
    game_income = db.session.query(func.sum(Profit.net_income)).filter(Profit.name == '게임 팀').scalar()
    goods_income = db.session.query(func.sum(Profit.net_income)).filter(Profit.name == '굿즈 팀').scalar()
    consulting_income = db.session.query(func.sum(Profit.net_income)).filter(Profit.name == '입시 컨설팅 플랫폼 팀').scalar()
    ticket_income = db.session.query(func.sum(Profit.net_income)).filter(Profit.name == '잔여 티켓 플랫폼 팀').scalar()
    
    if kinder_income == 0:
        kinder_ratio = 0
    else:
        kinder_ratio = round(kinder_income / kinder ,2) *100
    if game_income == 0:
        game_ratio = 0
    else:
        game_ratio = round(game_income / game ,2) *100
    if goods_income == 0:
        goods_ratio = 0
    else:
        goods_ratio = round(goods_income / goods ,2) *100

    if consulting_income == 0:
        consulting_ratio = 0
    else:
        consulting_ratio = round(consulting_income / consulting ,2) *100

    if ticket_income == 0:
        ticket_ratio = 0
    else:
        ticket_ratio = round(ticket_income / ticket ,2) *100
    
    revenue_dic = {"total":total,"income":income ,"kinder":kinder,"game":game,"goods":goods,"consulting":consulting,"ticket":ticket,"kinder_income":kinder_ratio,"game_income":game_ratio,"goods_income":goods_ratio,"consulting_income":consulting_ratio,"ticket_income":ticket_ratio}
    return render_template("dashboard.html", revenues = revenue_dic)


@app.route('/add')
def add():
    return render_template('forms.html')

@app.route('/adding_profit',methods=['POST'])
def adding_profit(): #수익 추가 함수
    teams = {
        1:'Kindle 전자책 팀',
        2:'게임 팀',
        3:'굿즈 팀',
        4:'입시 컨설팅 플랫폼 팀',
        5:'잔여 티켓 플랫폼 팀'
    }
    new_revenue = int(float(request.form.get('revenue')))
    new_net_income = int(float(request.form.get('net_income')))
    team_name = teams[int(request.form.get('team'))]

    #수익 추가 
    with app.app_context(): 
        profit_to_add = Profit(
            name = team_name,
            revenue = new_revenue,
            net_income = new_net_income
        )
        db.session.add(profit_to_add)
        db.session.commit()
    return redirect(url_for('add'))

@app.route('/table',methods=['POST','GET'])
def modify():
    if request.method == 'POST':
        team_name = request.form.get('sort_team')
        result = Profit.query.filter(or_(Profit.name == team_name, Profit.name.like(f'%{team_name}%')), Profit.id >= 6).order_by(desc(Profit.id)).all()
        return render_template('tables.html',results = result)
    else:
        result = Profit.query.filter(Profit.id >= 6).order_by(desc(Profit.id)).all()
        return render_template('tables.html',results = result)

#데이터 삭제
@app.route('/delete')
def delete():
    delete_id = request.args.get('id')
    with app.app_context():
        result_to_delete = Profit.query.get(delete_id)
        db.session.delete(result_to_delete)
        db.session.commit()
    return redirect(url_for('modify'))



if __name__ == "__main__":
    app.run(debug=True)