from flask import render_template, redirect, url_for, flash, request, session
from . import auth_bp
from app.utils.supabase_client import get_supabase_client
import gotrue.errors

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        supabase = get_supabase_client()
        
        try:
            # Supabase Auth Login
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            session['user'] = response.user.id
            session['email'] = response.user.email
            flash('Acceso concedido. Bienvenido al Centro de Mando.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error de acceso: {str(e)}', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        supabase = get_supabase_client()
        
        try:
            # Supabase Auth Register
            response = supabase.auth.sign_up({"email": email, "password": password})
            flash('Cuenta creada. Por favor verifica tu correo o inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Error de registro: {str(e)}', 'danger')

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    supabase = get_supabase_client()
    supabase.auth.sign_out()
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))
