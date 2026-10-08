"""Main Flask application."""
import os
import sys
import logging
import traceback
from flask import Flask, render_template, jsonify, redirect

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global error state to prevent cascading failures
_error_state = {'initialization_error': None}

def create_app():
    """Create and configure Flask app."""
    try:
        app = Flask(__name__, 
                    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
                    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
        
        # Set Flask config for stability
        app.config['PROPAGATE_EXCEPTIONS'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True
        app.config['JSON_SORT_KEYS'] = False
        app.config['TRAP_HTTP_EXCEPTIONS'] = False
        app.config['TRAP_BAD_REQUEST_ERRORS'] = False
        
        # Defer database initialization to first request
        _db_initialized = [False]
        
        def _init_db_once():
            if not _db_initialized[0]:
                try:
                    from server.utils.db import init_db, DATABASE_PATH
                    logger.info("Initializing database...")
                    init_db()
                    logger.info("Database initialized successfully")
                    _db_initialized[0] = True
                except Exception as e:
                    logger.error(f"Database initialization error: {e}", exc_info=True)
                    _error_state['initialization_error'] = str(e)
        
        # Initialize database immediately
        _init_db_once()
        
        # Register blueprints with error handling - optimized for speed
        blueprints_config = [
            ('server.routes.auth', 'auth_bp', 'auth'),
            ('server.routes.parts', 'parts_bp', 'parts'),
            ('server.routes.builder', 'builder_bp', 'builder'),
            ('server.routes.games', 'games_bp', 'games'),
            ('server.routes.quick_parts', 'quick_parts_bp', 'quick_parts'),
            ('server.routes.compatibility', 'compatibility_bp', 'compatibility'),
            ('server.routes.ai_build', 'ai_bp', 'ai'),
            ('server.routes.ml_routes', 'ml_bp', 'ml'),
            ('server.routes.game_search', 'game_search_bp', 'game_search'),
            ('server.routes.search', 'search_bp', 'search'),
        ]
        
        for module_name, bp_name, display_name in blueprints_config:
            try:
                module = __import__(module_name, fromlist=[bp_name])
                bp = getattr(module, bp_name)
                app.register_blueprint(bp)
                logger.info(f"Registered {display_name} blueprint")
            except Exception as e:
                logger.error(f"Error registering {display_name} blueprint: {e}", exc_info=True)
        
        # Safe template rendering helper
        def safe_render(template_name):
            """Safely render template with fallback."""
            try:
                return render_template(template_name)
            except Exception as e:
                logger.error(f"Template render error for {template_name}: {e}", exc_info=True)
                return f"<html><body><h1>Page Loading</h1><p>Template: {template_name}</p></body></html>"
        
        @app.route('/login')
        def login_page():
            """Login page."""
            return safe_render('login.html')
        
        @app.route('/signup')
        def signup_page():
            """Signup page."""
            return safe_render('signup.html')
        
        @app.route('/')
        def home():
            """Show the animated landing intro before sign-in."""
            return safe_render('index.html')
        
        @app.route('/home')
        def dashboard():
            """Dashboard page after login."""
            return safe_render('home.html')
        
        @app.route('/integrated-builder')
        def integrated_builder():
            """Complete integrated PC builder with all steps."""
            return safe_render('integrated-builder.html')
        
        @app.route('/ai-domain-selection')
        def ai_domain_selection():
            """AI domain selection page."""
            return safe_render('ai-domain-selection.html')
        
        @app.route('/ai-game-input')
        def ai_game_input():
            """AI game/domain input page."""
            return safe_render('ai-game-input.html')
        
        @app.route('/ai-suggestions')
        def ai_suggestions():
            """AI build suggestions page."""
            return safe_render('ai-suggestions.html')
        
        @app.route('/performance-analysis')
        def performance_analysis():
            """Performance analysis page."""
            return safe_render('performance-analysis.html')
        
        @app.route('/summary')
        def summary():
            """Build summary page."""
            return safe_render('summary.html')
        
        @app.route('/manual-domain-selection')
        def manual_domain_selection():
            """Manual builder domain selection page."""
            return safe_render('manual-domain-selection.html')
        
        @app.route('/manual-goal-input')
        def manual_goal_input():
            """Manual builder goal/game input page."""
            return safe_render('manual-goal-input.html')
        
        @app.route('/manual-builder')
        def manual_builder():
            """Manual PC builder page."""
            return safe_render('manual-builder.html')
        
        @app.route('/3d-builder')
        def builder_3d():
            """3D drag-drop builder page."""
            return safe_render('3d-builder.html')
        
        @app.route('/builder')
        def builder():
            """PC builder page (legacy)."""
            return safe_render('builder.html')
        
        @app.route('/saved')
        def saved_builds():
            """Saved builds page."""
            return safe_render('saved.html')
        
        @app.route('/mode-selection')
        def mode_selection():
            """Build mode selection page (Manual vs AI)."""
            return safe_render('mode-selection.html')
        
        @app.route('/compare')
        def compare_page():
            """Component and build comparison page."""
            return safe_render('saved.html')
        
        @app.route('/health')
        def health():
            """Health check endpoint."""
            return jsonify({'status': 'ok', 'server': 'running'}), 200
        
        @app.before_request
        def before_request_handler():
            """Initialize DB and catch any startup errors."""
            # DISABLED - DB is initialized in create_app(), not on every request
            # Calling init_db() on every request can cause lock contention
            pass
        
        @app.after_request
        def after_request_handler(response):
            """Ensure proper response handling."""
            try:
                response.headers['X-Content-Type-Options'] = 'nosniff'
                response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            except:
                pass
            return response
        
        @app.errorhandler(404)
        def not_found(error):
            """Handle 404 errors - return HTML page."""
            logger.warning(f"404 error: {error}")
            return '<html><body><h1>PC Simulator</h1><p>Page found but rendered as fallback</p></body></html>', 200
        
        @app.route('/<path:path>')
        def catch_all(path):
            """Catch all undefined routes."""
            try:
                return render_template(f'{path}.html')
            except:
                return '<html><body><h1>PC Simulator - Page</h1></body></html>', 200
        
        @app.errorhandler(500)
        def server_error(error):
            """Handle 500 errors."""
            logger.error(f"500 error: {error}", exc_info=True)
            try:
                return render_template('500.html'), 500
            except:
                return jsonify({'error': 'Internal server error'}), 500
        
        @app.errorhandler(Exception)
        def handle_exception(error):
            """Handle uncaught exceptions."""
            logger.error(f"Uncaught exception: {error}", exc_info=True)
            import traceback
            print(f"EXCEPTION CAUGHT: {error}", flush=True)
            traceback.print_exc()
            sys.stdout.flush()
            return jsonify({'error': 'Server error', 'type': type(error).__name__}), 500
        
        # Wrap all view functions to catch exceptions
        def wrap_endpoint(endpoint):
            original = app.view_functions.get(endpoint)
            if not original:
                return
            
            def wrapped(*args, **kwargs):
                try:
                    return original(*args, **kwargs)
                except Exception as e:
                    print(f"VIEW WRAPPER ERROR in {endpoint}: {e}", flush=True)
                    import traceback
                    traceback.print_exc()
                    sys.stdout.flush()
                    raise
            
            wrapped.__name__ = original.__name__
            app.view_functions[endpoint] = wrapped
        
        # Wrap all view functions
        for endpoint in list(app.view_functions.keys()):
            wrap_endpoint(endpoint)
        
        logger.info("Flask app created successfully")
        return app
    
    except Exception as e:
        logger.critical(f"FATAL: Failed to create Flask app: {e}", exc_info=True)
        raise
