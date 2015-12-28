# -*- coding: utf-8 -*-

{
    "name" : 'web_ckeditor',
    "version" : "0.1",
    "author" : "Valentin LAB <valentin.lab@0k.io>",
    "depends" : [ 'web'],
    'data': [
        'web_ckeditor_master_view.xml',
    ],
    "installable" : True,
    "active" : False,
    "js": ["static/src/js/base.js",
           "static/lib/js/ckeditor/ckeditor.js" ],
    "css": [],
    "qweb": ["static/src/xml/*.xml", ]
}
