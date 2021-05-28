# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import whitelist
import frappe
from frappe.model.document import Document

class QuotingSheet(Document):
	def validate(self):
		self.calculate_totals()

	def calculate_totals(self):
		"""
		   Calculates total cost and cost per unit of item
		"""
		total_charges = self.rm_cost + self.packaging_charges + self.shipping_cost
		self.total_price  = total_charges + (total_charges * self.profit_markup/100)

		self.price_per_unit = self.total_price / self.qty	

@frappe.whitelist()
def get_item_details_quoting_sheet(item_code):
	"""
	Send valuation rate, stock UOM and default BOM name to quoting sheet

	Args:
		item_code (str): item code for sending details to raw materials table in quoting sheet

	Returns:
		dict: return valuation rate, stock UOM and default BOM
	"""	
	return frappe.db.get_values("Item", item_code, ["valuation_rate", "stock_uom", "default_bom"], as_dict=1)