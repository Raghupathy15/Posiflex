from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang, get_lang

class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	warranty_period = fields.Char(string="Warranty Months")
	discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)
	add_discount = fields.Selection([('percentage', 'Percentage'), ('amount', 'Amount')],string='Add Disc')

	@api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id','state','add_discount')
	def _compute_amount(self):
		"""
		Compute the amounts of the SO line.
		"""
		for line in self:
			if line.order_id.state == 'dis_app_sh':
				if line.add_discount == 'percentage':
					price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
					taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
					line.update({
						'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
						'price_total': taxes['total_included'],
						'price_subtotal': taxes['total_excluded'],
					})
					line.order_id.write({'is_dis_approved':True})
				elif line.add_discount == 'amount':
					price = line.price_subtotal - line.discount
					taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
					line.update({
						'price_subtotal': price,
					})
					line.order_id.write({'is_dis_approved':True})
			if line.order_id.is_dis_approved == False:
				price = line.price_unit
				taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
				line.update({
					'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
					'price_total': taxes['total_included'],
					'price_subtotal': taxes['total_excluded'],
				})

	@api.constrains('product_uom_qty','price_unit','discount')
	def _check_product_uom_qty(self):
		for product in self:
			if product.product_uom_qty < 1:
				raise UserError('Product Qty should be greater than Zero !!!')
			if product.price_unit <1:
				raise UserError('Unit price should be greater than Zero !!!')
			if product.add_discount == 'percentage':
				if product.discount < 0 or product.discount > 100:
					raise UserError('Discount should between 0 to 100 !!!')
			if product.add_discount == 'amount':
				if product.discount < 0 or product.price_subtotal < product.discount:
					raise UserError('You cannot enter discount amount greater than actual cost or value lower than 0. !!!')
			if product.product_uom_qty:
				qty = product.product_uom_qty % 1
				if qty != 0:
					raise UserError('Quantity should in whole number')
			if product.discount and not product.add_discount:
				raise UserError('Please select "Add disc" type')
			if product.add_discount and product.discount < 1:
				raise UserError('Please select discount value greater than zero')
					
	@api.onchange('product_id')
	def _onchange_warranty_months(self):
		if self.product_id:
			self.warranty_period = self.product_id.warranty_period

	@api.onchange('name')
	def _onchange_product_description(self):
		if self.name:
			self.name = self.product_id.prod_description