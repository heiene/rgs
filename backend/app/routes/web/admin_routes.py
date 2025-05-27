"""
Admin web routes (HTML interfaces)
"""
from flask import render_template_string
from . import admin_bp


@admin_bp.route('/')
def dashboard():
    """Admin dashboard"""
    # TODO: Create proper template
    return render_template_string("""
    <h1>Admin Dashboard</h1>
    <p>Welcome to the admin interface!</p>
    <ul>
        <li><a href="{{ url_for('admin.login') }}">Login</a></li>
        <li><a href="{{ url_for('admin.upload') }}">Upload CSV</a></li>
    </ul>
    """)


@admin_bp.route('/login')
def login():
    """Admin login page"""
    # TODO: Implement login form and logic
    return render_template_string("""
    <h1>Admin Login</h1>
    <p>Login form - to be implemented</p>
    <a href="{{ url_for('admin.dashboard') }}">Back to Dashboard</a>
    """)


@admin_bp.route('/upload')
def upload():
    """CSV upload page"""
    # TODO: Implement file upload form
    return render_template_string("""
    <h1>CSV Upload</h1>
    <p>File upload form - to be implemented</p>
    <a href="{{ url_for('admin.dashboard') }}">Back to Dashboard</a>
    """) 