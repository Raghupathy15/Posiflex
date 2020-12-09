from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
import re
from odoo.exceptions import ValidationError

class ProductProduct(models.Model):
	_inherit = "product.template"

	default_code = fields.Char('Product code', index=True)
	prod_description = fields.Text('Product Description',required=True)
