from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File path for storing feedback
FEEDBACK_FILE = 'feedback_data.json'

# In-memory storage for feedback
feedback_list = []

# Load feedback from file on startup
def load_feedback():
    global feedback_list
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, 'r') as f:
                feedback_list = json.load(f)
        except:
            feedback_list = []
    else:
        feedback_list = []

# Save feedback to file
def save_feedback():
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_list, f, indent=2)

# Load feedback when app starts
load_feedback()

@app.route('/')
def index():
    """Homepage route"""
    return render_template('index.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Feedback form route"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Add feedback to list
        feedback_item = {
            'name': name,
            'email': email,
            'message': message
        }
        feedback_list.append(feedback_item)
        
        # Save to file
        save_feedback()
        
        # Redirect to view page
        return redirect(url_for('view_feedback'))
    
    return render_template('feedback.html')

@app.route('/view')
def view_feedback():
    """View all feedback route"""
    return render_template('view.html', feedbacks=feedback_list)

if __name__ == '__main__':
    app.run(debug=True)
