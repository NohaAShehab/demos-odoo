from odoo import models, fields

class ITIStudent(models.Model):
    _name='iti.skills'
    _description = "ITI skills table "
    name = fields.Char()
