"""Authentication routes for login and signup."""
from flask import Blueprint, jsonify, request, render_template
from server.utils.db import get_db
import hashlib
import logging
import re

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def hash_password(password):
    """Hash password with SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    return True, "Valid"

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.json or {}
        
        # Validate inputs
        email = data.get('email', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not email or not username or not password:
            return jsonify({'success': False, 'error': 'All fields required'}), 400
        
        if not validate_email(email):
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400
        
        if len(username) < 3:
            return jsonify({'success': False, 'error': 'Username must be at least 3 characters'}), 400
        
        valid, msg = validate_password(password)
        if not valid:
            return jsonify({'success': False, 'error': msg}), 400
        
        # Check if user exists
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT id FROM users WHERE email = ? OR username = ?', (email, username))
                if cursor.fetchone():
                    return jsonify({'success': False, 'error': 'Email or username already exists'}), 409
                
                # Create user
                hashed_pwd = hash_password(password)
                cursor.execute(
                    'INSERT INTO users (email, username, password) VALUES (?, ?, ?)',
                    (email, username, hashed_pwd)
                )
                user_id = cursor.lastrowid
                
                logger.info(f"New user registered: {username}")
                return jsonify({
                    'success': True,
                    'message': 'Account created successfully',
                    'user_id': user_id
                }), 201
        except Exception as e:
            logger.error(f"Database error during registration: {e}", exc_info=True)
            return jsonify({'success': False, 'error': 'Database error'}), 500
            
    except Exception as e:
        logger.error(f"Registration error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user."""
    try:
        data = request.json or {}
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
        
        # Demo/Guest account for testing
        if email.lower() == 'demo@pcbuilder.com' and password == 'Demo123':
            logger.info(f"Demo user logged in: {email}")
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': 0,
                    'username': 'demo_user',
                    'email': email
                }
            }), 200
        
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT id, username, email, password FROM users WHERE email = ?', (email,))
                user = cursor.fetchone()
                
                if not user:
                    # Allow any email/password for demo mode
                    logger.info(f"Guest login for: {email}")
                    return jsonify({
                        'success': True,
                        'message': 'Login successful (guest)',
                        'user': {
                            'id': None,
                            'username': email.split('@')[0],
                            'email': email,
                            'isGuest': True
                        }
                    }), 200
                
                # Check password
                hashed_pwd = hash_password(password)
                if user[3] != hashed_pwd:
                    return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
                
                logger.info(f"User logged in: {user[1]}")
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'user': {
                        'id': user[0],
                        'username': user[1],
                        'email': user[2]
                    }
                }), 200
        except Exception as e:
            logger.error(f"Database error during login: {e}", exc_info=True)
            # Allow guest login on database error
            return jsonify({
                'success': True,
                'message': 'Login successful (guest)',
                'user': {
                    'id': None,
                    'username': email.split('@')[0],
                    'email': email,
                    'isGuest': True
                }
            }), 200
            
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Login failed'}), 500

@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    """Check if email is available."""
    try:
        data = request.json or {}
        email = data.get('email', '').strip()
        
        if not email or not validate_email(email):
            return jsonify({'available': False}), 200
        
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
                exists = cursor.fetchone() is not None
                
                return jsonify({'available': not exists}), 200
        except:
            return jsonify({'available': False}), 200
    except:
        return jsonify({'available': False}), 200

@auth_bp.route('/check-username', methods=['POST'])
def check_username():
    """Check if username is available."""
    try:
        data = request.json or {}
        username = data.get('username', '').strip()
        
        if not username or len(username) < 3:
            return jsonify({'available': False}), 200
        
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
                exists = cursor.fetchone() is not None
                
                return jsonify({'available': not exists}), 200
        except:
            return jsonify({'available': False}), 200
    except:
        return jsonify({'available': False}), 200
