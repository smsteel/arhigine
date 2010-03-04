# -*- coding: UTF-8 -*-

from output_class import OutputClass
from db_entities.custom_field import DBCustomField
from google.appengine.ext.webapp import template

class Customizer(OutputClass):
    """ this allows to customize site """

    url_handler = '/customize/?'
    access = 10
    param_set = DBCustomField().param_set
    
    def get(self):
        if not super(Customizer, self).get(): return
        
        param_set = self.param_set
        
        for param in param_set.values():
            try:
                rows = DBCustomField.gql("where type=:type", type = param["type"])
                param["value"] = (rows[0].value).encode("utf-8")
            except:
                #self.insertContent("<br/>type: " + param["type"])
                pass
        
        tpl_cust = template.Template ("""
        <form method="post" action="">
            <table>
            {% for param in params %}
                <tr>
                    <td>
                        {{param.caption}}
                    </td>
                    <td>
                    {% if param.txt_long %}
                        <textarea name="{{param.name}}">{{param.value}}</textarea>
                    {% else %}
                        <input type="text" name="{{param.name}}" size="40" value='{{param.value}}'>
                    {% endif %}
                    </td>
                </tr>
            {% endfor %}
                <tr>
                    <td>
                        
                    </td>
                    <td>
                        <input type="submit" value='Сохранить'>
                    </td>
                </tr>
            </table>
        <form>
        """)

        for param in param_set.values():
            if "txt_long" not in param:
                param["txt_long"] = True if len(param["value"]) > 100 else False
        out = tpl_cust.render(template.Context({"params":param_set.values()}))
        self.insertContent(out)
        self.drawPage()
    
    def post(self):
        if not super(Customizer, self).get(): return
        
        for param in self.param_set.values():
            param["value"] = self.request.get(param["name"])
            try:
                rows = DBCustomField.gql("where type=:type", type=param["type"])
                row = rows[0]
                row.value = param["value"]
                row.name = param["name"]
                row.put()
            except:
                row = DBCustomField()
                row.type = param["type"]
                row.value = param["value"]
                row.name = param["name"]
                row.put()
        self.insertContent("Сохранено")
        self.drawPage()
