import sys, os
 
sys.path.append('/Users/syrus/Sites/syrusakbary/website/')
sys.path.append('/Users/syrus/Sites/syrusakbary/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'



TEMPLATE_EXAMPLE = '''<ul>
{% for gender in gender_list %}
    <li>{{ gender.grouper }}
    <ul>
    {{ forloop.last }}
        {% for item in gender.list %}
        <li>{{ item.first_name|default:a|join:", "  }} {{ item.last_name|center:a }}</li>
        {% endfor %}
    </ul>
    </li>
{% endfor %}
{% trans 'hola' %}
</ul>'''

TEMPLATE_EXAMPLE2 = '''{% extends "admin/base.html" %}

{% block title %}{{ title }} | {% trans 'Django site admin'|default:'a' %}{% endblock %}

{% block branding %}
<h1 id="site-name">{% trans 'Django administration' %}</h1>
{% endblock %}
{% filter force_escape %}
Autoescapar
{% endfilter %}
{% autoescape on %}asd{% endautoescape %}
{% block nav-global %}{% endblock %}

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

TEMPLATE_ADMIN = '''{% load url from future %}<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE|default:"en-us" }}" {% if LANGUAGE_BIDI %}dir="rtl"{% endif %}>
<head>
<title>{% block title %}{% endblock %}</title>
<link rel="stylesheet" type="text/css" href="{% block stylesheet %}{% load adminmedia %}{% admin_media_prefix %}css/base.css{% endblock %}" />
{% block extrastyle %}{% endblock %}
<!--[if lte IE 7]><link rel="stylesheet" type="text/css" href="{% block stylesheet_ie %}{% load adminmedia %}{% admin_media_prefix %}css/ie.css{% endblock %}" /><![endif]-->
{% if LANGUAGE_BIDI %}<link rel="stylesheet" type="text/css" href="{% block stylesheet_rtl %}{% admin_media_prefix %}css/rtl.css{% endblock %}" />{% endif %}
<script type="text/javascript">window.__admin_media_prefix__ = "{% filter escapejs %}{% admin_media_prefix %}{% endfilter %}";</script>
{% block extrahead %}{% endblock %}
{% block blockbots %}<meta name="robots" content="NONE,NOARCHIVE" />{% endblock %}
</head>
{% load i18n %}

<body class="{% if is_popup %}popup {% endif %}{% block bodyclass %}{% endblock %}">

<!-- Container -->
<div id="container">

    {% if not is_popup %}
    <!-- Header -->
    <div id="header">
        <div id="branding">
        {% block branding %}{% endblock %}
        </div>
        {% if user.is_active and user.is_staff %}
        <div id="user-tools">
            {% trans 'Welcome,' %}
            <strong>{% filter force_escape %}{% firstof user.first_name user.username %}{% endfilter %}</strong>.
            {% block userlinks %}
                {% url 'django-admindocs-docroot' as docsroot %}
                {% if docsroot %}
                    <a href="{{ docsroot }}">{% trans 'Documentation' %}</a> /
                {% endif %}
                {% url 'admin:password_change' as password_change_url %}
                {% if password_change_url %}
                    <a href="{{ password_change_url }}">
                {% else %}
                    <a href="{{ root_path }}password_change/">
                {% endif %}
                {% trans 'Change password' %}</a> /
                {% url 'admin:logout' as logout_url %}
                {% if logout_url %}
                    <a href="{{ logout_url }}">
                {% else %}
                    <a href="{{ root_path }}logout/">
                {% endif %}
                {% trans 'Log out' %}</a>
            {% endblock %}
        </div>
        {% endif %}
        {% block nav-global %}{% endblock %}
    </div>
    <!-- END Header -->
    {% block breadcrumbs %}<div class="breadcrumbs"><a href="/">{% trans 'Home' %}</a>{% if title %} &rsaquo; {{ title }}{% endif %}</div>{% endblock %}
    {% endif %}

    {% block messages %}
        {% if messages %}
        <ul class="messagelist">{% for message in messages %}
          <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
        {% endfor %}</ul>
        {% endif %}
    {% endblock messages %}

    <!-- Content -->
    <div id="content" class="{% block coltype %}colM{% endblock %}">
        {% block pretitle %}{% endblock %}
        {% block content_title %}{% if title %}<h1>{{ title }}</h1>{% endif %}{% endblock %}
        {% block content %}
        {% block object-tools %}{% endblock %}
        {{ content }}
        {% endblock %}
        {% block sidebar %}{% endblock %}
        <br class="clear" />
    </div>
    <!-- END Content -->

    {% block footer %}<div id="footer"></div>{% endblock %}
</div>
<!-- END Container -->

</body>
</html>'''
from django.template import Template
from django.template.loader import *

from djinja.template.utils import DjinjaAdapter
from django.template.loader_tags import *
from django.templatetags.i18n import TranslateNode, BlockTranslateNode

dj = DjinjaAdapter(Template(TEMPLATE_EXAMPLE))


print dj.process()