from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ITIStudent(models.Model):
    _name='iti.students'
    _description = "ITI students table "
    # _log_access=False

    name = fields.Char()
    age = fields.Integer()
    salary = fields.Float()
    gender = fields.Selection(
        [('m', "Male"), ('f', 'Female')]
    )
    cv = fields.Binary()
    image = fields.Binary()
    accepted = fields.Boolean()
    bio = fields.Html()
    registeration_at = fields.Datetime()
    track_id = fields.Many2one("iti.tracks")
    track_open = fields.Boolean(related='track_id.opened', readonly=False)
    skill_ids = fields.Many2many("iti.skills")
    military_certificate = fields.Binary()
    info = fields.Char()
    state= fields.Selection([
        ("new", "New"),
        ("pass1", "Passed first Interview"),
        ("pass2", "Passed second Interview"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected")], default='new')


    ############## Day03- Part02
    log_history_ids = fields.One2many("iti.log.history", "student_id")
    tax= fields.Float()
    computed_tax = fields.Float(compute="_cal_tax", store=True) # by default it is not saved until you say this


    @api.depends("salary")
    def _cal_tax(self):
        for record in self:
            record.computed_tax = record.salary*.2

    def get_selected_state(self):
        states = ["new", "pass1", "pass2", "accepted", "rejected"]
        index = states.index(self.state)
        return index
    def to_next(self):
        states = ["new", "pass1", "pass2", "accepted", "rejected"]
        selected = self.get_selected_state()
        print(selected)
        try:
            self.state= states[selected+1]
        except:
            self.state=states[0]

        description =f"status changed to {self.state}"
        if not self.env["iti.log.history"].search([
                ('create_uid','=', self.id), ('description', '=', description)]):
            self.env["iti.log.history"].create({
                "description": f"status changed to {self.state}",
                "student_id": self.id
            })

    def to_prev(self):
        states = ["new", "pass1", "pass2", "accepted", "rejected"]
        selected = self.get_selected_state()
        print(f"prev------------>{selected}")


        try:
            self.state = states[selected-1]
        except:
            self.state = states[-1]

    @api.onchange('accepted')
    def _onchange_accepted(self):
        # if self.accepted:
        #     self.salary +=1000
        #     return {
        #         "warning":{
        #             "title": "Hello",
        #             "message": f"the salary was changed to {self.salary}"
        #         }
        #     }
        print(len(self.track_id.students_ids))
        if len(self.track_id.students_ids) > 3:
            print("------------ Hereeeeeeeeeeeeeeeeeeee")
            return {
                "domain": {
                    "track_id": [()]
                },
                "warning":{
                    "title": "Note",
                    "message": f"You exceeded the students limit in the track"
                }
            }


    @api.model  # to identify that this a new record
    def create(self, vals):
        # if not vals.get("name"):
        #      print("--------- errorr  ")
        return super(ITIStudent, self).create(vals)
        # create function must return with the created object --- odoo can return
        # with any object has id property
        # return Dummy()

    # def write(self, vals):
    #     print(vals)
    #     if self.state=="accepted":
    #         raise UserError("You cannot updated user error ... ")
    #     return super(ITIStudent, self).write(vals)
    # #
    # def unlink(self):
    #     for record in self:  # self may hold different values
    #         if record.state !='new':
    #             raise UserError("You cannot delete passed user ... ")
    #         pass

    # ### faster than api constraints
    _sql_constraints = [
        ("duplicated_name", "UNIQUE(name)", "User with this name already exists"),
        # ("invalid age", "CHECK(age>0)", "User age must be greater than 20")
    ]

    @api.constrains("info")
    def check_valid_info(self):
        if self.info and len(self.info) < 20:
            raise ValidationError("The len of the info should be 20 or more ")

    @api.onchange("salary")
    def calculate_tax(self):
        self.tax = self.salary*.2


class Dummy:
    def __init__(self):
        self.id =10


############ Part 02

class ITILogHistory(models.Model):
    _name = "iti.log.history"

    description=fields.Char()
    student_id = fields.Many2one("iti.students")