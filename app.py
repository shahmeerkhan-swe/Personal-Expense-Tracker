from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
db = SQLAlchemy(app)
api = Api(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)

db.create_all()

expense_parser = reqparse.RequestParser()
expense_parser.add_argument('date', type=str, required=True, help= 'Date is required.')
expense_parser.add_argument('category', type=str, required=True, help= 'Category is required.')
expense_parser.add_argument('amount', type=float, required=True, help= 'Amount is required.')
expense_parser.add_argument('description', type=str, required=False)

class ExpenseList(Resource):
    
    def get(self, expense_id =None): 
        if expense_id: 
            expense = Expense.query.get(expense_id)
            if not expense: 
                return {'message': 'Expense not found'}, 404
            return { 
                'id': expense.id,
                'date': expense.date,
                'category': expense.category,
                'amount': expense.amount,
                'description': expense.description
            }
        else: 
            expenses = Expense.query.all()
            return [{'id': e.id, 'date': e.date, 'category': e.category, 'amount': e.amount, 'description': e.description} for e in expenses]
        
    def post(self):
        args = expense_parser.parse_args()
        expense = Expense(
            date=args['date'], 
            category=args['category'],
            amount=args['amount'],
            description=args['description']
        )
        db.session.add(expense)
        db.session.commit()
        return {'message': 'Expense added successfully', 'id': expense.id}, 201

    def put(self, expense_id):
        args = expense_parser.parse_args()
        expense = Expense.query.get(expense_id)

        if not expense: 
            return {'message': 'Expense not found'}, 404    
        
        expense.date = args['date'] 
        expense.category = args['category']
        expense.amount = args['amount']
        expense.description = args['description']
        db.session.commit()
        return {'message': 'Expense updated successfully'}, 200
    
    def delete(self, expense_id):
        expense = Expense.query.get(expense_id)

        if not expense: 
            return {'message': 'Expense not found'}, 404
        
        db.session.delete(expense)  
        db.session.commit()
        return {'message': 'Expense deleted successfully'}, 200
    

api.add_resource(ExpenseList, '/expenses', '/expenses/<int:expense_id>')