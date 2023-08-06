from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, url_for,
    session
)
from werkzeug.exceptions import abort
from fossbill.auth import login_required, user_pref_smtp_enough
from fossbill.database import get_db
from fossbill.auth import setup_locale
from fossbill.auth import load_logged_in_user
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
import smtplib
from email.message import EmailMessage

bp = Blueprint('user', __name__, url_prefix='/me')

def get_user_smtp_server(user_pref):
    if user_pref.smtp_security == "TLS":
        server = smtplib.SMTP_SSL(
            host=user_pref.smtp_host,
            port=user_pref.smtp_port,
            timeout=10
        )
    else:
        server = smtplib.SMTP(
            host=user_pref.smtp_host,
            port=user_pref.smtp_port,
            timeout=10
        )
        if user_pref.smtp_security == "STARTTLS":
            server.starttls()

    server.login(user_pref.smtp_username, user_pref.smtp_password)

    return server

@bp.route('/test_email', methods=['POST'])
@login_required
@user_pref_smtp_enough
def test_email():
    body = render_template('user/test_email.plain')

    msg = EmailMessage()
    msg["From"] = g.user_pref.smtp_username
    msg["To"] = g.user_pref.email
    msg["Subject"] = _("Test email from Fossbill")
    msg.set_content(body)

    if g.user_pref.smtp_reply_to:
        msg["Reply-To"] = g.user_pref.smtp_reply_to
    if g.user_pref.smtp_cc:
        msg["Cc"] = g.user_pref.smtp_cc

    try:
        server = get_user_smtp_server(g.user_pref)
        server.send_message(msg)
        server.quit()
    except smtplib.SMTPException as e:
        flash(_("We failed to send the mail: " + str(e)))
        return redirect(url_for("user.update"))

    flash(_("We sent an email to you."))
    return redirect(url_for("user.update"))

@bp.route('/update', methods=('GET', 'POST'))
@login_required
def update():
    if request.method == 'POST':
        error = None

        smtp_host = request.form.get('smtp_host', None)
        if not smtp_host:
            smtp_host = None

        smtp_username = request.form.get('smtp_username', None)
        if not smtp_username:
            smtp_username = None

        smtp_password = request.form.get('smtp_password', None)
        if not smtp_password:
            smtp_password = None

        smtp_port = request.form.get('smtp_port', None)
        if not smtp_port:
            smtp_port = None
        else:
            try:
                int(smtp_port)
            except ValueError as ve:
                error = _('SMTP Port should be an integer.')

        smtp_security = request.form.get('smtp_security', None)
        if not smtp_security:
            smtp_security = None
        else:
            available_protocols = ['TLS', 'STARTTLS']
            if not smtp_security in available_protocols:
                error = _('SMTP Security should be one of {available_protocols}.').format(
                    available_protocols=', '.join(available_protocols)
                )

        smtp_reply_to = request.form.get('smtp_reply_to', None)
        if not smtp_reply_to:
            smtp_reply_to = None

        smtp_cc = request.form.get('smtp_cc', None)
        if not smtp_cc:
            smtp_cc = None

        quote_mentions = request.form.get('quote_mentions', None)
        if not quote_mentions:
            quote_mentions = None

        bill_mentions = request.form.get('bill_mentions', None)
        if not bill_mentions:
            bill_mentions = None

        available_locales = ['en_US', 'fr_FR']
        if not request.form.get('locale') in available_locales:
            error = _('Locale should be one of {available_locales}.').format(
                available_locales = ', '.join(available_locales)
            )

        email = request.form.get('email', None)
        if not email:
            email = None

        currency = request.form.get('currency', None)
        if not currency:
            currency = None

        source = request.form.get('source', None)
        if not source:
            source = None

        if error is None:
            engine, metadata = get_db()
            user_prefs = metadata.tables['user_pref']

            stmt = user_prefs.update().values(
                bill_mentions=bill_mentions,
                currency=currency,
                email=email,
                locale=request.form['locale'],
                quote_mentions=quote_mentions,
                smtp_host=smtp_host,
                smtp_password=smtp_password,
                smtp_port=smtp_port,
                smtp_security=smtp_security,
                smtp_username=smtp_username,
                smtp_reply_to=smtp_reply_to,
                smtp_cc=smtp_cc,
                source=source,
            ).where(
                user_prefs.c.user_id == g.user.id,
            )
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                error = f"Something went wrong."
            else:
                load_logged_in_user() # refresh stripe_customer
                setup_locale() # refresh locale
                flash(_("User updated."))
                return redirect(url_for("user.update"))

        flash(error)

    return render_template('user/update.html')


@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    engine, metadata = get_db()

    try:
        with engine.connect() as conn:
            for table_name in ['user_pref', 'bill_row', 'bill', 'client', 'product', 'payment']:
                table = metadata.tables[table_name]
                stmt = table.delete().where(
                    table.c.user_id == g.user.id,
                )
                result = conn.execute(stmt)

            stmt = metadata.tables['user'].delete().where(
                metadata.tables['user'].c.id == g.user.id,
            )
            result = conn.execute(stmt)

            conn.commit()

            session.clear()

            return redirect(url_for("landing.home"))
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))

    return redirect(url_for("user.update"))

@bp.route('/delete_bills', methods=['POST'])
@login_required
def delete_bills():
    engine, metadata = get_db()

    try:
        with engine.connect() as conn:
            for table_name in ['bill_row', 'bill']:
                table = metadata.tables[table_name]
                stmt = table.delete().where(
                    table.c.user_id == g.user.id,
                )
                result = conn.execute(stmt)

            conn.commit()
            flash(_("All bills has been deleted."))
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))

    return redirect(url_for("user.update"))
