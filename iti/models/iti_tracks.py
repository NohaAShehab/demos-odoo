from odoo import models, fields

class ITIStudent(models.Model):
    _name='iti.tracks'
    _description = "ITI tracks table "
    _rec_name = "track_name"
    track_name = fields.Char(required=True)
    opened = fields.Boolean()
    students_ids = fields.One2many("iti.students", "track_id", string="Students")  # logical field
