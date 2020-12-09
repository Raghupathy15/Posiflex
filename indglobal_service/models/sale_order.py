from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError,UserError

class SaleOrder(models.Model):
	_inherit = "sale.order"

	service_id = fields.Many2one('tickets', string="Name")