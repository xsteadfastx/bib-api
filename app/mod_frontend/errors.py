from flask import url_for, redirect, flash

from app.mod_frontend import mod_frontend


@mod_frontend.errorhandler(500)
def internal_server_error(error):
    flash('Something went wrong!', 'danger')

    return redirect(url_for('mod_frontend.index'))
