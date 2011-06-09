import sys, os
 
sys.path.append('/Users/syrus/Proyectos/exercita/website/')
sys.path.append('/Users/syrus/Sites/exercita/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


TEMPLATE_EXAMPLE = '''<ul>
{% for gender in gender_list %}
    <li>{{ gender.grouper }}
    <ul>
        {% for item in gender.list %}
        <li>{{ item.first_name|default:a|join:", "  }} {{ item.last_name|center:a }}</li>
        {% endfor %}
    </ul>
    </li>
{% endfor %}
</ul>'''

TEMPLATE_EXAMPLE2 = '''{% extends "admin/base.html" %}
{% load i18n %}

{% block title %}{{ title }} | {% trans 'Django site admin'|default:'a' %}{% endblock %}

{% block branding %}
<h1 id="site-name">{% trans 'Django administration' %}</h1>
{% endblock %}
{% filter force_escape %}
Autoescapar
{% endfilter %}
{% autoescape on %}asd{% endautoescape %}
{% block nav-global %}{% endblock %}
{% trans 'hola' %}
{% for user in users %}
    <li class="{% cycle 'odd' 'even' %}">{{ user }}</li>
    <li class="{% cycle 'odd' 'eveojkn' as b %}">{{ user }}</li>
    <li class="{% cycle b %}">{{ user }}b</li>
    {% include "admin/base.html" with a='1' r='2' aa='1' %}
{% empty %}
    Vacio
{% endfor %}
    {% ifequal a b %}a{% endifequal %}
    {% ifequal a b %}a{% else %}b{% endifequal %}
{% firstof a b 'hola' %}

{% if a|length > 0 or b and c|default:'b' <= c|default:'a' and not b%}
asd
{% endif %}
    {% blocktrans with amount=article.price count years=i.length %}
    That will cost $ {{ amount }} per year.
    {% plural %}
That will cost $ {{ amount }} per {{ years }} years.
{% endblocktrans %}

{% regroup people|dictsort:"gender" by gender_by as gender_list %}

{% url path.to.view arg arg2 as the_url %}
{% url app_views.client client.id %}
'''

TEMPLATE_ADMIN = '''{% extends "admin/base_site.html" %}
{% load i18n %}

{% block breadcrumbs %}<div class="breadcrumbs"><a href="/">{% trans "Home" %}</a> &rsaquo; {% trans "Server error" %}</div>{% endblock %}

{% block title %}{% trans 'Server error (500)' %}{% endblock %}

{% block content %}
<h1>{% trans 'Server Error <em>(500)</em>' %}</h1>
<p>{% trans "There's been an error. It's been reported to the site administrators via e-mail and should be fixed shortly. Thanks for your patience." %}</p>

{% endblock %}
'''
#from django.template.loader import *
from django.template import Template

from djinja.template.utils import DjinjaAdapter

dj = DjinjaAdapter(Template(TEMPLATE_EXAMPLE2))
print dj.process()