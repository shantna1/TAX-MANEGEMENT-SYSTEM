from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import database  # Importing our database abstraction layer

app = Flask(__name__, template_folder='templates')

# Ensure database tables exist immediately upon application boot
database.initialize_database()

@app.route('/public/<path:filename>')
def serve_public(filename):
    return send_from_directory(os.path.join(app.root_path, 'public'), filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/calculate-tax', methods=['POST'])
def calculate_tax():
    try:
        data = request.get_json()
        
        # Financial Parameters Extraction
        financial_year = data.get('financial_year')
        gross_income = float(data.get('gross_income', 0))
        deductions = float(data.get('deductions', 0))

        # Core Valuations Guard
        if gross_income < 0 or deductions < 0 or deductions > gross_income:
            return jsonify({'error': 'Invalid financial parameters received.'}), 400

        # Run tax calculations engine
        taxable_income = max(0.0, gross_income - deductions)
        tax_payable = run_backend_slab_calculation(taxable_income)

        # ---- RELATIONAL DATABASE INJECTION PHASE ----
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Mocking or simulating an active client entry for the submission demo
        # (In production, this client_id comes from a selected dropdown list or login token)
        test_client_name = "Default Intern Client"
        test_client_email = "client@pareekassociates.com"

        # Check if the client exists, if not, create them
        cursor.execute("SELECT client_id FROM Clients WHERE email = ?", (test_client_email,))
        client_row = cursor.fetchone()

        if client_row:
            client_id = client_row['client_id']
        else:
            cursor.execute("INSERT INTO Clients (name, email) VALUES (?, ?)", (test_client_name, test_client_email))
            client_id = cursor.lastrowid

        # Insert calculation telemetry parameters directly into TaxRecords mapping back via Foreign Key
        cursor.execute('''
            INSERT INTO TaxRecords (client_id, financial_year, gross_income, deductions, tax_payable)
            VALUES (?, ?, ?, ?, ?)
        ''', (client_id, financial_year, gross_income, deductions, tax_payable))

        # Commit transactional changes safely to the storage layer
        conn.commit()
        conn.close()
        # ---------------------------------------------

        return jsonify({
            'status': 'success',
            'client_id': client_id,
            'financial_year': financial_year,
            'gross_income': gross_income,
            'deductions': deductions,
            'taxable_income': taxable_income,
            'tax_payable': tax_payable
        }), 200

    except Exception as e:
        return jsonify({'error': f'Database or Processing Failure: {str(e)}'}), 500

def run_backend_slab_calculation(income):
    tax = 0.0
    if income <= 300000: return 0.0
    elif income <= 700000: tax = (income - 300000) * 0.05
    elif income <= 1000000: tax = 20000 + (income - 700000) * 0.10
    elif income <= 1200000: tax = 50000 + (income - 1000000) * 0.15
    elif income <= 1500000: tax = 80000 + (income - 1200000) * 0.20
    else: tax = 140000 + (income - 1500000) * 0.30
    return tax

@app.route('/api/tax-records', methods=['GET'])
def get_tax_records():
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        # SQL relational Inner Join query linking TaxRecords with Client Emails
        cursor.execute('''
            SELECT tr.record_id, c.email, tr.financial_year, tr.gross_income, tr.deductions, tr.tax_payable 
            FROM TaxRecords tr
            INNER JOIN Clients c ON tr.client_id = c.client_id
            ORDER BY tr.calculated_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        # Map raw database column row instances safely into standard json lists
        records_list = []
        for row in rows:
            records_list.append({
                'record_id': row['record_id'],
                'email': row['email'],
                'financial_year': row['financial_year'],
                'gross_income': row['gross_income'],
                'deductions': row['deductions'],
                'tax_payable': row['tax_payable']
            })
            
        return jsonify(records_list), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve records: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)