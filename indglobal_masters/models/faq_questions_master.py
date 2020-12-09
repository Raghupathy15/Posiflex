from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime

class FAQ_Questions(models.Model):
    _name = 'questions.master'
    _inherit = ['mail.thread']
    _description = "FAQ - Question Master"

    # name = fields.Char(string="Name", required=True)
    categ_id = fields.Many2one('product.category',string="Product category")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    questions_line_ids = fields.One2many('questions.line', 'header_id')

class QuestionsLine(models.Model):
	_name = 'questions.line'
	_description = "Set of Questions"

	name = fields.Text("Questions")
	header_id = fields.Many2one('questions.master')