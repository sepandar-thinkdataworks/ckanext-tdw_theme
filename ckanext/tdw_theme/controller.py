import ckan.lib.base as base
import ckan.logic as logic
from ckan.common import _, request, c
import ckan.lib.captcha as captcha
import ckan.lib.navl.dictization_functions as dictization_functions
from pylons import config
import ckan.lib.mailer as mailer

unflatten = dictization_functions.unflatten

class SuggestController(base.BaseController):
    def __before__(self, action, **env):
        base.BaseController.__before__(self, action, **env)
        try:
            context = {'model': base.model, 'user': base.c.user or base.c.author,
                       'auth_user_obj': base.c.userobj}
            logic.check_access('site_read', context)
        except logic.NotAuthorized:
            base.abort(401, _('Not authorized to see this page'))


    def _send_suggestion(self, context):
        try:
            data_dict = logic.clean_dict(unflatten(
                logic.tuplize_dict(logic.parse_params(request.params))))
            context['message'] = data_dict.get('log_message', '')

            c.form = data_dict['name']
            captcha.check_recaptcha(request)

            #return base.render('suggest/form.html')
        except logic.NotAuthorized:
            base.abort(401, _('Not authorized to see this page'))

        except captcha.CaptchaError:
            error_msg = _(u'Bad Captcha. Please try again.')
            h.flash_error(error_msg)
            return self.suggest_form(data_dict) 


        errors = {}
        error_summary = {}

        if (data_dict["email"] == ''):

            errors['email'] = [u'Missing Value']
            error_summary['email'] =  u'Missing value'

        if (data_dict["name"] == ''):

            errors['name'] = [u'Missing Value']
            error_summary['name'] =  u'Missing value'


        if (data_dict["suggestion"] == ''):

            errors['suggestion'] = [u'Missing Value']
            error_summary['suggestion'] =  u'Missing value'


        if len(errors) > 0:
            return self.suggest_form(data_dict, errors, error_summary)
        else:
            # #1799 User has managed to register whilst logged in - warn user
            # they are not re-logged in as new user.
            mail_to = config.get('email_to')
            recipient_name = 'ThinkDataWorks'
            subject = 'CKAN - Dataset suggestion'

            body = 'Submitted by %s (%s)\n' % (data_dict["name"], data_dict["email"])

            if (data_dict["category"] != ''):
                body += 'Category: %s' % data_dict["category"]

            body += 'Request: %s' % data_dict["suggestion"]

            try:
                mailer.mail_recipient(recipient_name, mail_to,
                        subject, body)
            except mailer.MailerException:
                raise


            return base.render('suggest/suggest_success.html')


    def suggest_form(self, data=None, errors=None, error_summary=None):
        suggest_new_form = 'suggest/suggest_form.html'

        context = {'model': base.model, 'session': base.model.Session,
                   'user': base.c.user or base.c.author,
                   'save': 'save' in request.params,
                   'for_view': True}

        if (context['save']) and not data:
            return self._send_suggestion(context)

        data = data or {}
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}            

        c.form = base.render(suggest_new_form, extra_vars=vars)

        return base.render('suggest/form.html')

